import requests
import json
import main

Base_URL = 'https://dev.copp42.ru/programs'

response = requests.get(f'{Base_URL}')

print(response.json())

#JSON для мероприятий
#response = requests.get('https://www.mininghamster.com/api/v2/aI6dgBApSPbph0kDISXNCaoHYvVgXTfS')
#print(response.json()[0]['success'])


#f = json.loads("Events.json")
#
# for item in f:
#     print(item)
#
# with open('Events.json', encoding='utf-8') as f:
#     data = f.read()
#     categories = json.loads(data)
#
# for i,name in enumerate(categories):
#     print(i, name)

#for i in categories:
    #print(i)
#    for j, name in enumerate(categories):
#    for j in categories['content'] :
  #      print(j)