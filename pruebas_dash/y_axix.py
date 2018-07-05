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
capacity = go.Scatter(
    y=df [3],  # It's not capacity 
    x=df [0],
    name = 'capacity'
 )

## Capacity
fig2 = tools.make_subplots()
fig2.append_trace(capacity , 1 , 1)

fig2['layout'].update(height=600, width=600, title='capacity')

# Start graphs 
app = dash.Dash()
app.layout = html.Div([

    html.Div([
        html.H3('capacity'),
        dcc.Graph( figure=fig2 , id='capacity')
    ], className="c")
])
figure['layout']['shapes'] = [dict({
                'x0': [1,2,3]
                'x1': [1,2,3]
                'y0': [2,3,4]
                'y1': [1,2,3]
            }, **shape)]

# style 
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

#######
if __name__ == '__main__':
    app.run_server(debug=True)
