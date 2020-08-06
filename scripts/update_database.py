import pymongo
from info import getClient

import glob
import pandas as pd
import sys
sys.path.append("../")

client = pymongo.MongoClient(getClient())
mydb = client['covid19-forecast']
mycol = mydb['all_forecasts']
files = glob.glob("../forecasts_processed/all/*.csv")

models_list = []
for file in files:
    df = pd.read_csv(file)
    if df.empty == True:
        continue
    
    last_slash = file.rfind('/')
    filetype = file.find('.csv')
    model_name = file[last_slash + 1 : filetype]

    df = df.drop_duplicates(subset=['target_end_date', 'location'], keep='last')
    df = df.loc[(df['target'].str.contains("wk"))]

    df.astype({'value': 'float', 'quantile': 'float'}).dtypes

    df = df.groupby('location')

    for name, group in df:
        if name != 'US':
            location = int(name) 
        else:
            location = name
        targets = list(group['target'].array)
        forecast_date = list(group['forecast_date'].array)
        target_dates = list(group['target_end_date'].array)
        values = list(group['value'].array)
        values = [float(value) for value in values]
        types = list(group['type'].array)
        quantiles = list(group['quantile'].array)
        quantiles = [float(quantile) for quantile in quantiles]

        # Inserting documents
        model_dict = {'model': model_name, 
                  'location': location, 
                  'target': targets,
                  'type': types,
                  'quantile': quantiles,
                  'forecast_date': forecast_date,
                  'target_end_date': target_dates,
                  'value': values}

        x = mycol.insert_one(model_dict)

    print(model_name)
