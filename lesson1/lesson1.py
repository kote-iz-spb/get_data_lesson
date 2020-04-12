import requests
import json
from pprint import pprint

#1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для
# конкретного пользователя, сохранить JSON-вывод в файле *.json.



headers = {'user_agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'}

user='sonzza'

github=f'https://api.github.com/users/{user}/repos'

response=requests.get(github,headers=headers)
data=json.loads(response.text)

with open(f'{user}_repos.json', 'w') as f:
    json.dump(data, f)

for i in range(len(data)):
    pprint(data[i]['name'])


