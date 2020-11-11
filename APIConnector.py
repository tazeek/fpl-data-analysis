import requests

class APIConnector:

	def __init__(self):

		url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

		r = requests.get(url)
		self.json_object = r.json()

	def show_all_keys(self):
		return self.json_object.keys()

	def get_events_gameweeks(self):
		return self.json_object['events']

	def get_teams_information(self):
		return self.json_object['teams']

	def get_player_information(self):
		return self.json_object['elements']

	def get_player_types(self):
		return self.json_object['element_types']