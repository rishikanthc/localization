import paho.mqtt.publish as publish
import time
print("Sending 0...")
publish.single("ledStatus", "2", hostname="server.local")
time.sleep(1)
print("Sending 1...")
