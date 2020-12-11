from Results import Results
from APIConnector import APIConnector
from GameweekStats import GameweekStats
from Teams import Teams

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app(app):

	results_obj = Results()
	api_connector = APIConnector()
	gameweek_stats = GameweekStats(api_connector.get_events_gameweeks())

	future_opp_score_df = results_obj.get_future_opponents_stats(gameweek_stats.current_gameweek_number())

	fig = go.Figure(go.Bar(
            x=future_opp_score_df['difficulty'],
            y=future_opp_score_df['team'],
            orientation='h'))

	fig.update_layout(
		title="Average FDR for teams (Next 4 matches)"
	)

	fig.update_xaxes(
		title_text = "Average FDR",
        tickangle = 45,
        title_standoff = 25
	)

	fig.update_yaxes(
		title_text = "Teams",
	   title_standoff = 25
	)

if __name__ == '__main__':

	app = dash.Dash()

	initialize_app(app)

	app.run_server(debug=True)

