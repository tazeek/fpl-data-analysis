from Results import Results
from APIConnector import APIConnector
from GameweekStats import GameweekStats
from Teams import Teams

import plotly.graph_objects as go

class Graphs:

	def __init__(self):

		self._api_connector = APIConnector()
		
		self._team_info = Teams(self._api_connector.get_teams_information())

		self._results_obj = Results(self._team_info)
		self._gameweek_results = self._results_obj.prepare_gameweek_stats()

		self._gameweek_obj = GameweekStats(self._api_connector.get_events_gameweeks())
		self._gameweek_number = self._gameweek_obj.current_gameweek_number().item() # convert int64 to int
		self._x_values = [i for i in range(1, self._gameweek_number + 1)]

	def get_future_fdr_scores_fig(self):

		future_opp_score_df = self._results_obj.get_future_opponents_stats(self._gameweek_number)

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
			yaxis_tickformat=',d'
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
			yaxis_tickformat=',d'
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
