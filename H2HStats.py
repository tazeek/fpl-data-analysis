import pandas as pd
import numpy as np
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

	def filter_columns(self, column_list, rename_columns):

		self.results_df = self.results_df[column_list]

		self.results_df.rename(columns=rename_columns, inplace=True)

	def extract_gameweek_points(self):

		points_list = []
		gameweek_points = {}

		# Gameweek always starts at 1
		gameweek_number = 1

		for index,result in self.results_df.iterrows():

			# Check if gameweek number is same:
			# If so: Add to existing dictionary
			if gameweek_number != result['gameweek']:

				points_list.append(gameweek_points)

				gameweek_number = result['gameweek']
				gameweek_points = {}
				

			gameweek_points[result['player_1']] =  result['player_1_points']
			gameweek_points[result['player_2']] =  result['player_2_points']

		# Append the recent gameweek data
		points_list.append(gameweek_points)

		points_list_df = pd.DataFrame(points_list)

		points_list_df['average'] = points_list_df.mean(axis=1).apply(np.ceil)

		return points_list_df
