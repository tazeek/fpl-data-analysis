import pandas as pd
import numpy as np
import requests

class Results:

	def __init__(self):

		url = 'https://fantasy.premierleague.com/api/fixtures/'
		r = requests.get(url)

		self.results_matches_df =  pd.DataFrame(r.json())

	def drop_columns(self, drop_columns):

		self.results_matches_df = self.results_matches_df.drop(drop_columns, axis=1)

	def map_teams(self,team_df):

		my_df = self.results_matches_df
		team_names = team_df.set_index('id').name

		my_df['team_a'] = my_df.team_a.map(team_names)
		my_df['team_h'] = my_df.team_h.map(team_names)

		self.results_matches_df = my_df

	def _filter_unplayed_matches(self):

		my_df = self.results_matches_df

		return my_df[my_df.finished==True]

	def prepare_goal_stats(self):

		goals_df = self.results_matches_df[['event','team_h_score','team_a_score']].copy()
		goals_df.dropna(inplace=True)

		# Sum up: home goals, away goals
		goals_df = goals_df.groupby(['event']).sum()

		return goals_df