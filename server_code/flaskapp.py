from flask import Flask, jsonify, request, make_response
import logging
from logging.handlers import RotatingFileHandler
import paho.mqtt.publish as publish
import pickle
import math
import operator


app = Flask(__name__)

### Global Variables ###
message = "hello"
XY_train = []
rssi_1 = 0
rssi_2 = 0
rssi_3 = 0



################# KNN #######################
def load_data(file_name):
    f = open(file_name)
    var = pickle.load(f)
    f.close()
    return var

def dist_func(train_point, test_point):
    dist = (train_point[0] - test_point[0])**2
    dist += (train_point[1] - test_point[1])**2 
    dist += (train_point[2] - test_point[2])**2
    return math.sqrt(dist)
                    
def getNeighbors(trainingSet, testInstance, k):
    global XY_train
    distances = []
    for x in range(len(XY_train)):
        dist = dist_func(testInstance,XY_train[x])
        distances.append((XY_train[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


############# APIs #########################

@app.route('/')
def hello_world():
    global rssi_1, XY_train
    #XY_train = load_data("/home/pi/localization/X_Y_train.data")
    #XY_train = load_data("/home/pi/localization/new_train.data")
    XY_train = load_data("/home/pi/localization/boosted_train.data")
    #XY_train = load_data("/home/pi/localization/new1_train.data")
    return "Values: {} {} {}".format(str(rssi_1), str(rssi_2), str(rssi_3)) 
    #return 'Hello from Flask!'

@app.route('/location')
def findLocation():
    global rssi_1, rssi_2, rssi_3
    loc_area = "Location unavailable"

    if rssi_1 == 0 or rssi_2 == 0 or rssi_3 == 0:
        return jsonify({'area':loc_area, 'rssi1':rssi_1, 'rssi2':rssi_1, 'rssi3':rssi_3})
    else:
        neighbors = getNeighbors(XY_train, (rssi_1, rssi_2, rssi_3), 15)
        loc = getResponse(neighbors)

    if loc == 'b':
        loc_area = "bedroom"
    elif loc == 'k':
        loc_area = "kitchen"
    elif loc == 'h':
        loc_area = "hallway"
    elif loc == 'l':
        loc_area = "living room"
    else:
        loc_area = "Unknown"

    return jsonify({'area':loc_area, 'rssi1':rssi_1, 'rssi2':rssi_1, 'rssi3':rssi_3})


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


