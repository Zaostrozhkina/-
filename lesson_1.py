import requests
from pprint import pprint
import json

#Zaostrozhkina
#github
user = 'Zaostrozhkina'
url = f"https://api.github.com/users/{user}/repos"
params = {'type': 'all'}
response = requests.get(url, params=params)

j_data = response.json()
#pprint(j_data)

repositories = []

for n in range(len(j_data)):
    repositories.append(j_data[n]['name'])

#print(repo)
print(f"Репозитории пользователя {user}: {repositories}")

with open ('repositories.json', 'w') as repos:
    json.dump(j_data, repos)
