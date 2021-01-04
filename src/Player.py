import pandas as pd

class Player:

	def __init__(self, players_json):
		
		self._players_df = pd.DataFrame(players_json)
		self._prepare_data()

	def _prepare_data(self):

		df = self._players_df
		df['name'] = df['first_name'] + ' ' + df['second_name']
		df['now_cost'] = df['now_cost'] / 10

		column_list = ['name','team','id','element_type',
            'selected_by_percent','now_cost','goals_scored',
               'assists','clean_sheets','bonus','total_points']

		self._players_df = df[column_list]

		return None

	def get_players_stats(self):

		return self._players_df