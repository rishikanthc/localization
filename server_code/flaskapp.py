from flask import Flask, jsonify, request, make_response
import logging
from logging.handlers import RotatingFileHandler
import paho.mqtt.publish as publish
app = Flask(__name__)

### Global Variables ###
message = "hello"
rssi_1 = 0
rssi_2 = 0
rssi_3 = 0

@app.route('/')
def hello_world():
    global rssi_1
    return "Values: " + str(rssi_1) + str(rssi_2) + str(rssi_3) 
    #return 'Hello from Flask!'

@app.route('/start')
def start_train():
    publish.single("ledStatus", "2", hostname="server.local")
    return "Training Started"

@app.route('/node1', methods=['POST'])
def get_node1_val():
    global rssi_1

    if not request.json or not 'val' in request.json:
        app.logger.error("json error !!")

    rssi_1 = request.json['val']
    #app.logger.info(request.json['val'])
    return make_response("success",201)

@app.route('/node2', methods=['POST'])
def get_node2_val():
    global rssi_2

    if not request.json or not 'val' in request.json:
        app.logger.error("json error !!")

    rssi_2 = request.json['val']
    #app.logger.info(request.json['val'])
    return make_response("success",201)


@app.route('/node3', methods=['POST'])
def get_node3_val():
    global rssi_3

    rssi_3 = request.json['val']
    return make_response("success", 201)

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.error("testing logging")
    app.run()


