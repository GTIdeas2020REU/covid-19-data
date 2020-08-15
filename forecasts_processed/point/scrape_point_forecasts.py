import github
import pandas as pd
from io import StringIO
import time
import os

from info import token

start = time.time()

g = github.Github(token())

files = []
file = open('fileurls.txt', 'r')
for line in file:
    line = line.strip()
    files.append(line)


repo = g.get_repo("reichlab/covid19-forecast-hub")
contents = repo.get_contents("data-processed")


def get_filenames(model):
    contents = repo.get_contents("/data-processed/" + model)
    for content_file in contents:
        raw_url = content_file.download_url
        filename = content_file.name
        if filename[-3:] == 'csv' and raw_url not in files:
            files.append(raw_url)

            df = pd.read_csv(raw_url)
            df = df.loc[df['type'] == 'point']
            if not os.path.exists(model + '.csv'):
                df.to_csv(model + '.csv', mode='w', index=False)
            else:
                other = pd.read_csv(model + '.csv')
                dfs = pd.concat([other, df])
                dfs.to_csv(model + '.csv', mode='w', index=False)

    print(model)
    

csv_files = []
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
        get_filenames(file_content.name)


with open('fileurls.txt', 'w') as file:
    for f in files:
        file.write(f + "\n")

end = time.time()
print(' ')
print('TIME TAKEN (seconds):')
print(end-start)
