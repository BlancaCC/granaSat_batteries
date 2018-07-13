import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader.data import DataReader
import time
from collections import deque
import plotly.graph_objs as go
import random

app = dash.Dash('vehicle-data')

data_dict = {"Oil Temperature":oil_temps,
"Intake Temperature": intake_temps,
"Coolant Temperature": coolant_temps,
"RPM":rpms,
"Speed":speeds,
"Throttle Position":throttle_max}

pos_length = 50
times = deque(maxlen=max_length)
oil_temps = deque(maxlen=max_length)
intake_temps = deque(maxlen=max_length)
coolant_temps = deque(maxlen=max_length)
rpms = deque(maxlen=max_length)
speeds = deque(maxlen=max_length)
throttle_pos = deque(maxlen=max_length)


def update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos):

    times.append(time.time())
    if len(times) == 1:
        #starting relevant values
        oil_temps.append(random.randrange(180,230))
        intake_temps.append(random.randrange(95,115))
        coolant_temps.append(random.randrange(170,220))
        rpms.append(random.randrange(1000,9500))
        speeds.append(random.randrange(30,140))
        throttle_pos.append(random.randrange(10,90))
    else:
        for data_of_interest in [oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))

    return times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos

times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos = update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos)

app.layout = html.Div([
    html.Div([
        html.H2('Vehicle Data',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='vehicle-data-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Coolant Temperature','Oil Temperature','Intake Temperature'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=100),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})


@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('vehicle-data-name', 'value')],
    events=[dash.dependencies.Event('graph-update', 'interval')]
    )
def update_graph(data_names):
    graphs = []
    update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos)
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'


    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})


if __name__ == '__main__':
    app.run_server(debug=True)
#####################################################################

# global variables
#global TEST, file_name, save_file
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
