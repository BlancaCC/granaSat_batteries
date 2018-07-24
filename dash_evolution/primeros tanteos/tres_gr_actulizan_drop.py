# -*- coding: utf-8 -*-
# Dash basic libraries
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools


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

START_TIME = time.time()
LENGTH = 50 # length data axies
TIME = 1 #time in seconds

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



######################################### Start graphs  ##################################################
app = dash.Dash()

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


##################################### funcion ###############################################################
def update_data(data,test):
    """update data of a particular test
"""
    data['time'].append(time.time() - START_TIME)
    for i in PARAMETERS:
        # add here comunication
        data[test][i].append( rd.randrange(MIN_Y ,MAX_Y) )
    #sabe data
    my_csv.save_csv( '.'+test,[ data['time'] , data[test]['voltage'] , data[test]['current'] , data[test]['capacity']  ] )
    return data


@app.callback(
    dash.dependencies.Output('graph_update','figure'),
    [Input('dropdown', 'value')],
    events=[Event('graph-update', 'interval')]
    )
def update_graph( test ):
    update_data( data , test )
    fig = tools.make_subplots(rows=1, cols=3,# specs=[[{}]],
                          shared_xaxes=False, shared_yaxes=False,
                          vertical_spacing=1)
    # Get values grahp
    col = 1
    for i in PARAMETERS:
       fig.append_trace( go.Scatter(
           y = list( data[test][i]),
           x = list(data['time']),
           name = i,
          )
                         , 1, col)
       col += 1
  
    fig['layout'].update(title= f' {PARAMETERS[0]} {PARAMETERS[1]} and {PARAMETERS[2]} ')

    return fig 



# style 
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

#######
if __name__ == '__main__':
    app.run_server(debug=True)


