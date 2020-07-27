import pymongo
from info import getClient

import glob
import pandas as pd
import sys
sys.path.append("../")

client = pymongo.MongoClient(getClient())
mydb = client['covid19-forecast']
mycol = mydb['forecasts']
files = glob.glob("../forecasts_processed/*.csv")

models_list = []
for file in files:
    df = pd.read_csv(file)
    if df.empty == True:
        continue
    
    last_slash = file.rfind('/')
    filetype = file.find('.csv')
    model_name = file[last_slash + 1 : filetype]

    df.astype({'quantile': 'float', 'value': 'float'}).dtypes

    locations = list(df['location'].array)
    locations = [int(loc) for loc in locations if loc != 'US']
    targets = list(df['target'].array)
    types = list(df['type'].array)
    quantiles = list(df['quantile'].array)
    quantiles = [float(quantile) for quantile in quantiles]
    forecast_date = df['forecast_date'].array[0]
    target_dates = list(df['target_end_date'].array)
    values = list(df['value'].array)
    values = [float(value) for value in values]

    model_dict = {'model': model_name, 
                  'location': locations, 
                  'target': targets,
                  'type': types,
                  'quantile': quantiles,
                  'forecast_date': forecast_date,
                  'target_end_date': target_dates,
                  'value': values}

    models_list.append(model_dict)

x = mycol.insert_many(models_list)