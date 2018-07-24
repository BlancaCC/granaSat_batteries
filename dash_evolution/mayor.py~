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

#time update libraries
from dash.dependencies import Input, Output 
import datetime

#
import random as rd
import subprocess as shell

#My imports
import my_csv

# global variables
global TEST, file_name, save_file
TEST = 0
file_name = None
save_file = False

LENGHT = 15 #number of elements to be representates at maximun
SAVE_LENGHT = 15
data = {
    'y' : [0],
    'x' : [0]
}
pass_interval = 0

TIME = 0.5 # time of refresh in seconds


# Starting interfaz
app = dash.Dash(__name__)

option = [ ' Test 1	High Vacuum test',
           ' Test 2	Capacity and Internal Resistance vs Temperature',
           ' Test 3	Self-Discharge Test',
           ' Test 4	LEO Cycling',
           ' Test 5	EMF vs SOC',
           ' Test 6	Reduced pressure 30 % DOD Cycling',
           ' Test 7	Reduced pressure 80% DOD Cycling' ]

app.layout = html.Div( [

    # Head
    html.H1( 'Batteries Tests'),
    
    # Selection test panel
    html.Label ('Please select a test'), 
    dcc.Dropdown(
        options=[ {'label': option[i] , 'value': str(i)} for i in range(len(option)) ],
        id = 'dropdown',
        value=len(option)
    ),
    dcc.Graph(
        id = 'graph'
        ),
    dcc.Interval(
            id = 'interval',
            interval = TIME*1000, # work in milliseconds
            n_intervals = 0
        )
])





@app.callback(
   Output('graph', 'figure'),
   [Input('dropdown', 'value'), Input('interval', 'n_intervals')],
)
def update_graph(test , n ):
   """
   update graph in time and dropdown 
"""
   #ADD MORE FIGURES FOR MORE GRAPHICS
   fig = plotly.tools.make_subplots()
   
   if test != TEST:
      # callback input was value, so has changed test type
      print(f'FILNAME {file_name}')
      TEST = test
      if file_name != None and save_file == False:
         shell.run(['rm', file_name])
         file_name = 'T'+str(TEST)+'csv'
         data['y'] = []
         data['x'] = []
      
   if pass_interval != n:
      new_data = rd.uniform(-10*TEST,10*TEST) #get_data_from_test
      pass_interval = n
   
      if n > LENGHT:
         data['y'] = data['y'][1:]+[new_data]
         data['x'] = list (map (lambda x: x+1 , data['x']) )
         
         # all data are new, so save into the cvs file
      if n % SAVE_LENGHT == 0:
         my_csv.save_csv( file_name , [ data['x'] , data['y'] ] )
         print ("Updating in data.cvs")
      else:
         data['x'].append(new_data)

   fig.append_trace({
      'x': data['x'],
      'y': data['y'],
      'type': 'scatter'
   }, 1, 1)

   return fig

    
   
if __name__ == '__main__':
   app.run_server(debug=True)
