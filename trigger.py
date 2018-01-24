import paho.mqtt.publish as publish
import time
import sys

print("sending {}".format(sys.argv[1]))
publish.single("ledStatus", sys.argv[1], hostname="server.local")
