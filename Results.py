import pandas as pd
import numpy as np
import requests

class Results:

	def __init__(self):

		url = 'https://fantasy.premierleague.com/api/fixtures/'
		r = requests.get(url)
		json = r.json()

		self.results_matches_df = pd.Dataframe(json)