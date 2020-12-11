from Results import Results
from APIConnector import APIConnector
from GameweekStats import GameweekStats
from Teams import Teams

import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app(app):

	results_obj = Results()
	api_connector = APIConnector()
	gameweek_stats = GameweekStats(api_connector.get_events_gameweeks())
	team_info = Teams(api_connector.get_teams_information())

	team_df = team_info.return_dataframe_obj()
	results_obj.map_teams(team_df)

	future_opp_score_df = results_obj.get_future_opponents_stats(gameweek_stats.current_gameweek_number())

	fig = go.Figure(go.Bar(
            x=future_opp_score_df['difficulty'],
            y=future_opp_score_df['team'],
            orientation='h'))

	fig.update_layout(
		title="Average FDR for teams (Next 4 matches)",
		height = 700
	)

	fig.update_xaxes(
		title_text = "Average FDR",
        tickangle = 45,
        title_standoff = 25
	)

	app.layout = html.Div([
		dcc.Graph(id='fdr-display',figure=fig)
	])

if __name__ == '__main__':

	app = dash.Dash()

	initialize_app(app)

	app.run_server(debug=True)

