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

		return pd.DataFrame(points_list)

	def extract_player_points(self):

		player_points_dict = {}
		player_points_list = []
		gameweek_number = 1

		for index,result in self.results_df.iterrows():

			if gameweek_number != result['gameweek']:

				player_points_list.append(player_points_dict.copy())
				gameweek_number = result['gameweek']

			player_1_name = result['player_1']
			player_2_name = result['player_2']

			if player_1_name not in player_points_dict:
				player_points_dict[player_1_name] = 0

			if player_2_name not in player_points_dict:
				player_points_dict[player_2_name] = 0

			# Find the points difference
			# - If > 0, player 1 has won
			# - If < 0, player 2 has won
			# - If it is 0, it is a draw
			points_difference = result['player_1_points'] - result['player_2_points']

			if points_difference > 0:
				player_points_dict[player_1_name] += 3
			elif points_difference < 0:
				player_points_dict[player_2_name] += 3
			else:
				player_points_dict[player_1_name] += 1
				player_points_dict[player_2_name] += 1


		# Append the last gameweek
		player_points_list.append(player_points_dict)

		return pd.DataFrame(player_points_list)
