# -*- coding: utf-8 -*-
# First graphic
# Author Blanca Cano
# fuente de inspiración:
## para múltiples fuentes
## https://plot.ly/python/multiple-axes/
## Gráficas paralelas


# Basic dash library
import dash
import dash_core_components as dcc
import dash_html_components as html
# import csv
import pandas as pd

# plot dessing
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

#open data file, columns' mean  votage,current,time,capacity
 
df = pd.read_csv('df.csv' , header=None)



# Get values grahp
voltage = go.Scatter(
    y = df[0],
    x = df [2],
    name = 'voltage'
)
current = go.Scatter(
    y = df[1],
    x = df [2],
    name = 'current'
)

capacity = go.Scatter(
    y=df [3],
    x=df [2],
    name = 'capacity'
 )

## Current and voltage 
fig = tools.make_subplots(rows=2, cols=1, specs=[[{}], [{}]],
                          shared_xaxes=True, shared_yaxes=False,
                          vertical_spacing=0.001)
fig.append_trace(voltage, 1, 1)
fig.append_trace(current, 2, 1)

## Capacity
fig2 = tools.make_subplots()
fig2.append_trace(capacity , 1 , 1)

fig['layout'].update(height=600, width=600, title='voltage and current')
fig2['layout'].update(height=600, width=600, title='capacity')

# Start graphs 
app = dash.Dash()
app.layout = html.Div([
    html.Div([
        html.H3('voltage_current'),
        dcc.Graph(figure=fig, id='voltage_current')
        ], className="vc"),

    html.Div([
        html.H3('capacity'),
        dcc.Graph( figure=fig2 , id='capacity')
    ], className="c")
])


# style 
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

#######
if __name__ == '__main__':
    app.run_server(debug=True)
