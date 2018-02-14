from requests import get
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
import credentials
import get_time

def hass_time_format(stamp):
    return stamp.strftime("%Y-%m-%dT%T")

period_start = hass_time_format(get_time.day(.25))
period_end = hass_time_format(datetime.now())

input_var = '/api/history/period/'+period_start+'?end_time='+period_end

the_title = 'Temp Sensors'

value_1 = 'sensor.bathroom_temperature'
value_2 = 'sensor.sensor2_temperature'
value_3 = 'sensor.sensor3_temperature'

url = credentials.api_url+input_var
headers = {'x-ha-access': credentials.api_password,
           'content-type': 'application/json'}

response = get(url, headers=headers).json()

value_1_dict = {}
value_2_dict = {}
value_3_dict = {}

for x in response:
    for n,y in enumerate(x):
        if y['entity_id'] == value_1:
            value_1_dict[n] = y
        if y['entity_id'] == value_2:
            value_2_dict[n] = y
        if y['entity_id'] == value_3:
            value_3_dict[n] = y

value_1_x = []
value_1_y = []
value_2_x = []
value_2_y = []
value_3_x = []
value_3_y = []

for n,x in enumerate(value_1_dict):
    if value_1_dict[x]['state'] != 'unknown':
        if float(value_1_dict[x]['state']) > 5:
            value_1_y.append(value_1_dict[x]['state'])
            #print(value_1_dict[x]['last_changed'])
            sep = '+'
            x2 = value_1_dict[x]['last_changed'].split(sep, 1)[0]
            sep2 = '.'
            x3 = x2.split(sep2, 1)[0]
            time_formatted = datetime.strptime(x3, '%Y-%m-%dT%H:%M:%S')
            time_adjusted = time_formatted - timedelta(hours=5)
            value_1_x.append(time_adjusted)

for n,x in enumerate(value_2_dict):
    if value_2_dict[x]['state'] != 'unknown':
        if float(value_2_dict[x]['state']) > 5:
            value_2_y.append(value_2_dict[x]['state'])
            #print(value_2_dict[x]['last_changed'])
            sep = '+'
            x2 = value_2_dict[x]['last_changed'].split(sep, 1)[0]
            sep2 = '.'
            x3 = x2.split(sep2, 1)[0]
            time_formatted = datetime.strptime(x3, '%Y-%m-%dT%H:%M:%S')
            time_adjusted = time_formatted - timedelta(hours=5)
            value_2_x.append(time_adjusted)

for n,x in enumerate(value_3_dict):
    if value_3_dict[x]['state'] != 'unknown':
        if float(value_3_dict[x]['state']) > 5:
            value_3_y.append(value_3_dict[x]['state'])
            #print(value_3_dict[x]['last_changed'])
            sep = '+'
            x2 = value_3_dict[x]['last_changed'].split(sep, 1)[0]
            sep2 = '.'
            x3 = x2.split(sep2, 1)[0]
            time_formatted = datetime.strptime(x3, '%Y-%m-%dT%H:%M:%S')
            time_adjusted = time_formatted - timedelta(hours=5)
            value_3_x.append(time_adjusted)

# for d,v in zip(value_2_x,value_2_y):
#     print(str(d)+" : "+str(v))

plt.title(the_title)
plt.rcParams['lines.linewidth'] = 2
plt.plot(value_1_x,value_1_y, color='red')
plt.plot(value_2_x,value_2_y, color='blue')
plt.step(value_3_x,value_3_y, color='orange')
plt.legend([value_1,value_2,value_3])
plt.plot


plt.show()
