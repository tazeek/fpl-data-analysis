import pandas as pd

class Player:

	def __init__(self, players_json):
		
		self._players_df = pd.DataFrame(players_json)

	def _prepare_data(self):

		df = self._players_df
		df['name'] = player_info_df['first_name'] + ' ' + player_info_df['second_name']
		df['now_cost'] = player_info_df['now_cost'] / 10

		column_list = ['name','team','id','element_type',
            'selected_by_percent','now_cost','goals_scored',
               'assists','clean_sheets','bonus','total_points']

		self._players_df = df[column_list]

		return None