import pandas as pd
import requests

class H2HStats:

	def __init__(self, id):

		self.id = id

	def extract_results(self):

		url = 'https://fantasy.premierleague.com/api/leagues-h2h-matches/league/{}/?page=1'.format(self.id)
		r = requests.get(url)
		json = r.json()

		return pd.DataFrame(json['results'])