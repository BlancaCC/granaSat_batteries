"""

file: csv_save 
author: Blanca Cano

"""
import csv
import subprocess as shell

def save_csv(fname , column ):
    """
@brief: save x and i in the file fname.csv
@param fname: file's fname, if it does not finish in .csv the funcion would add it
@param column: list of list fo columns
"""
    if True : #test if name is None
    # renaming with correct extension
        if fname[ -4: ]!= '.csv':
            if fname.find('.') > -1:
                fname = fname[: fname.find('.')]+'.csv'
            else:
                fname += '.csv'

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
    
    
                         
            
