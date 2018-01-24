import paho.mqtt.client as mqtt
import os 
import subprocess 
import requests
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
    mssg = str(msg.payload)
    print(msg.topic+" "+mssg)
    if mssg == '0':
        exit_flag = 1
        os._exit(0)
    elif mssg == '1':
        loc_start()
    elif mssg == '2':
        p = subprocess.Popen("python /home/pi/localization/train.py", stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()
        print("Training finished", p_status)

def loc_start():
    scanner = BeaconScanner()
    scanner.set_scan_enable(False)
    scanner.set_filter()
    scanner.set_scan_parameters()
    scanner.ival = 0x0010
    scanner.wval = 0x0010
    while True:
        scanner.avg_rssi = 0
        scanner.count = 0
        scanner.set_scan_enable(True)
        time.sleep(1)
        scanner.set_scan_enable(False)
        if scanner.count:
            datum = {'val': scanner.avg_rssi / scanner.count}
            r = requests.post("http://server.local/node3", json=datum)
            print r.status_code
        time.sleep(5)


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("server.local", 1883, 60)
    client.loop_forever()

