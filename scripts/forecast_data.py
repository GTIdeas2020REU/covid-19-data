import github

g = github.Github('fde94c65ddafe5cc420e0fb75536b189faf4065e')
repo = g.get_repo("GTIdeas2020REU/covid-19-data")
contents = repo.get_contents("")

csv_files = []
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        #print(file_content.name)
        contents.extend(repo.get_contents(file_content.path))
    else:
        #print(' ')
        raw_url = file_content.download_url
        if '.csv' in raw_url:
            csv_files.append(raw_url)

#print(csv_files)
csv_grouped = {}

for file in csv_files:
    split_file = file.split('/')
    index = split_file.index('forecasts')
    org = split_file[index+1]
    if org not in csv_grouped:
        csv_grouped[org] = [file]
    else:
        csv_grouped[org].append(file)

print(csv_grouped)



