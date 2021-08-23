import threading
import time
import socket
from random import randrange
from socket import *
import requests

deadServers=[3000,3001]
activeServers=[]
query="Awake"
print("Checking servers...............")
def checkServer():
    t=2
    while(True):
        global activeServers
        global deadServers
        tempDead=[]
        tempActive=[]
        for port in deadServers:
            try:
                #mysock=socket(AF_INET,SOCK_STREAM)
                #mysock.connect(('127.0.0.1',port))
                #mysock.sendall(query.encode())
                #data=mysock.recv(5000).decode()
                data=requests.get('http://127.0.0.1:'+str(port)+'/isalive')
                #print("port "+str(port) + " is active")
                tempActive.append(port)
                #mysock.close()
            except:
                tempDead.append(port)
                #print("port "+str(port) + " is not active")
            
        deadServers=[]
        deadServers.extend(tempDead)
        activeServers.extend(tempActive)
        tempDead=[]
        tempActive=[]
        for port in activeServers:
            try:
                #mysock=socket(AF_INET,SOCK_STREAM)
                #mysock.connect(('127.0.0.1',port))
                #mysock.sendall(query.encode())
                #data=mysock.recv(5000).decode()
                data=requests.get('http://127.0.0.1:'+str(port)+'/isalive')
                #print("port "+str(port) + " is active")
                tempActive.append(port)
            except:
                #print("port "+str(port) + " is not active")
                tempDead.append(port)
            #mysock.close()
        activeServers=[]
        deadServers.extend(tempDead)
        activeServers.extend(tempActive)
        tempDead=[]
        tempActive=[]
        print("---------------------------------------------------------")
        print("active servers: ", activeServers)
        time.sleep(t)


num=0
def getPortNumber():
    global num
    num=num+1
    num=num%len(activeServers)
    #return activeServers[randrange(len(activeServers))]
    return activeServers[num]

    
t1=threading.Thread(target=checkServer,name="t1")
t1.start()
LoadBalancer=socket(AF_INET,SOCK_STREAM)
LoadBalancer.bind(('localhost',8050))
LoadBalancer.listen(5)
print("Load Balancer is up..................")
while(True):
    (clientSocket,address)=LoadBalancer.accept()
    query1=clientSocket.recv(1024).decode()
    print(query1)
    if(query1=="giveMePort"):
        clientSocket.sendall(str(getPortNumber()).encode())
