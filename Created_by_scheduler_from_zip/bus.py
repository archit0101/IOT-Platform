import threading
import time
import random
from _thread import *
import json
import requests
from flask import Flask, jsonify, Response, request
from pykafka import KafkaClient
import sys
from pykafka.common import OffsetType
import math
import os

busID=sys.argv[1]
IP=sys.argv[2]
PORT=int(sys.argv[3])
ipPort=IP+":"+str(PORT)
duration=int(float(sys.argv[4]))



biometricID="Biom " +busID

attempt=1
attemptFlag=True
while (attempt<5 and attemptFlag):
    try:
        global kafkaTopicBio
        kafkaTopicBio=requests.get("http://"+ipPort+"/getKafkaTopic/"+biometricID)
        kafkaTopicBio=kafkaTopicBio.text
        attemptFlag=False
    except:
        print("Error in getting Biometric Kafka Topic from Sensor Manager")
    time.sleep(5)
    attempt+=1


attempt=1
attemptFlag=True
while (attempt<5 and attemptFlag):
    try:
        global kafkaTopicBus
        kafkaTopicBus=requests.get("http://"+ipPort+"/getKafkaTopic/"+busID)
        kafkaTopicBus=kafkaTopicBus.text
        attemptFlag=False
    except:
        print("Error in getting Bus Kafka Topic from Sensor Manager")
    time.sleep(5)
    attempt+=1


rate = 10
xf=10
yf=10
tempThreshold=33
lightThreshold=207
def get_fare(xi,yi):
    global xf, yf, rate
    #print(xf,yf,xi,yi)
    fare=abs((xf+yf)-(xi+yi))*5 + 100
    #print(fare)
    return fare


def sendSMS(board):
    #send sms
    print(board)

def getBusCurrentCor():
    client = KafkaClient(hosts='localhost:9092')
    for i in client.topics[kafkaTopicBus].get_simple_consumer(auto_offset_reset=OffsetType.LATEST,reset_offset_on_start=True):
        data_json = i.value.decode()
        data = json.loads(data_json)
        cor= (data["GPS"])
        temp= (data["currentTemp"])
        lux= (data["currentLux"])
        return cor,temp,lux

def getBiometric():
    client = KafkaClient(hosts='localhost:9092')
    flag=True
    
    for i in client.topics[kafkaTopicBio].get_simple_consumer(auto_offset_reset=OffsetType.LATEST,reset_offset_on_start=True):
        data_json = i.value.decode()
        #print(data_json)
        data = json.loads(data_json)
        personId= (data["personID"])
        busCorrdinate,temp,lux=getBusCurrentCor()
        fare=get_fare(busCorrdinate[0],busCorrdinate[1])
        msg=personId + " has boarded Bus: "+str(busID)+" having fare: "+str(fare)
        sendSMS(msg)
        # if flag:
        #     flag=False
        if temp>tempThreshold:
            attempt=1
            attemptFlag=True
            while (attempt<5 and attemptFlag):
                try:
                    requests.get("http://"+ipPort+"/changeControllerState/"+busID+"/"+"switchACState"+"/True")
                    attemptFlag=False
                except:
                    print("Error in calling controller from Sensor Manager for Switching On AC")
                time.sleep(5)
                attempt+=1
        
        if lux<lightThreshold:
            attempt=1
            attemptFlag=True
            while (attempt<5 and attemptFlag):
                try:
                    requests.get("http://"+ipPort+"/changeControllerState/"+busID+"/"+"switchLightState"+"/True")
                    attemptFlag=False
                except:
                    print("Error in calling controller from Sensor Manager for Switching On Lights")
                time.sleep(5)
                attempt+=1
                
#getBiometric()




def getGPS():
    attempt=1
    attemptFlag=True
    while (attempt<5 and attemptFlag):
        try:
            global barricadesList
            barricadesList=requests.get("http://"+ipPort+"/getSensorData/"+"barricades")
            attemptFlag=False
        except:
            print("Error in calling Sensor Manager for getting barricades list")
        time.sleep(5)
        attempt+=1
    #print(barricadesList.text)
    barricadesList=json.loads(barricadesList.text)
    barricadesList=barricadesList.replace("'",'"')
    #print(barricadesList,type(barricadesList))
    barricadesList=json.loads(barricadesList)
    #print(barricadesList,type(barricadesList))
    barricades=list()
    barricadesList=barricadesList["instances"]
    #print(barricadesList)
    for b in barricadesList:
        barricades.append((float(b["X-cor"]),float(b["Y-cor"]),str(b["name"])))

    threshold=2

    client = KafkaClient(hosts='localhost:9092')
    for i in client.topics[kafkaTopicBus].get_simple_consumer(auto_offset_reset=OffsetType.LATEST,reset_offset_on_start=True):
        data_json = i.value.decode()
        data = json.loads(data_json)
        cor= (data["GPS"])
        for bar in barricades:
            if math.sqrt(  (int(cor[0])-int(bar[0]))**2 + (int(cor[1])-int(bar[1]))**2     )<=threshold:
                barricadeName=bar[2]
                msg= str(busID)+ " has passed barricade "+str(barricadeName)
                print(msg)
                attempt=1
                attemptFlag=True
                while (attempt<5 and attemptFlag):
                    try:
                        requests.get("http://"+ipPort+"/sendNotification/"+msg)
                        attemptFlag=False
                    except:
                        print("Error in calling Sensor Manager for sending Notification for bus passing barricades")
                    time.sleep(5)
                    attempt+=1
                barricades.remove(bar)

                
def forceStop():
    stopfile="stop/"+busID+".txt"
    while True:
        with open(stopfile, 'r') as f:
            stopCondition=f.readline()
            #print(stopCondition)
            if stopCondition=="True":
                os._exit(1)                                  
            time.sleep(1)

def durationStop():
    global duration
    #print(duration)
    while True:
        if duration == 0:
            os._exit(1)
        time.sleep(1)
        duration-=1
    

#application 1 and 2
biometricThread=threading.Thread(target=getBiometric,name="biometricThread")
biometricThread.start()

#application 4
gpsThread=threading.Thread(target=getGPS,name="gpsThread")
gpsThread.start()

#Force Stop
forceStopThread=threading.Thread(target=forceStop,name="forceStopThread")
forceStopThread.start()

#Duration Stop
durationStopThread=threading.Thread(target=durationStop,name="durationStopThread")
durationStopThread.start()
