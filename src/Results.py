import pandas as pd
import numpy as np
import requests

class Results:

	def __init__(self, team_info_df, gameweek_num):

		url = 'https://fantasy.premierleague.com/api/fixtures/'
		filter_columns = ['code','finished_provisional','id','kickoff_time',
		'minutes','provisional_start_time','started','pulse_id']

		r = requests.get(url)

		self._results_matches_df =  pd.DataFrame(r.json())
		self._results_matches_df.drop(filter_columns, axis=1, inplace=True)
		self._gameweek_num = gameweek_num
		self._window_num = 4
		
		self._map_teams(team_info_df)

	def _map_teams(self,team_df):

		team_names = team_df.set_index('id').name

		for team in ['team_a','team_h']:
			self._results_matches_df[team] = self._results_matches_df[team].map(team_names)

		return None

	def prepare_gameweek_stats(self):

		gw_stats_df = self._results_matches_df.copy()
		gw_stats_df.dropna(inplace=True)

		# Prepare stats for clean sheet
		gw_stats_df['home_team_cs'] = False
		gw_stats_df['away_team_cs'] = False

		gw_stats_df.loc[gw_stats_df['team_h_score'] == 0, 'away_team_cs'] = True
		gw_stats_df.loc[gw_stats_df['team_a_score'] == 0, 'home_team_cs'] = True

		# Count number of goals scored
		gw_stats_df = gw_stats_df.groupby(['event']).sum()

		gw_stats_df.rename(columns = {
			'team_h_score':'home_team', 
			'team_a_score': 'away_team'
		}, inplace = True)

		return gw_stats_df

	def get_future_opponents_stats(self):

		future_opp_score_df = self._results_matches_df.copy()

		event_col = future_opp_score_df['event']

		upper_bound = self._gameweek_num + self._window_num
		future_opp_score_df = future_opp_score_df[(event_col > self._gameweek_num) & (event_col <= upper_bound)]

		home_teams_df = future_opp_score_df[['event','team_h','team_h_difficulty']].copy()
		away_teams_df = future_opp_score_df[['event','team_a','team_a_difficulty']].copy()

		home_teams_df.rename(columns={'team_h': 'team', 'team_h_difficulty':'difficulty'}, inplace=True)
		away_teams_df.rename(columns={'team_a': 'team', 'team_a_difficulty':'difficulty'}, inplace=True)

		overall_df = pd.concat([home_teams_df,away_teams_df])

		overall_df = overall_df.groupby(['team']).mean()
		overall_df.reset_index(level=0, inplace=True)
		overall_df.drop(['event'], axis=1, inplace=True)

		return overall_df.sort_values('difficulty')

	def find_previous_match_results(self):

		# Filter columns and drop null values
		results_matches_df = self._results_matches_df.copy()
		results_matches_df.dropna(inplace=True)

		# Filter from lower to current gameweek
		event_col = results_matches_df['event']
		lower_bound = self._gameweek_num - self._window_num
		results_matches_df = results_matches_df[(event_col <= self._gameweek_num) & (event_col > lower_bound)]

		# Convert to list of dictionary and create the dictionary for goals stats
		team_form_dict = {}

		for results in results_matches_df.to_dict('records'):

			home_team = results['team_h']
			away_team = results['team_a']

			if home_team not in team_form_dict:
				team_form_dict[home_team] = {
					'goals_for': 0,
					'goals_against': 0,
					'clean_sheets_num': 0
				}

			if away_team not in team_form_dict:
				team_form_dict[away_team] = {
					'goals_for': 0,
					'goals_against': 0,
					'clean_sheets_num': 0
				}

			home_score = results['team_h_score']
			away_score = results['team_a_score']

			team_form_dict[away_team]['clean_sheets_num'] += 1 if home_score == 0 else 0
			team_form_dict[home_team]['clean_sheets_num'] += 1 if away_score == 0 else 0

			team_form_dict[home_team]['goals_for'] += home_score
			team_form_dict[home_team]['goals_against'] += away_score

			team_form_dict[away_team]['goals_for'] += away_score
			team_form_dict[away_team]['goals_against'] += home_score

		# Convert back to dataframe and find goal difference
		team_form_df = pd.DataFrame.from_dict(team_form_dict, orient='index')
		team_form_df['total_goals_involved'] = team_form_df['goals_for'] + team_form_df['goals_against']

		return team_form_df

	def _return_empty_dict_player(self, id):

		return {
			'id': id,
			'goals': 0,
			'assists': 0,
			'bonus': 0
		}

	def find_stats_previous_matches(self, player_details):

		# Filter columns and drop null values
		results_matches_df = self._results_matches_df.copy()
		event_col = results_matches_df['event']

		lower_bound = self._gameweek_num - self._window_num
		results_matches_df = results_matches_df[(event_col <= self._gameweek_num) & (event_col > lower_bound)]

		in_form_players_dict = {}

		for stat in results_matches_df['stats']:

			if len(stat) == 0:
				continue

			goals_scored_json = stat[0]
			goals_assists_json = stat[1]
			bonus_points_json = stat[8]

			# For goals scored
			for scorer in goals_scored_json['a'] + goals_scored_json['h']:
				player = scorer['element']
				goals_scored = scorer['value']

				if player not in in_form_players_dict:
					in_form_players_dict[player] = self._return_empty_dict_player(player)

				in_form_players_dict[player]['goals'] += goals_scored

			# For assists
			for assister in goals_assists_json['a'] + goals_assists_json['h']:
				player = assister['element']
				goals_assist = assister['value']

				if player not in in_form_players_dict:
					in_form_players_dict[player] = self._return_empty_dict_player(player)

				in_form_players_dict[player]['assists'] += goals_assist

			# For bonus points
			for bonus_player in bonus_points_json['a'] + bonus_points_json['h']:
				player = bonus_player['element']
				bonus_points = bonus_player['value']

				if player not in in_form_players_dict:
					in_form_players_dict[player] = self._return_empty_dict_player(player)

				in_form_players_dict[player]['bonus'] += bonus_points

		inform_stats_df = pd.DataFrame.from_dict(in_form_players_dict, orient='index')

		inform_stats_df['involved'] = inform_stats_df['goals'] + inform_stats_df['assists']

		# Filter out players who are not so involved
		inform_stats_df.query('involved > 1', inplace=True)

		# Filter out players who do not have a lot of bonuses
		bonus_stats_only_df = inform_stats_df[['id', 'bonus']].copy()
		bonus_stats_only_df.query('bonus > 3', inplace=True)

		# Reset index to get the ID
		inform_stats_df.reset_index(drop=True,inplace=True)
		bonus_stats_only_df.reset_index(drop=True,inplace=True)

		# Merge with player dataframe to find names
		inform_stats_df = pd.merge(player_details, inform_stats_df, on='id')
		bonus_stats_only_df = pd.merge(player_details, bonus_stats_only_df, on='id')

		# Sort in descending order
		inform_stats_df.sort_values('involved',inplace=True)
		bonus_stats_only_df.sort_values('bonus',inplace=True)


		return inform_stats_df, bonus_stats_only_df

