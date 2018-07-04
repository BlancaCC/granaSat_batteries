# Make a graph basic in a .cvs
# Author: Blanca Cano Camarero
# File : grafico1.py

# fuente de inspiración:
# https://github.com/plotly/dash-core-components/pull/74
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

#open data file
df = pd.read_csv('df.cvs')

# basic class app
app = dash.Dash()

app.layout = html.Div
(
    [
        
        dcc.Graph
        (
            id = 'graph_csv',
            figure =
            {
                'data':[
                    { 'x':df['time'] , 'y':df['current'] , 'type':'scatter'},
                    ],
                'layout':{ 'title': 'Current'}
            }
        )
    ]
)

def dates ():
    print(df['time'])

if __name__ == "__main__":
    dates()
    app.run_server()

    
