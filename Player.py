import pandas as pd

class Player:

	def __init__(self, players_json, player_type):
		
		self.players_df = pd.DataFrame(players_json)
		self.players_types_df = pd.DataFrame(player_type)