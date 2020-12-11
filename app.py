from Results import Results
from APIConnector import APIConnector
from GameweekStats import GameweekStats
from Teams import Teams

import dash
import dash_core_components as dcc
import dash_html_components as html

results_obj = Results()
api_connector = APIConnector()
gameweek_stats = GameweekStats(api_connector.get_events_gameweeks())

future_opp_score_df = results_obj.get_future_opponents_stats(gameweek_stats.current_gameweek_number())