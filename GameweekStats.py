import pandas as pd
import numpy as np

class GameweekStats:

	def __init__(self, json_file, filtered_columns):

		self.events_df = pd.DataFrame(json_file)
		self.events_df = self.events_df[filtered_columns]


	def filter(self):

		# We only want data till the current gameweek
		index_num = self.events_df[self.events_df['is_current']==True].index.values

		# The slicing will be done one gameweek less; hence, the "+1" is needed
		self.events_df = self.events_df.iloc[: index_num[0] + 1]

	def fetch_scores(self):

		# Fetch the highest and average scores of the week
		return self.events_df[['id','average_entry_score','highest_score']]
