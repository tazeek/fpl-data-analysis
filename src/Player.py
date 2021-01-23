import pandas as pd

class Player:

	def __init__(self, players_json):
		
		self._players_df = pd.DataFrame(players_json)
		self._prepare_data()

	def _prepare_data(self):

		df = self._players_df
		df['name'] = df['first_name'] + ' ' + df['second_name']
		df['now_cost'] = df['now_cost'] / 10
		df['selected_by_percent'] = df['selected_by_percent'].astype('float')

		column_list = ['name','team','id','element_type',
            'selected_by_percent','now_cost','goals_scored',
               'assists','clean_sheets','bonus','total_points']

		self._players_df = df[column_list]

		return None

	def get_players_stats(self):

		return self._players_df

	def get_player_names(self):

		return self._players_df[['name','id']].copy()

	def get_popular_players(self, count):

		players_df = self._players_df[['name','selected_by_percent']].copy()
		players_df.sort_values('selected_by_percent',ascending=False,inplace=True)

		return players_df.head(count)

