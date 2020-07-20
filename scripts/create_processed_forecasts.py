from info import token

import github
import pandas as pd
from io import StringIO

g = github.Github(token())
repo = g.get_repo("GTIdeas2020REU/covid-19-data")
contents = repo.get_contents("")

csv_files = []
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        raw_url = file_content.download_url
        if '.csv' in raw_url:
            csv_files.append(raw_url)

#print(csv_files)
csv_grouped = {}

for file in csv_files:
    split_file = file.split('/')
    if 'forecasts' not in split_file:
        continue
    index = split_file.index('forecasts')
    org = split_file[index+1]
    if org not in csv_grouped:
        csv_grouped[org] = [file]
    else:
        csv_grouped[org].append(file)

#print(csv_grouped)

for group in csv_grouped:
    groups = ['IHME-CurveFit', 'LANL-GrowthRate', 'YYG-ParamSearch']
    #print(group)
    if group not in groups:
        continue

    dfs = []
    for link in csv_grouped[group]:
        df = pd.read_csv(link)
        df = df.loc[df['type'] == 'point']
        dfs.append(df)
    result = pd.concat(dfs)

    output = StringIO()
    result.to_csv(output)

    if group in groups:
        f = open(group + '.csv', 'w')
        f.write(output.getvalue())
        f.close()
    else:
        repo.create_file("forecasts_processed/" + group + '.csv', "Create processed forecast files", output.getvalue(), branch="master")


