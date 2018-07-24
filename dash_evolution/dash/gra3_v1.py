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
from dash.dependencies import Input, Output , Event

# import csv
import pandas as pd
import csv

# plot dessing
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

import base64
import datetime
import io
import os
#open data file, columns' mean  votage,current,time,capacity
 


# Start graphs 
app = dash.Dash()
app.layout = html.Div([
       dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '80%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div([
        html.H3('voltage , current and capacity'),
        dcc.Graph(id='graph_update')
        ], className="vc"),

])

@app.callback(Output('graph_update', 'figure'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])

def update_output(contents, list_of_names):

    content_type, content_string = contents[0].split(',')

    decoded = base64.b64decode(content_string)
    df = pd.read_csv(
        io.StringIO(decoded.decode('utf-8')))
    print (type(df))
    #procedo a converit el archivo 
    df.to_csv('.pandas.csv', header=None, index=None, sep=',', mode='w')
    print ('archivo pandas creado')

    # dibujo figura
    df = pd.read_csv('.pandas.csv' , header=None)



    # Get values grahp
    voltage = go.Scatter(
        y = df[0],
        x = df[2],
        name = 'voltage'
    )
    current = go.Scatter(
        y = df[1],
        x = df[2],
        name = 'current'
    )
    
    capacity = go.Scatter(
        y=df [3],
        x=df [2],
        name = 'capacity'
    )

    ## Current , voltage and capacity
    fig = tools.make_subplots(rows=1, cols=3,
                              shared_xaxes=False, shared_yaxes=False,
                              vertical_spacing=100)
    fig.append_trace(voltage, 1, 1)
    fig.append_trace(current, 1, 2)
    fig.append_trace(capacity ,  1, 3)

    
    fig['layout'].update(height=600, width=1000, title='voltage, current and capacity')
    return fig


# style 
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

#######
if __name__ == '__main__':
    app.run_server(debug=True)
