import pandas as pd

class Player:

	def __init__(self, players_json):
		
		self._players_df = pd.DataFrame(players_json)

	def _prepare_data(self):

		df = self._players_df
		df['name'] = player_info_df['first_name'] + ' ' + player_info_df['second_name']
		df['now_cost'] = player_info_df['now_cost'] / 10

		self._players_df = df[['name','team','id','element_type','selected_by_percent','now_cost','minutes','total_points']]