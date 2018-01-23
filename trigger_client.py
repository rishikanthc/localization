import paho.mqtt.client as mqtt
import os 
import time
from blebeacon import BeaconScanner

####global variables #####
exit_flag = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    client.subscribe("ledStatus")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global exit_flag
    print(msg.topic+" "+str(msg.payload))
    if str(msg.payload) == '0':
        exit_flag = 1
        os._exit(0)
    elif str(msg.payload) == '1':
        loc_start()

def loc_start():
    scanner = BeaconScanner()
    scanner.set_scan_enable(False)
    scanner.set_filter()
    scanner.set_scan_parameters()
    scanner.set_scan_enable(True)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("server.local", 1883, 60)
    client.loop_forever()

