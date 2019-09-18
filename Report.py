from requests import get
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import get_time
import credentials
import pprint
import matplotlib.pyplot as plt
import numpy as np



def hass_time_format(stamp):
    return stamp.strftime("%Y-%m-%dT%T")

period_start = hass_time_format(get_time.day(1)) #x days ago
period_end = hass_time_format(datetime.now()) #now obviously

input_var = '/api/history/period/'+period_start+'?end_time='+period_start #should be period_end
input_var = '/api/states'
url = credentials.api_url+input_var
headers = {'x-ha-access': credentials.api_password,
           'content-type': 'application/json'}

response = get(url, headers=headers).json()

value_dict = [
'sensor.report_monthly_switch_kitchen_overhead',
'sensor.report_monthly_light_cabinets',
'sensor.report_monthly_light_wall',
'sensor.report_monthly_light_sink',
'sensor.report_monthly_light_bedroom_1',
'sensor.report_monthly_light_dresser',
'sensor.report_monthly_light_nightstand',
'sensor.report_monthly_light_bedroom_2',
'sensor.report_monthly_light_small_lamp',
'sensor.report_monthly_switch_sparkle_tree',
'sensor.report_monthly_switch_twinkle',
'sensor.report_monthly_switch_glass_door',
'sensor.report_monthly_light_dining_room_dimmer',
'sensor.report_monthly_switch_entryway_switch',
'sensor.report_monthly_switch_front_porch_switch',
'sensor.report_monthly_switch_downstairs_bathroom_fan_switch',
'sensor.report_monthly_switch_downstairs_bathroom_light_switch',
'sensor.report_monthly_light_desk_lamp',
'sensor.report_monthly_light_guest_room_lamp',
'sensor.report_monthly_switch_bathroom_fan_switch',
'sensor.report_monthly_switch_shower_light_switch',
'sensor.report_monthly_switch_upstairs_bathroom_light_switch'
]

result_dict = {}
n = 1

for x in response:
    if x['entity_id'] in value_dict:
        #print(x['entity_id'],x['state'])
        result_dict[n] = x
        n = n + 1
    #print(x['entity_id'])

#pprint.pprint(result_dict)

# for x in response:
#     for n,y in enumerate(x):
#         pprint.pprint(y)
#         # if y['entity_id'] == value_1:
#         #     print (y)

x_list = []
y_list = []

for entry in reversed(sorted(result_dict.items(), key=lambda k_v: float(k_v[1]['state']))):
#for entry in sorted(result_dict.items(),key=lambda x:getitem(x[1],'state')):
#for entry in result_dict:
    #print(entry[1]['entity_id'])
    # for x in entry:
    #     print(x)

    if 'friendly_name' in entry[1]['attributes']:
        name = entry[1]['attributes']['friendly_name']
        name = name.replace("Report Weekly: ",'')
        name = name.replace("Report Monthly: ",'')
        x_list.append(name)
    else:
        x_list.append(entry[1]['entity_id'])
    y_list.append(float(entry[1]['state']))

pprint.pprint(x_list)
pprint.pprint(y_list)


bar_width = 0.35
opacity = 0.4


fig, ax = plt.subplots(figsize=(13,8))
fig.subplots_adjust(bottom=0.35)


rects1 = ax.bar(x_list, y_list, bar_width,
                alpha=opacity, color='b', align='center',
                label='State')

major_ticks = np.arange(0, max(y_list)+5, 10)
minor_ticks = np.arange(0, max(y_list)+5, 1)

#ax.set_xticks(major_ticks)
#ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

# Or if you want different settings for the grids:
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

#ax.set_xlabel('Entity')
ax.set_ylabel('Hours')
ax.set_title('Week to Date Entity Hours')
#ax.yaxis.grid(True)
#plt.xticks(rotation=45)
plt.setp( ax.xaxis.get_majorticklabels(), rotation=45, ha="right", rotation_mode="anchor")


#ax.set_xticks(index + bar_width / 2)
#ax.set_xticklabels(('A', 'B', 'C', 'D', 'E'))
ax.legend()
plt.show()
