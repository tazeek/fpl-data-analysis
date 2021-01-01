from layout import generate_layout

import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
server = app.server

app.layout = generate_layout()

if __name__ == '__main__':

	app.run_server(debug=True)

