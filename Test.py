from requests import get
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import credentials



def cut_time(last_changed):
    sep = '+'
    x2 = last_changed.split(sep, 1)[0]
    sep2 = '.'
    x3 = x2.split(sep2, 1)[0]
    time_formatted = datetime.strptime(x3, '%Y-%m-%dT%H:%M:%S')
    time_adjusted = time_formatted - timedelta(hours=5)
    timestamp = datetime.now()
    time_since = timestamp - time_adjusted
    nice_time_since = str(time_since).split(".",1)[0]
    return nice_time_since



headers = {'x-ha-access': credentials.api_password,
           'content-type': 'application/json'}

VAR6 = '/api/states/group.all_switches'
VAR7 = '/api/states/group.all_lights'

url = credentials.api_url+VAR6
response1 = get(url, headers=headers).json()

url = credentials.api_url+VAR7
response2 = get(url, headers=headers).json()

response_dict = {}

if response1['state'] == 'on':
    for value in response1['attributes']['entity_id']:
        url =  credentials.api_url+"/api/states/"+str(value)
        response = get(url, headers=headers).json()
        print(value)
        response_dict[value] = {}
        response_dict[value]['state'] = response['state']
        response_dict[value]['last_changed'] = cut_time(response['last_changed'])

if response2['state'] == 'on':
    for value in response2['attributes']['entity_id']:
        url =  credentials.api_url+"/api/states/"+str(value)
        response = get(url, headers=headers).json()
        print(value)
        response_dict[value] = {}
        response_dict[value]['state'] = response['state']
        response_dict[value]['last_changed'] = cut_time(response['last_changed'])

print("**************")
for value in response_dict:
    if response_dict[value]['state'] == 'on':
        print(value+": "+response_dict[value]['state']+" : "+str(response_dict[value]['last_changed']))
