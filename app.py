from Results import Results
from APIConnector import APIConnector
from GameweekStats import GameweekStats
from Teams import Teams

from Graphs import Graphs

import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

graphs_obj = Graphs()

app = dash.Dash()
server = app.server

app.layout = html.Div([
	dcc.Graph(id='fdr-display',figure=graphs_obj.get_future_fdr_scores_fig()),
	dcc.Graph(id='show-all-chips',figure=graphs_obj.get_chips_stats_fig()),
	dcc.Graph(id='fpl-scores-stats',figure=graphs_obj.get_fpl_scores_stats()),
	dcc.Graph(id='fpl-transfers-stats',figure=graphs_obj.get_transfers_stats()),
	dcc.Graph(id='goals-scored-fig',figure=graphs_obj.get_goals_scored_stats_fig()),
	dcc.Graph(id='clean-sheet-stats',figure=graphs_obj.get_clean_sheets_stats_fig())
])

if __name__ == '__main__':

	app.run_server(debug=True)

