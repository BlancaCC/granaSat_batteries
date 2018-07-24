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
   'Test'+str(i):{ j: deque(maxlen=LENGTH) for j in PARAMETERS} for i in range(len(option))
   }
data.update( { 'time' : deque (maxlen=LENGTH ) } )
 
###################################################
app = dash.Dash( 'Battery_testter')

app.layout = html.Div( [

    # Head
    html.H1( 'Batteries Tests'),
    
    # Selection test panel
    html.Label ('Please select a test'), 
    dcc.Dropdown(
        options=[ { 'label': option[i] , 'value':'Test'+str(i) } for i in range(len(option)) ],
        id = 'dropdown',
        value=len(option)
    ),
    html.Div( children=html.Div(id='graph'), className='row'),
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
    dash.dependencies.Output('graph','children'),
    [Input('dropdown', 'value')],
    events=[Event('graph-update', 'interval')]
    )
def update_graph (test):
    """
update graph
    """

    update_data(data,test)
    graphs = [1,2,3]
    class_choice = 'col s12 m6 l4'
        
    for i in range( len( PARAMETERS) ):
        data_g = go.Scatter(
            x=list(data['time']),
            y=list(data[test][ PARAMETERS[i] ]),
            name='Scatter',
            #fill="tozeroy",
            #fillcolor="#6897bb"
            )

        graphs[i]= html.Div(dcc.Graph(
            id=test,
            #animate=True,
            figure={'data': [data_g],
                    'layout' : go.Layout(xaxis=dict(range=[min(data['time']),max(data['time'])]),
                                                        yaxis=dict(range=[ MIN_Y , MAX_Y ] ),
                                                       margin={'l':50,'r':1,'t':45,'b':1},
                                        title='{}'.format(PARAMETERS[i])
                                         ,height = 600 , width = 600
                    ),
                   }
            ), className=class_choice) #para el append añadir paréntesis
    return graphs

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']

for js in external_css:
    app.scripts.append_script({'external_url': js})
if __name__ == '__main__':
    app.run_server(debug = True)



