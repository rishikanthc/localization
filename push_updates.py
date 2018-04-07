import paho.mqtt.client as publisher
import time
import sys
import json
import requests

def on_publish(client, userdat, msg):
    print ("success\n")

topic = "location"
broker_addr = "192.168.10.6"
client = publisher.Client("locupdates")
client.on_publish = on_publish
client.username_pw_set("admin", "IBMProject$")
client.connect(broker_addr, 61613, 60)


while True:
    r = requests.get("http://server.local/location")
    #datum = json.loads(r.text)
    client.publish(topic, r.text, qos=0, retain=False)
    time.sleep(5)

