####################################################################################################
##                                                                                                ##
##                            BATTERY TESTER                                                      ##
##                                                                                                ##
## Description: plot data in real time, and view last result                                      ##
##                                                                                                ##
##  Author: Blanca Cano camarero                                                                  ##
##  Last modification date : 24-07-2018                                                           ##
##                                                                                                ##
####################################################################################################

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
import time
import io
import os

import random as rd
import subprocess as shell
from collections import deque
#My imports
import my_csv

####################### global variables #############################

START_TIME = time.time()
LENGTH = 50 # length data axies
TIME = 1 #time in seconds

TEST = ''
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

app.config['suppress_callback_exceptions']=True

###########################################  APPS  ######################################################
#index app
app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    dcc.Link('View data.cvs', href='/view'),
    html.Br(),
    dcc.Link('Tests selection', href='/test'),

    # content will be rendered in this element, depend of test_app and charge_app
    html.Div(id='page-content')
])

#aplication of test selection
test_app = html.Div( [

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
        ),
    html.Div(dcc.Input(id='input-box', type='text')),
    html.Div([
        html.Button('Save', id='button' , n_clicks = 0 ),
        html.Div(id='output-container-button',
                 children='Enter a name and press Save'),
        html.Button('Remove not save data', id='rm_button'),
        html.Div( id = 'last_reset' , children = 'Las reset: never')
        ])
])

## layout to view a file
charge_app =  html.Div([
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
        multiple=False
    ),
    html.Div([
        html.H3('voltage , current and capacity'),
        dcc.Graph(id='graph_update_file')
        ], className="vc"),

])
######################################## CALLBACKS ########################################

### INDEX CALLBACK
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    """ Update web page depending of the path name
"""
    
    if (pathname == '/view'):
        return  charge_app
    else:
        return test_app
    

### FILE CHARGE CALLBACK
    
@app.callback(Output('graph_update_file', 'figure'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])

def update_output(contents, list_of_names):
    """ Plot a csv file which contains charge, time , current and capacity in this order
"""
    print('PLOTTING GRAPHS')
    content_type, content_string = contents.split(',')

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

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})



### TEST SELECTION CALLBACK
def update_data(data,test):
    """update data of a particular test
"""
    if test != 7:
        data['time'].append(time.time() - START_TIME)
        for i in PARAMETERS:
            # add here comunication
            data[test][i].append( rd.randrange(MIN_Y ,MAX_Y) )
            #sabe data
            my_csv.save_csv( '.'+test,[ data['time'] , data[test]['voltage'] , data[test]['current'] , data[test]['capacity']  ] )
    return data

### graph update
@app.callback(
    dash.dependencies.Output('graph_update','figure'),
    [Input('dropdown', 'value')],
    events=[Event('graph-update', 'interval')]
    )
def update_graph( test ):
    """
    create three graphs
"""
    global TEST
    TEST = test
    update_data( data , test )
    fig = tools.make_subplots(rows=1, cols=3,# specs=[[{}]],
                          shared_xaxes=False, shared_yaxes=False,
                          vertical_spacing=1)
    if test != 7:
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
### save,button update

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, text):
    """
save actual .actual test 
"""

    if TEST != '':
        new_name =  my_csv.give_name(text)
        cp_name = '.'+TEST+'.csv'
        shell.call([ 'cp' , '.'+ TEST + '.csv' , new_name])
        return f'{TEST} saved in {new_name}'
    else:
        return 'Write file name and save'

@app.callback(
    dash.dependencies.Output('last_reset', 'children'),
    [dash.dependencies.Input('rm_button', 'n_clicks')]
    )
def rm_data(n):
    """
Remove not save data
"""
    for i in range(1,8):
        shell.call(['rm',f'.Test{i}.csv'])
    full_date = shell.call(['date'])
    
    return f"You have reset it {n} times "


######################################## main ########################################
if __name__ == '__main__':
    app.run_server(debug=True)
