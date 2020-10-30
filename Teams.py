import pandas as pd
import requests

class Teams:

	def __init__(self, json_file):

		self.team_info_df =  pd.DataFrame(json_file)

	def filter_columns(self, filter_columns):

		self.team_info_df = self.team_info_df[filter_columns]

	def return_dataframe_obj(self):
		return self.team_info_df