from requests import get
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import get_time
import credentials
import pprint
import calendar
from pushover import Client #pip install python-pushover



client = Client(credentials.push_id, api_token=credentials.push_token)

def hass_time_format(stamp):
    return stamp.strftime("%Y-%m-%dT%T")

def convert_weekday_short(i):
    return str(calendar.day_abbr[i.weekday()])+" "+str(calendar.month_abbr[i.month])+" "+str(i.day)

def convert_weekday_full(i):
    return str(calendar.day_name[i.weekday()])+" "+str(calendar.month_name[i.month])+" "+str(i.day)

def get_weekly():
    mhs = 0
    mms = 0
    total = 0

    input_var = '/api/states'
    url = credentials.api_url+input_var
    headers = {'x-ha-access': credentials.api_password,
               'content-type': 'application/json'}

    response = get(url, headers=headers).json()

    for x in response:
        if x['entity_id'] == 'sensor.work_mhs_this_week':
            mhs = x['state']
        if x['entity_id'] == 'sensor.work_mms_this_week':
            mms = x['state']
        if x['entity_id'] == 'sensor.work_this_week':
            total = x['state']

    return float(mhs),float(mms),float(total)

def ft(x):
    return str("{0:.2f}".format(x))

def nt(time):
    hours = int(time)
    minutes = (time*60) % 60
    seconds = (time*3600) % 60
    return "%d:%02d:%02d" % (hours, minutes, seconds)


def notify(goal_hours,mhs,mms,total,diff):
    if diff > 0:
        iden = "+ "
    else:
        iden = ""


    msg = ("Goal: "+nt(goal_hours)+"\nDiff: "+iden+nt(diff)+"\nTotal: "+nt(total)\
    +"\nMHS: "+nt(mhs)+"\nMMS: "+nt(mms))

    client.send_message(msg, title="Weekly Work")#, priority="-2")

mhs,mms,total = get_weekly()

timestamp = datetime.now()
cur_weekday = timestamp.weekday()

if cur_weekday == 0:
    print("Monday")
    goal_hours = 8.0
    diff = float(total)-goal_hours
    notify(goal_hours,mhs,mms,total,diff)
if cur_weekday == 1:
    print("Tuesday")
    goal_hours = 16
if cur_weekday == 2:
    print("Wednesday")
    goal_hours = 24
if cur_weekday == 3:
    print("Thursday")
    goal_hours = 32
if cur_weekday == 4:
    print("Friday")
    goal_hours = 40
