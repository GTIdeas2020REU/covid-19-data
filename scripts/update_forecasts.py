from info import token

import github
import pandas as pd
from io import StringIO

g = github.Github(token())

# GT Ideas repo contents
myrepo = g.get_repo("GTIdeas2020REU/covid-19-data")
mycontents = myrepo.get_contents("")

# Get all CSV files from GT Ideas repo
mycsv_files = []
mycsv_names = []
while mycontents:
    myfile_content = mycontents.pop(0)
    if myfile_content.type == "dir":
        mycontents.extend(myrepo.get_contents(myfile_content.path))
    else:
        raw_url = myfile_content.download_url
        #print(myfile_content.name)
        if '.csv' in raw_url:
            mycsv_files.append(raw_url)
            mycsv_names.append(myfile_content.name)


#print(' ')
# Reichlab forecasts repo
repo = g.get_repo("reichlab/covid19-forecast-hub")
contents = repo.get_contents("data-processed")
#print(contents)

# Get all necessary files
csv_files = []
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        # If we don't already have this file
        if file_content.name not in mycsv_names:
            raw_url = file_content.download_url
            if '.csv' in raw_url:
                csv_files.append(raw_url)
                split_url = raw_url.split('/')
                foldername = split_url[split_url.index('data-processed') + 1]
                #print(foldername)
                #print(file_content.name)
                #print(' ')
                #myrepo.create_file("forecasts/" + foldername + "/" + file_content.name, "Create processed forecast files", output.getvalue(), branch="master")


#print(csv_files)



csv_grouped = {}

for file in csv_files:
    split_file = file.split('/')
    if 'data-processed' not in split_file:
        continue
    index = split_file.index('data-processed')
    org = split_file[index+1]
    if org not in csv_grouped:
        csv_grouped[org] = [file]
    else:
        csv_grouped[org].append(file)

#print(csv_grouped)


for group in csv_grouped:
    '''groups = ['IHME-CurveFit', 'LANL-GrowthRate', 'YYG-ParamSearch']
    #print(group)
    if group not in groups:
        continue'''
    '''forecast_file = myrepo.get_contents("forecasts_processed")
    print(forecast_file)
    break'''
    print(group)
    original_df = pd.read_csv("https://raw.githubusercontent.com/GTIdeas2020REU/covid-19-data/master/forecasts_processed/" + group + '.csv')
    dfs = [original_df]
    for link in csv_grouped[group]:
        df = pd.read_csv(link)
        df = df.loc[df['type'] == 'point']
        dfs.append(df)
    result = pd.concat(dfs)

    output = StringIO()
    result.to_csv(output)
    print(output.getvalue())
    print(' ')
    '''
    if group in groups:
        f = open(group + '.csv', 'w')
        f.write(output.getvalue())
        f.close()
    else:
        repo.create_file("forecasts_processed/" + group + '.csv', "Create processed forecast files", output.getvalue(), branch="master")
'''

