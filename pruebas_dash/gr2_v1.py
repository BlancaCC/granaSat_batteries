# -*- coding: utf-8 -*-
# First graphic
# Author Blanca Cano
# fuente de inspiración:
# para múltiples fuentes
# https://plot.ly/python/multiple-axes/


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

#open data file
# columanas 
df = pd.read_csv('df.csv' , header=None)

#votage,current,time,capacity
app = dash.Dash()

# Get values 
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
    x=df [3],
    y=df [2],
    name = 'capacity'
)
fig = tools.make_subplots(rows=2, cols=1, specs=[[{}], [{}]],
                          shared_xaxes=True, shared_yaxes=True,
                          vertical_spacing=0.001)
fig.append_trace(voltage, 1, 1)
fig.append_trace(current, 2, 1)
#fig.appen_trace(capacity, 1 , 1)


fig['layout'].update(height=600, width=600, title='voltage and current')


app.layout = html.Div([
    dcc.Graph(figure=fig, id='my-figure')
])

if __name__ == '__main__':
    app.run_server(debug=True)
