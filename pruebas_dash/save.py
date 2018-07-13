def update_graph(n , TEST):
   """
   update graph in time and dropdown 
"""
   #ADD MORE FIGURES FOR MORE GRAPHICS
   fig = plotly.tools.make_subplots()
   
   if type(n) == str: # callback input was value, so has changed test type
      n = int (n)
      #if they have selected another TEST
      if TEST != n:
         TEST = n
         if file_name and save_file == False:
            shell.run(['rm', file_name])
            file_name = 'T'+str(TEST)+'csv'
            data['y'] = []
            data['x'] = []
      
   else: # time 
      if pass_interval != n_intervals:
         new_data = rd.uniform(-10*TEST,10*TEST) #get_data_from_test
   
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
