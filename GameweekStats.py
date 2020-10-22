import pandas as pd
import numpy as np

class GameweekStats:

	def __init__(self, json_file, filtered_columns):

		self.events_df = pd.DataFrame(json_file)
		self.events_df = self.events_df[filtered_columns]