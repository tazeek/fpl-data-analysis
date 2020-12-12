from Results import Results
from APIConnector import APIConnector
from GameweekStats import GameweekStats
from Teams import Teams

from Graphs import Graphs

import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app(app):

	graphs_obj = Graphs()

	results_obj = Results()
	api_connector = APIConnector()
	gameweek_stats = GameweekStats(api_connector.get_events_gameweeks())
	team_info = Teams(api_connector.get_teams_information())

	team_df = team_info.return_dataframe_obj()
	results_obj.map_teams(team_df)

	chips_fig = go.Figure()

	chip_stats_df = gameweek_stats.fetch_chip_stats()
	total_gameweeks_played = gameweek_stats.total_gameweeks()
	x_values = [i for i in range(1, total_gameweeks_played + 1)]

	chip_stats_df.rename(
		columns = {
		'bboost':'bench_boost', 
		'3xc':'triple_captain'
		},
		inplace = True
	)

	for column in chip_stats_df.columns:

		chips_fig.add_trace(go.Scatter(x=x_values, y=chip_stats_df[column],
			mode='lines+markers',
			name=column))

	chips_fig.update_layout(
		title="Number of chips played per gameweek",
		hovermode='x unified',
		yaxis_tickformat='k'
	)

	chips_fig.update_xaxes(
		title_text = "Gameweek",
		tickangle = 45,
		nticks = total_gameweeks_played + 1,
		title_standoff = 25
	)

	chips_fig.update_yaxes(
		title_text = "Total",
		title_standoff = 25
	)

	app.layout = html.Div([
		dcc.Graph(id='fdr-display',figure=graphs_obj.get_future_fdr_scores()),
		dcc.Graph(id='show-all-chips',figure=chips_fig)
	])

if __name__ == '__main__':

	app = dash.Dash()

	initialize_app(app)

	app.run_server(debug=True)

