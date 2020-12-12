from Results import Results
from APIConnector import APIConnector
from GameweekStats import GameweekStats
from Teams import Teams

import plotly.graph_objects as go

class Graphs:

	def __init__(self):

		self._results_obj = Results()
		self._api_connector = APIConnector()
		
		self._gameweek_stats = GameweekStats(self._api_connector.get_events_gameweeks())
		self._team_info = Teams(self._api_connector.get_teams_information())

	def get_future_fdr_scores_fig(self):

		results_obj = self._results_obj
		team_df = self._team_info.return_dataframe_obj()

		results_obj.map_teams(team_df)

		future_opp_score_df = results_obj.get_future_opponents_stats(self._gameweek_stats.current_gameweek_number())

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

		gameweek_stats = self._gameweek_stats

		chip_stats_df = gameweek_stats.fetch_chip_stats()
		total_gameweeks_played = gameweek_stats.total_gameweeks()
		x_values = [i for i in range(1, total_gameweeks_played + 1)]

		chip_stats_df.rename(
			columns = {
			'bboost':'bench_boost', 
			'3xc':'triple_captain'
			},
			inplace = True
		)

		fig = go.Figure()

		for column in chip_stats_df.columns:

			fig.add_trace(go.Scatter(x=x_values, y=chip_stats_df[column],
				mode='lines+markers',
				name=column))

		fig.update_layout(
			title="Number of chips played per gameweek",
			hovermode='x unified',
			yaxis_tickformat='k'
		)

		fig.update_xaxes(
			title_text = "Gameweek",
			tickangle = 45,
			nticks = total_gameweeks_played + 1,
			title_standoff = 25
		)

		fig.update_yaxes(
			title_text = "Total",
			title_standoff = 25
		)

		return fig