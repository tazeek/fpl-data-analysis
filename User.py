import pandas as pd
import requests

class User:

	def __init__(self, id):

		self.fpl_id = id

	def fetch_current_squad(self):

		url = f"https://fantasy.premierleague.com/api/my-team/{self.fpl_id}/"
		r = requests.get(url)

		return r