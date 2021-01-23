import pandas as pd
import numpy as np

class GameweekStats:

	def __init__(self, json_file):

		self.events_df = pd.DataFrame(json_file)

		useful_columns = ['id','average_entry_score','highest_score','chip_plays','most_selected',
		'most_transferred_in','top_element','top_element_info','transfers_made',
		'most_captained','most_vice_captained','is_current']

		self._current_gameweek = self._find_current_gameweek()
		self._filter(useful_columns)

	def _find_current_gameweek(self):
		
		index_num = self.events_df[self.events_df['is_current']==True].index.values
		return int(index_num[0] + 1)

	def _filter(self, filtered_columns):

		# Keep the columns that are only needed
		self.events_df = self.events_df[filtered_columns]

		# The slicing will be done one gameweek less
		self.events_df = self.events_df[: self._current_gameweek]

		return None

	def get_current_gameweek(self):
		return self._current_gameweek

	def fetch_scores(self):

		# Fetch the highest and average scores of the week
		return self.events_df[['id','average_entry_score','highest_score']].copy()

	def fetch_chip_stats(self):

		# Return all the chip statistics played every gameweek
		chip_stats_list = []

		for gameweek_chip_list in self.events_df['chip_plays']:

			chip_stats = {
				'bboost': 0,
				'3xc': 0,
				'wildcard': 0,
				'freehit': 0
			}

			for chip_info in gameweek_chip_list:
				chip_stats[chip_info['chip_name']] = chip_info['num_played']

			chip_stats_list.append(chip_stats)

		return pd.DataFrame(chip_stats_list)

	def fetch_transfers(self):
		return self.events_df[['id','transfers_made']].copy()
