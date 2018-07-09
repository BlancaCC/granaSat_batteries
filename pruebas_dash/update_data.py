import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import random


app = dash.Dash(__name__)

app.layout = html.Div(
    html.Div([
    html.H3("Grafiquillo extremadamente serio")
        html.Div( id = 'life_update_text')
        dcc.Graph( id = 'life-update-graph')
        dcc.interval(
            id = 'interval',
            interval = 1*1000, # work in milliseconds
            n_intervals = 0
        )
    ])
)

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval', 'n_intervals')])
def update_graph(n):
    fig =  plotly.tools.make_subplots()
    


if __name__ == '__main__':
    app.run_server(debug=True)
