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

	def filter_columns(self, column_list, rename_columns):

		self.results_df = self.results_df[column_list]

		self.results_df.rename(columns=rename_columns, inplace=True)

	def extract_gameweek_points(self):

		points_list = {}
		gameweek_number = 0

		for index,result in self.results_df.iterrows():

			gameweek = result['gameweek']

			if gameweek not in points_list:
				points_list[gameweek] = []

			points_list[result['gameweek']].append({
				result['player_1']: result['player_1_points'],
				result['player_2']: result['player_2_points']
			})

		return points_list
		#return pd.DataFrame(points_list)

