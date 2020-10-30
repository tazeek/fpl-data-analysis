import pandas as pd
import requests

class Teams:

	def __init__(self, json_file):

		self.team_info_df =  pd.DataFrame(json_file)