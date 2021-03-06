from src.Results import Results
from src.APIConnector import APIConnector
from src.GameweekStats import GameweekStats
from src.Teams import Teams

import plotly.graph_objects as go

class Graphs:

	def __init__(self):

		self._api_connector = APIConnector()

		self._teams_info = self._api_connector.get_teams_information()
		self._gameweek_obj = self._api_connector.get_events_gameweeks()
		self._player_obj = self._api_connector.get_player_information()
		self._gameweek_number = self._gameweek_obj.get_current_gameweek()

		self._results_obj = Results(self._teams_info.return_dataframe_obj(), self._gameweek_number)
		self._gameweek_results = self._results_obj.prepare_gameweek_stats()

		self._x_values = [i for i in range(1, self._gameweek_number + 1)]

	def get_future_fdr_scores_fig(self):

		future_opp_score_df = self._results_obj.get_future_opponents_stats()

		fig = go.Figure(
			go.Bar(
				x=future_opp_score_df['difficulty'],
				y=future_opp_score_df['team'],
				orientation='h'
			)
		)

		fig.update_layout(
			title="Average FDR for teams (Next 4 matches)",
			height = 700
		)

		fig.update_xaxes(
			title_text = "Average FDR",
			tickangle = 45,
			title_standoff = 25
		)

		return fig

	def get_chips_stats_fig(self):

		chip_stats_df = self._gameweek_obj.fetch_chip_stats()

		chip_stats_df.rename(
			columns = {
				'bboost':'bench_boost', 
				'3xc':'triple_captain'
			},
			inplace = True
		)

		fig = go.Figure()

		for column in chip_stats_df.columns:

			fig.add_trace(
				go.Scatter(
					x=self._x_values, 
					y=chip_stats_df[column],
					mode='lines+markers',
					name=column
				)
			)

		fig.update_layout(
			title="Number of chips played per gameweek",
			hovermode='x',
			yaxis_tickformat='k'
		)

		fig.update_xaxes(
			title_text = "Gameweek",
			tickangle = 45,
			nticks = self._gameweek_number + 1,
			title_standoff = 25
		)

		fig.update_yaxes(
			title_text = "Total",
			title_standoff = 25
		)

		return fig

	def get_goals_scored_stats_fig(self):

		fig = go.Figure() 

		for column in ['home_team','away_team']:

			fig.add_trace(
				go.Scatter(
					x=self._x_values, 
					y=self._gameweek_results[column],
					mode='lines+markers',
					name=column
				)
			)

		fig.update_layout(
			title="Goals scored per gameweek (Home vs Away)",
			hovermode='x',
			yaxis_tickformat='k'
		)

		fig.update_xaxes(
			title_text = "Gameweek",
			tickangle = 45,
			title_standoff = 25
		)

		fig.update_yaxes(
			title_text = "Goals scored",
			title_standoff = 25
		)

		return fig

	def get_clean_sheets_stats_fig(self):

		fig = go.Figure()

		for column in ['home_team_cs','away_team_cs']:

			fig.add_trace(
				go.Scatter(
					x=self._x_values, 
					y=self._gameweek_results[column],
					mode='lines+markers',
					name=column
				)
			)

		fig.update_layout(
			title="Clean sheets per gameweek (Home vs Away)",
			hovermode='x',
			yaxis_tickformat='k'
		)

		fig.update_xaxes(
			title_text = "Gameweek",
			tickangle = 45,
			title_standoff = 25
		)

		fig.update_yaxes(
			title_text = "Number of clean sheets",
			title_standoff = 25
		)

		return fig

	def get_fpl_scores_stats(self):

		fig = go.Figure()

		scores_df = self._gameweek_obj.fetch_scores()

		fig.add_trace(
			go.Scatter(
				x=self._x_values, 
				y=scores_df['average_entry_score'],
				mode='lines+markers',
				name='Average Score'
			)
		)

		fig.update_layout(
			title="Average scores per gameweek",
			hovermode="x"
		)

		fig.update_xaxes(
			title_text = "Gameweek",
			tickangle = 45,
			nticks = self._gameweek_number,
			title_standoff = 25
		)


		fig.update_yaxes(
			title_text = "Scores",
			title_standoff = 25
		)

		return fig

	def get_transfers_stats(self):

		fig = go.Figure()

		transfers_df = self._gameweek_obj.fetch_transfers()

		fig.add_trace(
			go.Scatter(
				x=self._x_values, 
				y=transfers_df['transfers_made'],
				mode='lines+markers',
				hovertemplate='Total: %{y}'
			)
		)

		fig.update_layout(
			title="Total transfers per gameweek"
		)

		fig.update_xaxes(
			title_text = "Gameweek",
			tickangle = 45,
			nticks = self._gameweek_number,
			title_standoff = 25
		)

		return fig

	def _get_clean_sheets_form(self, team_form_df):

		team_form_df.sort_values('clean_sheets_num', inplace=True) 

		fig = go.Figure()

		fig.add_trace(
			go.Bar(
				y=team_form_df.index,
				x=team_form_df['clean_sheets_num'],
				orientation='h'
			)
		)

		fig.update_layout(
			title="Total clean sheets in the last 4 matches",
			height = 700
		)

		fig.update_xaxes(
			title_text = "Number",
			tickangle = 45,
			title_standoff = 25
		)

		return fig


	def _get_goals_scored_conceded(self, team_form_df):

		team_form_df.sort_values('total_goals_involved',inplace=True)

		fig = go.Figure()

		fig.add_trace(
			go.Bar(
				y=team_form_df.index,
				x=team_form_df['goals_for'],
				name='Goals scored',
				orientation='h',
				texttemplate="%{x}",
				textposition="inside",
				textfont_color='white',
				hoverinfo='none',
				marker=dict(
				color='rgba(13, 142, 6, 0.81)',
				line=dict(color='rgba(13, 142, 6, 1)', width=2))
			)
		)

		fig.add_trace(
			go.Bar(
				y=team_form_df.index,
				x=team_form_df['goals_against'],
				name='Goals against',
				orientation='h',
				texttemplate="%{x}",
				textposition="inside",
				textfont_color='white',
				hoverinfo='none',
				marker=dict(
				color='rgba(142, 6, 6, 0.81)',
				line=dict(color='rgba(142, 6, 6, 1)', width=2))
			)
		)

		fig.update_layout(
			barmode='stack',
			title="Goals for and against (Previous four matches)",
			height = 700
		)
		
		return fig

	def get_info_about_teams_form(self):

		team_form_df = self._results_obj.find_previous_match_results()

		return {
			'goals_scored_concded_fig': self._get_goals_scored_conceded(team_form_df[['goals_for','goals_against','total_goals_involved']].copy()),
			'clean_sheets_fig': self._get_clean_sheets_form(team_form_df[['clean_sheets_num']].copy())
		}

	def get_stats_about_players(self):

		player_details = self._player_obj.get_player_names()

		prev_stats_df, bonus_stats_df = self._results_obj.find_stats_previous_matches(player_details)

		inform_stats_fig = go.Figure()

		inform_stats_fig.add_trace(
			go.Bar(
				y=prev_stats_df['name'],
				x=prev_stats_df['goals'],
				name='Goals scored',
				orientation='h',
				texttemplate="%{x}",
				textposition="inside",
				textangle=0,
				textfont_color='white',
				hoverinfo='none',
				marker=dict(
				color='rgba(13, 142, 6, 0.81)',
				line=dict(color='rgba(13, 142, 6, 1)', width=2))
			)
		)

		inform_stats_fig.add_trace(
			go.Bar(
				y=prev_stats_df['name'],
				x=prev_stats_df['assists'],
				name='Assists',
				orientation='h',
				texttemplate="%{x}",
				textposition="inside",
				textangle=0,
				textfont_color='white',
				hoverinfo='none',
				marker=dict(
				color='rgba(142, 6, 6, 0.81)',
				line=dict(color='rgba(142, 6, 6, 1)', width=2))
			)
		)

		inform_stats_fig.update_yaxes(
			autorange="reversed"
		)

		inform_stats_fig.update_layout(
			barmode='stack',
			title="Goals and assists (Last 4 matches)",
			height = 50 * len(prev_stats_df)
		)

		bonus_points_fig = go.Figure()

		bonus_points_fig.add_trace(
			go.Bar(
				y=bonus_stats_df['name'],
				x=bonus_stats_df['bonus'],
				orientation='h'
			)
		)

		bonus_points_fig.update_layout(
			title="Total bonuses in last 4 matches (at least 3)",
			height = 700
		)

		bonus_points_fig.update_xaxes(
			title_text = "Number",
			tickangle = 45,
			title_standoff = 25
		)

		return inform_stats_fig, bonus_points_fig

	def get_popular_players(self):

		player_stats_picked = self._player_obj.get_popular_players(20)

		fig = go.Figure()

		fig.add_trace(
			go.Bar(
				y=player_stats_picked['name'],
				x=player_stats_picked['selected_by_percent'],
				orientation='h'
			)
		)

		fig.update_layout(
			title="Top popular players",
			height = 700
		)

		fig.update_xaxes(
			title_text = "% selected by",
			tickangle = 45,
			title_standoff = 25
		)

		fig.update_yaxes(
			autorange="reversed"
		)

		return fig
