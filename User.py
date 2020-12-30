import pandas as pd
import requests

class User:

	def __init__(self, id, email, password):

		self._fpl_id = id
		self._email = email
		self._password = password
		self._session = None

		self._login()

	def fetch_current_squad(self):

		url = f"https://fantasy.premierleague.com/api/my-team/{self._fpl_id}/"
		r = self._session.get(url)

		return r

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