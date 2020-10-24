import pandas as pd
import requests

class H2HStats:

	def __init__(self, id):

		self.id = id

	def extract_results(self):

		url = 'https://fantasy.premierleague.com/api/leagues-h2h-matches/league/{}/?page=1'.format(self.id)
		r = requests.get(url)
		json = r.json()

		self.results_df = pd.DataFrame(json['results'])

	def filter_columns(self, column_list):

		self.results_df = self.results_df[column_list]