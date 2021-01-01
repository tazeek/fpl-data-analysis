from GameweekStats import GameweekStats
from Teams import Teams
from Results import Results

import requests

class APIConnector:

	def __init__(self):

		url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

		r = requests.get(url)
		self.json_object = r.json()

		self._team_info = None
		self._gameweek_obj = None

	def show_all_keys(self):
		return self.json_object.keys()

	def get_events_gameweeks(self):
		if self._gameweek_obj is None:
			self._gameweek_obj = GameweekStats(self._api_connector.get_events_gameweeks())

		return self._gameweek_obj

	def get_teams_information(self):
		if self._team_info is None:
			self._team_info = Teams(self._api_connector.get_teams_information())

		return self._team_info

	def get_player_information(self):
		return self.json_object['elements']

	def get_player_types(self):
		return self.json_object['element_types']