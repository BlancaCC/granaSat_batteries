"""

file: csv_save 
author: Blanca Cano

"""
import csv
import subprocess as shell

AUX_FILE = '.Test'
def give_name(fname):
    """
return name.csv
"""
    if fname[:len( AUX_FILE) ] != AUX_FILE: # hide file
    # renaming with correct extension
        if fname[ -4: ]!= '.csv':
            if fname.find('.') > -1:
                fname = fname[: fname.find('.')]+'.csv'
            else:
                fname += '.csv'
    else:
        fname += '.csv'
    return fname
    
def save_csv(fname , column ):
    """
@brief: save x and i in the file fname.csv
@param fname: file's fname, if it does not finish in .csv the funcion would add it
@param column: list of list fo columns
"""
    fname = give_name(fname)
    
    # write part
    with open( fname , 'a', newline = '\n' ) as csvfile:
        csv_file = csv.writer(csvfile , delimiter = ',')
        for line in zip (*column ):
            csv_file.writerow( line)
                        
        csvfile.close()

#tests 
if __name__ == '__main__':

    save_csv ('tomate.csv' , [[1 ,2 ,3] , [1 , 4 , 3]])
    save_csv ('tomate.txt' , [[1,4,5],[2,3,1]])
    save_csv('tomate',["abc","ola","aaa"])
    
    shell.run( ['cat','tomate.csv'] )
    shell.run( [ 'rm' , 'tomate.csv'])
    
    
                         
            
