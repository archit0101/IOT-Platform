from flask import Flask, jsonify, Response, request
import time
import requests
import json
#import Dao as dao
from pykafka import KafkaClient
from pykafka.common import OffsetType
import json
import sys
import threading
from socket import *

ipPort_SensorManager = "127.0.0.1:6767"


app = Flask(__name__)

#/getSensorData/<sensorID>/<field>

sleepTime=5
@app.route('/getSensorData/<sensorID>')
def getSensorData(sensorID):
    url="http://"+ipPort_SensorManager+"/getSensorData/"+sensorID
    attempt=1
    attemptFlag=True
    while (attempt<5 and attemptFlag):
        try:
            global response
            response = requests.get(url)
            attemptFlag=False
        except:
            print("Error in getting sensor data from Sensor Manager, attempt:",str(attempt))
        time.sleep(sleepTime)
        attempt+=1
    return str(response.text)

@app.route('/getKafkaTopic/<kafkaTopic>')
def getKafkaTopic(kafkaTopic):
    url="http://"+ipPort_SensorManager+"/getKafkaTopic/"+kafkaTopic
    attempt=1
    attemptFlag=True
    while (attempt<5 and attemptFlag):
        try:
            global response
            response = requests.get(url)
            attemptFlag=False
        except:
            print("Error in getting Kafka Topic from Sensor Manager, attempt:",str(attempt))
        time.sleep(sleepTime)
        attempt+=1
    return str(response.text)

@app.route('/sendNotification/<msg>')
def sendNotification(msg):
    url="http://"+ipPort_SensorManager+"/sendNotification/"+msg
    attempt=1
    attemptFlag=True
    while (attempt<5 and attemptFlag):
        try:
            global response
            response = requests.get(url)
            attemptFlag=False
        except:
            print("Error in sending notification to Sensor Manager, attempt:",str(attempt))
        time.sleep(sleepTime)
        attempt+=1
    return str(response.text)

@app.route('/changeControllerState/<controllerID>/<field>/<newValue>')
def changeControllerState(controllerID, field,newValue):
    #print(sensorID, field)
    url="http://"+ipPort_SensorManager+"/changeControllerState/"+controllerID+"/"+field+"/"+newValue
    attempt=1
    attemptFlag=True
    while (attempt<5 and attemptFlag):
        try:
            global response
            response = requests.get(url)
            attemptFlag=False
        except:
            print("Error in sending switching controller state to Sensor Manager, attempt:",str(attempt))
        time.sleep(sleepTime)
        attempt+=1
    return str(response.text)
    
@app.route('/isalive')
def isalive():
    return str("Yes")

if __name__ == '__main__':
    app.run(port = int(sys.argv[1]))







