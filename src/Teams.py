import pandas as pd
import requests

class Teams:

	def __init__(self, json_file):

		self.team_info_df =  pd.DataFrame(json_file)
		filter_columns = ['id','name','short_name']

		self._filter_columns(filter_columns)

	def _filter_columns(self, filter_columns):

		self.team_info_df = self.team_info_df[filter_columns]

	def return_dataframe_obj(self):
		return self.team_info_df