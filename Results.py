import pandas as pd
import numpy as np
import requests

class Results:

	def __init__(self):

		url = 'https://fantasy.premierleague.com/api/fixtures/'
		r = requests.get(url)

		self.results_matches_df =  pd.DataFrame(r.json())

	def drop_columns(self, drop_columns):

		self.results_matches_df = self.results_matches_df.drop(drop_columns, axis=1)