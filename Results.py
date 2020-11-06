import pandas as pd
import numpy as np
import requests

class Results:

	def __init__(self):

		url = 'https://fantasy.premierleague.com/api/fixtures/'
		r = requests.get(url)

		self.results_matches_df =  pd.DataFrame(r.json())

	def drop_columns(self, drop_columns):

		self.results_matches_df = self.results_matches_df.drop(drop_columns, axis=1)

	def map_teams(self,team_df):

		my_df = self.results_matches_df
		team_names = team_df.set_index('id').name

		my_df['team_a'] = my_df.team_a.map(team_names)
		my_df['team_h'] = my_df.team_h.map(team_names)

		self.results_matches_df = my_df

	def prepare_gameweek_stats(self):

		gw_stats_df = self.results_matches_df[['event','team_h_score','team_a_score']].copy()
		gw_stats_df.dropna(inplace=True)

		gw_stats_df['home_team_cs'] = False
		gw_stats_df['away_team_cs'] = False

		gw_stats_df.loc[gw_stats_df['team_h_score'] == 0, 'away_team_cs'] = True
		gw_stats_df.loc[gw_stats_df['team_a_score'] == 0, 'home_team_cs'] = True

		gw_stats_df = gw_stats_df.groupby(['event']).sum()

		return gw_stats_df

	def prepare_goal_stats(self):

		goals_df = self.results_matches_df[['event','team_h_score','team_a_score']].copy()
		goals_df.dropna(inplace=True)

		# Sum up: home goals, away goals
		goals_df = goals_df.groupby(['event']).sum()

		return goals_df

	def prepare_clean_sheet_stats(self):

		clean_sheets_df = self.results_matches_df[['event','team_h_score','team_a_score']].copy()
		clean_sheets_df.dropna(inplace=True)

		clean_sheets_df['home_team_cs'] = False
		clean_sheets_df['away_team_cs'] = False

		clean_sheets_df.loc[clean_sheets_df['team_h_score'] == 0, 'away_team_cs'] = True
		clean_sheets_df.loc[clean_sheets_df['team_a_score'] == 0, 'home_team_cs'] = True

		clean_sheets_df = clean_sheets_df.groupby(['event']).sum()

		return clean_sheets_df

	def get_future_opponents_stats(self,current_gameweek_num):

		future_matches_num = 4
		column_list = ['event','team_h','team_h_difficulty','team_a','team_a_difficulty']

		future_opp_score_df = self.results_matches_df[column_list].copy()

		event_col = future_opp_score_df['event']

		upper_bound = current_gameweek_num + future_matches_num
		future_opp_score_df = future_opp_score_df[(event_col > current_gameweek_num) & (event_col <= upper_bound)]

		home_teams_df = future_opp_score_df[['event','team_h','team_h_difficulty']].copy()
		away_teams_df = future_opp_score_df[['event','team_a','team_a_difficulty']].copy()

		home_teams_df.rename(columns={'team_h': 'team', 'team_h_difficulty':'difficulty'}, inplace=True)
		away_teams_df.rename(columns={'team_a': 'team', 'team_a_difficulty':'difficulty'}, inplace=True)

		overall_df = pd.concat([home_teams_df,away_teams_df])

		return overall_df