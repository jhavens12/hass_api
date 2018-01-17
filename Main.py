from requests import get
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
import credentials

timestamp = str(datetime.now())

# VAR1 = '/api/states/climate.downstairs'
# VAR2 = '/api/history/period/2017-12-10T00:00:00?filter_entity_id=sensor.downstairs_thermostat_temperature'
# VAR3 = '/api/history/period/2017-12-09T00:00:00?end_time=2018-01-11T00:00:00'
# VAR4 = '/api/history/period/2017-09-24T00:00:00?end_time=2019-01-12T00:00:00'
VAR5 = '/api/history/period/2018-01-13T09:30:00?end_time=2018-01-14T8:45:00'

#my_entity = 'sensor.broadlink_sensor_temperature'
my_entity = 'sensor.sn1_temperature'
my_second_entity = 'sensor.sn1_temperature'

url = credentials.api_url+VAR5
headers = {'x-ha-access': credentials.api_password,
           'content-type': 'application/json'}

response = get(url, headers=headers).json()

entity_dict = {}
entity_2_dict = {}

for x in response:
    for n,y in enumerate(x):
        if y['entity_id'] == my_entity:
            entity_dict[n] = y
        # if y['entity_id'] == my_second_entity:
        #     entity_2_dict[n] = y

x_1_list = []
y_1_list = []
x_2_list = []
y_2_list = []

for n,x in enumerate(entity_dict):
    if entity_dict[x]['state'] != 'unknown':
        if float(entity_dict[x]['state']) > 5:
            y_1_list.append(entity_dict[x]['state'])
            print(entity_dict[x]['last_changed'])
            sep = '+'
            x2 = entity_dict[x]['last_changed'].split(sep, 1)[0]
            sep2 = '.'
            x3 = x2.split(sep2, 1)[0]
            time_formatted = datetime.strptime(x3, '%Y-%m-%dT%H:%M:%S')
            time_adjusted = time_formatted - timedelta(hours=5)
            x_1_list.append(time_adjusted)

x_1 = datetime(year=2018, month=1, day=12, hour=5, minute=47) #Turned on shower
x_2 = datetime(year=2018, month=1, day=12, hour=5, minute=57) #turned off shower
x_3 = datetime(year=2018, month=1, day=12, hour=5, minute=59) #turn on fan, open door
x_4 = datetime(year=2018, month=1, day=12, hour=6, minute=4) #turn off fan

plt.rcParams['lines.linewidth'] = 2
plt.plot(x_1_list,y_1_list, color='red')
# plt.axvline(x_1, color='blue', linewidth=1)
# plt.axvline(x_2, color='green', linewidth=1)
# plt.axvline(x_3, color='black', linewidth=1)
# plt.axvline(x_4, color='brown', linewidth=1)
plt.plot
#plt.plot(x_2_list,y_2_list, color='blue')
#plt.ylim(ymin=0)

plt.show()
