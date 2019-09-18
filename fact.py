import requests
import json
url = 'http://randomuselessfact.appspot.com/today.json?language=en'
#url = 'https://cat-fact.herokuapp.com/facts'
response = requests.get(url).json()

print(response['text'])
