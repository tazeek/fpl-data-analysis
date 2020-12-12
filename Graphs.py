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