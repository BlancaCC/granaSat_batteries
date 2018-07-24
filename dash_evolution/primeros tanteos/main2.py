"""
@brief: dropdown interfaz  
@file: dropdpwn.py   
@author: Blanca Cano   
"""

# -*- coding: utf-8 -*-
# Dash basic libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go

#time update libraries
from dash.dependencies import Input, Output , Event
import datetime
import time

#
import random as rd
import subprocess as shell
from collections import deque
#My imports
import my_csv


####################### global variables #############################


LENGTH = 50 # length data axies
TIME = 3 #time in seconds

MIN_Y = -10
MAX_Y = 10

PARAMETERS = ['voltage' , 'current' , 'capacity']

option = [ ' Test 1	High Vacuum test',
           ' Test 2	Capacity and Internal Resistance vs Temperature',
           ' Test 3	Self-Discharge Test',
           ' Test 4	LEO Cycling',
           ' Test 5	EMF vs SOC',
           ' Test 6	Reduced pressure 30 % DOD Cycling',
           ' Test 7	Reduced pressure 80% DOD Cycling' ]

data = {
   'Test'+str(i+1):{ j: deque(maxlen=LENGTH) for j in PARAMETERS} for i in range(len(option))
   }
data.update( { 'time' : deque (maxlen=LENGTH ) } )
 
###################################################
def div_graph ( name ):
    """
    Generate an html graphs
"""
    return html.Div([
        html.H4(name),
        dcc.Graph(id=name)
        ])
    


app = dash.Dash( 'Battery_testter')

app.layout = html.Div( [

    # Head
    html.H1( 'Batteries Tests'),
    
    # Selection test panel
    html.Label ('Please select a test'), 
    dcc.Dropdown(
        options=[ { 'label': option[i] , 'value':'Test'+str(i+1) } for i in range(len(option)) ],
        id = 'dropdown',
        value=len(option)
    ),
    dcc.Graph (id= 'graph_update'),
    dcc.Interval(
            id = 'graph-update',
            interval = TIME*1000, # work in milliseconds
            n_intervals = 0
        )
])

def update_data(data,test):
    """update data of a particular test
"""
    data['time'].append(time.time())
    for i in PARAMETERS:
        # add here comunication
        data[test][i].append( rd.randrange(MIN_Y ,MAX_Y) )
    #sabe data
    my_csv.save_csv(test ,[ data['time'] , data[test]['voltage'] , data[test]['current'] , data[test]['capacity']  ] )
    return data


@app.callback(
    dash.dependencies.Output('graph_update','figure'),
    [Input('dropdown', 'value')],
    events=[Event('graph-update', 'interval')]
    )
def update_graph (test):
    """
update graph
    """

    update_data(data,test)
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=3)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    for i in range( len( PARAMETERS) ):
        fig.append_trace({
            'x': list(data['time']),
            'y': list( data[test][PARAMETERS[i]])
            }, 1, i)
        
    return fig

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']

for js in external_css:
    app.scripts.append_script({'external_url': js})
if __name__ == '__main__':
    app.run_server(debug = True)



