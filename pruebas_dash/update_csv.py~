import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import random as rd

import my_csv


LENGHT = 15 #number of elements to be representates at maximun
data = {
    'y' : [ rd.uniform(-10 , 10) for i in range(LENGHT)],
    'x' : list( range(LENGHT))
}

app = dash.Dash(__name__)

app.layout = html.Div(
    html.Div([
        html.H3("Grafiquillo extremadamente serio"),
        html.Div( id = 'life_update_text'),
        dcc.Graph( id = 'life-update-graph'),
        dcc.Interval(
            id = 'interval',
            interval = 1*100, # work in milliseconds
            n_intervals = 0
        )
    ])
)

@app.callback(Output('life-update-graph', 'figure'), [Input('interval', 'n_intervals')])
def update_graph(n):
    fig =  plotly.tools.make_subplots()
    new_data = rd.uniform(-10,10)
    if n > LENGHT:
        data['y'] = data['y'][1:]+[new_data]
        data['x'] = list (map (lambda x: x+1 , data['x']) )
        
        # all data are new, so save into the cvs file
        if n % LENGHT == 0:
            my_csv.save_csv( "data.cvs" , [ data['x'] , data['y'] ] )
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
