import paho.mqtt.client as mqtt
import os 
import subprocess 
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
    scanner.set_scan_enable(True)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("server.local", 1883, 60)
    client.loop_forever()

