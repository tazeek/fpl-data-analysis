from Results import Results
from APIConnector import APIConnector
from GameweekStats import GameweekStats
from Teams import Teams

class Graphs:

	def __init__(self):

		self._results_obj = Results()
		self._api_connector = APIConnector()
		
		self._gameweek_stats = GameweekStats(self._api_connector.get_events_gameweeks())
		self._team_info = Teams(self._api_connector.get_teams_information())

	def get_future_fdr_scores(self):

		results_obj = self._results_obj
		team_df = self._team_info.return_dataframe_obj()

		results_obj.map_teams(team_df)

		future_opp_score_df = results_obj.get_future_opponents_stats(gameweek_stats.current_gameweek_number())

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