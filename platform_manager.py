import socket
import _thread
import shutil
import json
import ast
import time
import requests
#import SensorManager as sm

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5018    # The port used by the server


def thread_conn(s,py_file_data,clientfd): #with scheduler #keyword,data1,clientfd(during)    
    HOST='127.0.0.1'
    PORT=8082
    ans="done"
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))

    #with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
     #   clientsocket.connect((HOST, PORT)) 
        #print("s")
        #print(s)
    if s=="start":
        py_file_data=py_file_data.split("*")
        data=py_file_data[0]+"*"+py_file_data[1]+"*"+py_file_data[2]+"*"+py_file_data[3]+"*"+py_file_data[4]
        clientsocket.sendall(str(data).encode())
        ans=clientsocket.recv(1024).decode()
        """
        if ans=="RECEIVED":
            clientsocket.sendall(str(py_file_data[5]).encode())
            
            ans=clientsocket.recv(1024).decode()
        else:
            clientsocket.sendall(str("recvd error msg").encode())
            ans=clientsocket.recv(1024).decode()
        """

    elif s=="stop":
        #py_file_data me appname
        #data="*STOP:"+py_file_data
        data="2021-05-07 15:07:55*2021-05-07 15:08:05*0*10*STOP:"+py_file_data
        clientsocket.sendall(str(data).encode())
        ans="successfully stopped!!!"
    
    elif s=="buzzer":
        s="2021-05-07 15:07:55*2021-05-07 15:08:05*0*10*buzzer"
        print("Module is being deployed!")
        clientsocket.sendall((s).encode())
        ans=clientsocket.recv(1024).decode()
        """
        if ans=="RECEIVED":
            clientsocket.sendall(str(py_file_data).encode())
            ans=clientsocket.recv(1024).decode()
        else:
            clientsocket.sendall(str("recvd error msg").encode())
            ans=clientsocket.recv(1024).decode()
        """
        #py_file_data me app3.py ka data
    clientsocket.close()
    clientfd.send(str(ans).encode())


def start_server(clientfd):
    #while(1):
    ipPort_SensorManager = "127.0.0.1:6767"
    query=clientfd.recv(5000).decode()
    #print(app_name)
    tokens=query.split("*")
    if tokens[0] =="MontoringRequest":
        clientfd.sendall("done".encode())

    elif tokens[0] == "app":
        if tokens[1]== "admin":
            print(1)

            #class installation
            if tokens[2] == "1":
                print(3)
                data=tokens[3]
                #response=str(sm.registerNewSensorClass(data).text)
                #response=str(sm.registerNewSensorClass(data))
                #print(response)
                url="http://"+ipPort_SensorManager+"/registerNewSensorClass/"+data
                response=requests.get(url).text
                clientfd.sendall(response.encode())
            
            # instance installation
            if tokens[2] == "2":
                print(4)
                data=tokens[3]
                #response=str(sm.makeSensorInstances(data).text)
                #response=str(sm.makeSensorInstances(data))
                #print(response)
                url="http://"+ipPort_SensorManager+"/makeSensorInstances/"+data
                response=requests.get(url).text
                clientfd.sendall(response.encode())


            
            # upload application
            if tokens[2] == "3":
                print(5)
                print("for_deployment of module")
                data1 = tokens[3]
                keyword = "buzzer"
                
                #print(data1)
                _thread.start_new_thread(thread_conn, (keyword,data1,clientfd)) 
                #response=str(sm.validateAppSensors(data).text)
                #response=str(sm.validateAppSensors(data))
                #print(response)
                #clientfd.sendall(response.encode())
        
            # upload application
            if tokens[2] == "4":
                print(6)
                data = tokens[3]
                #response=str(sm.validateAppSensors(data).text)
                #response=str(sm.installNewBarricades(data))
                url="http://"+ipPort_SensorManager+"/installNewBarricades/"+data
                response=requests.get(url).text
                if response=="True":
                    response = "Barricades installed successfully!!"
                print(response)
                clientfd.sendall(response.encode())
      
        if tokens[1] == "user" and tokens[2]=="start":
            print(2)
            #t=json.dumps(lst[i])
            #data1 = json.dumps(tokens[2]) #kunal wali file

            selected_app=tokens[3]
            selected_app=selected_app[:4]
            print("bus name:",selected_app)
            print()
            data1=""
            dt=""
            while("done" not in dt):
                print("Recving data1")
                dt=clientfd.recv(2000).decode()
                #print(dt)
                data1+=dt
                print()
            
            data1=data1[:-4]
            
            #lst=data1.split("done")[0]

            print("data1(app124):",data1,type(data1))
            res=clientfd.sendall("ohohoho".encode())
            response=clientfd.recv(500000).decode()
            #print("response:",response,type(response))
            data2 = json.loads(response)  #for archi
            print()
            print("response after loads:",data2,type(data2))

            #print("wtphuck!!!")

            sid=dict()
            #sid = sm.getSensorIdByLocation(tokens[2]).text #kunal wala
            #lst = sm.getSensorIdByLocation(tokens[2])
            
            s=""
            s+=str(data2["starttime"])
            s+="*"
            s+=str(data2["endtime"])
            s+="*"
            s+=str(data2["recurring_bit"])
            s+="*"
            s+=str(data2["recurring_interval"])
            s+="*"

            s+=selected_app
            s+="*"
            s+=data1

            _thread.start_new_thread(thread_conn, ("start",s,clientfd))  # function change upar (keyword,data to be sent,)
        

        if tokens[1] == "user" and tokens[2]=="STOP":
            print("tokend3:")
            print(tokens[3])
            _thread.start_new_thread(thread_conn, ("stop",tokens[3],clientfd))  # function change upar (keyword,bus_name,) 

    return

def server():
    serverfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverfd.bind((HOST,PORT))
    serverfd.listen(5)
    print("*****************************")
    print("Server Established")
    print("*****************************")
    while(1):
        clientfd,add=serverfd.accept()
        _thread.start_new_thread(start_server,(clientfd,))
        #clientfd.shutdown(socket.SHUT_WR)

        #start_new_thread(start_server, (clientfd,))
    serverfd.close()


server()
