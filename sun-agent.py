#
# Mqttagent that inform dailight
#
#



import paho.mqtt.client as mqtt
import random
import time
import re
import configparser
import os.path
import json

import traceback

from datetime import datetime
from suntime import Sun, SunTimeException

from dateutil import tz

config = configparser.RawConfigParser()


DAYLIGHT = "home/agents/daylight"


#############################################################
## MAIN

conffile = os.path.expanduser('~/.mqttagents.conf')
if not os.path.exists(conffile):
   raise Exception("config file " + conffile + " not found")

config.read(conffile)


username = config.get("agents","username")
password = config.get("agents","password")
mqttbroker = config.get("agents","mqttbroker")

pos = config.get("daylight_lattitude","pos")
if not pos:
   raise Exception("pos key not found")

pos = json.loads(pos)
print("position for daylight :" + str(json.dumps(pos)))

if not "latitude" in pos:
    raise Exception("latitude not found")

if not "longitude" in pos:
    raise Exception("longitude not found")

client2 = mqtt.Client()

# client2 is used to send events to wifi connection in the house 
client2.username_pw_set(username, password)
client2.connect(mqttbroker, 1883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client2.loop_start()


lastvalue = None

while True:
   try:
        time.sleep(3)

        sun = Sun(pos["latitude"], pos["longitude"])

        # Get today's sunrise and sunset in UTC
        today_sr = sun.get_sunrise_time()
        today_ss = sun.get_sunset_time()

        # On a special date in your machine's local time zone
        abd = datetime.now()

        abd_sr = sun.get_local_sunrise_time(abd)
        abd_ss = sun.get_local_sunset_time(abd)

        nowutc = datetime.now(tz.tzlocal())
        light =  nowutc < abd_ss and nowutc > abd_sr
        client2.publish(DAYLIGHT + "/light", "1" if light else "0")

        if lastvalue is None:
            lastvalue = light

        if lastvalue != light:
            client2.publish(DAYLIGHT + "/lightchanged", "1" if light else "0")


   except Exception:
        traceback.print_exc()



