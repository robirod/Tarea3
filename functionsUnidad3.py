import pandas as pd
import joblib

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
    
# Crea archivo persistente PKL
def createPkl(path, dataframe):
    if path != '' and len(dataframe) > 0:
        path = path + ".pkl"
        # compress=3 optimiza el peso del archivo sin perder rendimiento
        joblib.dump(dataframe, path, compress=3)
        return True
    else:
        return False

# Importa archivo persistente PKL
def importPkl(path):
    if path != '':
        path = path + ".pkl"
        return joblib.load(path)
    else:
        return False