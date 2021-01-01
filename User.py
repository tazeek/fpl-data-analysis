import pandas as pd
import requests

class User:

	def __init__(self, id, email, password):

		self._fpl_id = id
		self._email = email
		self._password = password
		self._session = None

		self._squad_df = None

		self._login()

	def fetch_current_squad(self, player_info_df):

		if self._squad_df is None:

			url = f"https://fantasy.premierleague.com/api/my-team/{self._fpl_id}/"
			response = self._session.get(url)

			if response.status_code != 200:
				return { 'error' : 'Failed to fetch squad. Please try again later' }

			squad = response.json()['picks']
			squad_df = pd.DataFrame(squad)

			squad_df.set_index('element',inplace=True)
			player_info_df.set_index('id',inplace=True)

			squad_df = pd.merge(squad_df, player_info_df, left_index=True, right_index=True)
			squad_df.reset_index(drop=True,inplace=True)

			column_list = ['name','selected_by_percent','now_cost',
				'goals_scored','assists','clean_sheets', 'bonus', 'total_points']

			self._squad_df = squad_df[column_list]

		return {'squad' : self._squad_df }

	def _login(self):

		self._session = requests.session()

		url = 'https://users.premierleague.com/accounts/login/'

		payload = {
		 	'password': self._password,
			'login': self._email,
			'redirect_uri': 'https://fantasy.premierleague.com/a/login',
			'app': 'plfpl-web'
		}

		self._session.post(url, data=payload)

		return None