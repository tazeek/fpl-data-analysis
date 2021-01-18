from Graphs import Graphs

import dash_core_components as dcc
import dash_html_components as html

def generate_layout():

	graphs_obj = Graphs()

	try:
	    graphs_obj = Graphs()
	except:
	    return html.Div([
	    	html.H4(id='error-requests', children='Failed to load data. Please refresh again later.')
	    ])

	team_form = graphs_obj.get_info_about_teams_form()

	return html.Div([
		dcc.Graph(id='fdr-display',figure=graphs_obj.get_future_fdr_scores_fig()),
		dcc.Graph(id='show-all-chips',figure=graphs_obj.get_chips_stats_fig()),
		dcc.Graph(id='fpl-scores-stats',figure=graphs_obj.get_fpl_scores_stats()),
		dcc.Graph(id='fpl-transfers-stats',figure=graphs_obj.get_transfers_stats()),
		dcc.Graph(id='team-involvements-prev',figure=team_form['goals_scored_concded_fig']),
		dcc.Graph(id='clean-sheet-involvements',figure=team_form['clean_sheets_fig']),
		dcc.Graph(id='goals-scored-fig',figure=graphs_obj.get_goals_scored_stats_fig()),
		dcc.Graph(id='clean-sheet-stats',figure=graphs_obj.get_clean_sheets_stats_fig())
	])