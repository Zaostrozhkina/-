import requests
import json
#from pprint import pprint

url = 'https://api.vk.com/method/groups.get'
params = {'access_token': '073e55da3dfd38de29ed6244d1038b7364893ded3938adece4d14d792d58c3ca3c60ec88a19d481282c13',
          'user_id': '32536906',
          'extended': '1',
          'v': '5.131'}

response = requests.get(url, params=params)
j_data = response.json()

#pprint(j_data)

groups_list = []

for n in range(len(j_data['response']['items'])):
    groups_list.append(j_data['response']['items'][n]['name'])

print('\n'.join(groups_list))

with open ('groups.json', 'w') as groups:
    json.dump(j_data, groups)
