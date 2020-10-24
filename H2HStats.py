import pandas as pd
import requests

class H2HStats:

	def __init__(self, id):

		self.id = id

	def extract_results(self, current_gameweek):

		url = 'https://fantasy.premierleague.com/api/leagues-h2h-matches/league/{}/?page=1'.format(self.id)
		r = requests.get(url)
		json = r.json()

		results_list = []

		for result in json['results']:

			if result['event'] > (current_gameweek + 1):
				break

			results_list.append(result)


		self.results_df = pd.DataFrame(results_list)

	def filter_columns(self, column_list):

		self.results_df = self.results_df[column_list]