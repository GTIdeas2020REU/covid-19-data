import pymongo
from info import getClient

import glob
import pandas as pd
import sys
sys.path.append("../")

client = pymongo.MongoClient(getClient())
mydb = client['covid19-forecast']
mycol = mydb['point_forecasts']
files = glob.glob("../forecasts_processed/point/*.csv")

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

    #df.astype({'quantile': 'float', 'value': 'float'}).dtypes
    df.astype({'value': 'float'}).dtypes

    locations = list(df['location'].array)
    locations = [int(loc) for loc in locations if loc != 'US']
    targets = list(df['target'].array)
    #types = list(df['type'].array)
    #quantiles = list(df['quantile'].array)
    #quantiles = [float(quantile) for quantile in quantiles]
    #forecast_date = df['forecast_date'].array[0]
    forecast_date = list(df['forecast_date'].array)
    target_dates = list(df['target_end_date'].array)
    values = list(df['value'].array)
    values = [float(value) for value in values]
    print(model_name)

    # For now only inserting documents with point forecasts
    model_dict = {'model': model_name, 
                  'location': locations, 
                  'target': targets,
                  #'type': types,
                  #'quantile': quantiles,
                  'forecast_date': forecast_date,
                  'target_end_date': target_dates,
                  'value': values}

    x = mycol.insert_one(model_dict)

    #models_list.append(model_dict)

#x = mycol.insert_many(models_list)