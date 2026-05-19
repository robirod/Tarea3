
import pandas as pd

#Importa lecturas de CSV
def importCsv(path):
    if path != '':
        path = path + ".csv"
        return pd.read_csv(path, sep=';', decimal=',')
    else:
        return False

#Crea CSV 
def createCsv(path, dataframe, columns):
    if path != '' and len(dataframe) > 0 and len(columns) > 0:
        path = path + ".csv"
        dataframe[columns].to_csv(path, index=False, sep=';', decimal=',')
        return True
    else:
        return False

