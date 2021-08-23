import time
import sys
import socket
from _thread import *
import os
import ast
import subprocess
import json
import datetime as dt
import threading
import os.path
#-----------------------------------------------------------------------------------------------#

task = []  

'''
{
"starttime": "24:00 hours format",
"endtime": "24:00 hours format",
"recurring_bit" : 0/1,
"recurring_interval" : seconds in INT, 
"busname" : "string/buzzer/STOP:Busname",
}
'''

# IP PORT for Interacting with PLATFORM MANAGER
IP = "127.0.0.1"
PORT = 8082

#-----------------------------------------------------------------------------------------------#

def split_time(str1):
    d,t = str1.split(" ")
    Y,mo,d = d.split("-")
    h,m,s = t.split(":")
    #print(Y,mo,d,h,m,s)
    return int(Y), int(mo), int(d), int(h), int(m), int(s)

#-----------------------------------------------------------------------------------------------#

def process_time(st):
    Y,mo,d,h,m,s = split_time(st)

    a = dt.datetime(Y,mo,d,h,m,s)
    b = dt.datetime(1970,1,1,00,00,00)

    return (a-b).total_seconds() - 19800

#-----------------------------------------------------------------------------------------------#

def generate_algo_file(Client, appname):
    dt=""
    content = Client.recv(1024).decode()
    dt+=content
    while(len(content)>0):
        content=Client.recv(1024).decode()
        dt+=content

    if len(dt)<=0:
        print("Empty file received!\n")
        return
    
    fileName = appname
    #print("STATUS : " + fileName + " received\n")
    with open(fileName, "w") as f:
        f.writelines(dt)


    resp = "RECEIVED"
    Client.sendall(resp.encode())

#-----------------------------------------------------------------------------------------------#

def push_task(data):
    stime = data['starttime']
    etime = data['endtime']
    print(etime,stime)
    if data['appname']!='buzzer.py':
        start_time = process_time(stime)
        end_time = process_time(etime)
        data['starttime'] = start_time
        data['endtime'] = end_time
    else:
        data['starttime'] = float(stime)
        data['endtime'] = float(etime)

    datalist = []
    if data["appname"]=="buzzer.py":
        datalist.append(data['starttime'])
        datalist.append(data['endtime'])
        datalist.append(data['recurring_bit'])
        datalist.append(data['recurring_interval'])
        datalist.append(data['appname'])
        datalist.append("-1")
    else:
        datalist.append(data['starttime'])
        datalist.append(data['endtime'])
        datalist.append(data['recurring_bit'])
        datalist.append(data['recurring_interval'])
        datalist.append(data['appname'])
        datalist.append(data['busname'])


    task.append(datalist)

#-----------------------------------------------------------------------------------------------#

# Function for Receiving Task from PLATFORM MANAGER

def get_data(Client):
    print("In get data")
    global task
    req = Client.recv(2048).decode()
    lst=req.split("*")
    print(len(lst),lst)
    data={}
    if lst[4][:4]=="STOP":
        req,busname=lst[4].split(":")
        with open("stop/"+busname+".txt","w") as f:
            f.write("")
            f.write("True")
        #f.close()
        return
    elif lst[4]=="buzzer":
        #print("Hi Buzzer, How are you buddy?")
        tm = time.time()
        data["starttime"] = str(tm)
        data["endtime"] = str(tm+30)
        #print(data["starttime"],data["endtime"])
        data["recurring_bit"] = 1
        data["recurring_interval"] = 120
        data["appname"] = "buzzer.py"

    else:
        data["starttime"]=lst[0]
        data["endtime"]=lst[1]
        data["recurring_bit"]=lst[2]
        data["recurring_interval"]=lst[3]
        data["appname"]="bus.py"
        data["busname"]=lst[4]
    #data["sid"]=lst[5]
    #sid = ast.literal_eval(data['sid'])

    #-----> CHANGES FOR SOMYA

    '''
    for s in sid:
        if s == "False":
            resp = "Failed"
            Client.sendall(resp.encode())
            return
    '''

    #task.append(data)
    push_task(data)
    resp = "RECEIVED"
    Client.sendall(resp.encode())
    #temp=data["appname"]+".py"
    #generate_algo_file(Client, data["appname"])

#-----------------------------------------------------------------------------------------------#

# NOT CURRENTLY IN USE

def importName(modulename, name):
    """ 
    Import a named object from a module in the context of this function.
    """
    try:
        module = __import__(modulename, globals(), locals(  ), [name])
    except ImportError:
        return None
    return vars(module)[name]

#-----------------------------------------------------------------------------------------------#

# Function for requesting HOST and PORT from SERVER_MANAGER

def server_manager():
    IP = "127.0.0.1"
    PORT = 8050    #@@@@@@
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.connect((IP, PORT))
    sockfd.send("giveMePort".encode())  
    resp = sockfd.recv(1024).decode()
    sockfd.close()
    PORT = resp
    IP="127.0.0.1"
    print("#-> INSTANCE ALLOCATED")
    return IP, int(PORT)

#-----------------------------------------------------------------------------------------------#

# Function for sending FREE INSTANCE REQ to SERVER_MANAGER

def free_server_instance(host, port):
    IP = "127.0.0.1"
    PORT = 2121    #@@@@@@
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.connect((IP, PORT))
    sockfd.send( ("free_server|" + str(host) + "|" + str(port)).encode() )  
    sockfd.close()
    print("\n#-> INSTANCE FREED")

#-----------------------------------------------------------------------------------------------#

# Function for opening TERMINAL UI for ENDUSER

def open_terminal_UI(appname, endtime, starttime, busname, HOST, PORT):
    #os.system(appname + " " + str(float(endtime) - float(starttime)))
    os.system("gnome-terminal -x python3 " + appname +" "+busname+" "+HOST+" "+str(PORT)+" "+str(float(endtime) - float(starttime)))
    #os.system(appname +" "+busname+" "+HOST+" "+str(PORT)+" "+str(float(endtime) - float(starttime)))


#-----------------------------------------------------------------------------------------------#

# Function to run the scheduled process (Will create copy of app.py -> replace IP,PORT,SID -> Call open_terminal_UI -> Call free instance)

def connect(starttime, endtime, appname, busname):
    #print("CONNECT KE ANDAR\n\n")
    HOST, PORT = server_manager()

    #HOST = '127.0.0.1'   #@@@@@
    #PORT = 5000          #@@@@@  

    print("***********"+HOST," ",PORT," Scheduled instance"+"***********")

    #----> app.py ki nayi copy (myApp.py)
    #----> myApp.py IP PORT replace HOST PORT
    #----> how to send endtime to myApp.py
    '''
    s = ""  
    if len(sids)>1:
        for item in sids:
            s += str (item) + "/"
        s = s[:-1]
    else:
        s = sids

    #print(appname + "connect ke andar aagya he")
    #fin = open(appname, "rt")
    #fout = open("_" + appname, "wt")
    
    for line in fin:
        fout.write(line.replace('IP', HOST).replace('PORT', str(PORT)).replace("sensorID1", s))
    fin.close()
    fout.close()
    '''
    # tempHost = '127.0.0.1'
    # tempPort = 5656

    # sockfd = socket.socket()
    # sockfd.bind((tempHost, tempPort))

    # #print('\nListening for Server Response...')
    # sockfd.listen(10)
    #bus1=th.start
    if busname=='-1':
        start_new_thread(open_terminal_UI, (appname, endtime, starttime, busname, HOST, PORT))
    else:
        f=open("stop/"+busname+".txt","w")
        f.write("")
        f.write("False")
        f.close()
        start_new_thread(open_terminal_UI, (appname, endtime, starttime, busname, HOST, PORT))
    # while time.time() <= float(endtime):
    #     print("--------- NOMPS ========")
    #     Client, address = sockfd.accept()
    #     resp = Client.recv(2048).decode()
    #     if resp=="4":
    #         break

    # sockfd.close()
    # print("SOCKET CLOSED\n")
    #free_server_instance(HOST, PORT)

#-----------------------------------------------------------------------------------------------#

# Function will sort the task list and pick the process with start_time = current_time

def schedule():
    global task
    while len(task)!=0:
        st = time.time()
        #sort
        task.sort(key=lambda task:task[0])

        while len(task)!=0 and st >= float(task[0][0]):
            l = task[0]
            #print("WHILE KE ANDAR\n\n")
            #print("This is ur ass:"+l[2]+" "+l[3])
            #print(type(l[2]))
            if int(l[2])==1:
                #print("RECUR KE ANDAR\n\n")
                
                temp = task[0]
                if int(l[3])==-1:
                    temp[0] = temp[0] + 86400
                    temp[1] = temp[1] + 86400
                else:
                    #print("Hiiiiiii")
                    temp[0] = temp[0] + int(l[3])
                    temp[1] = temp[1] + int(l[3])
                    print(temp[0])
                    print(temp[1])
                    print("-----------------")
                task.append(temp)

            task=task[1:]
            start_new_thread(connect, (l[0],l[1],l[4],l[5]))   ###call by threading library method

#-----------------------------------------------------------------------------------------------#

# It is used to create the server side for get_data function to listen continously for task from PLATFORM MANAGER

def process_request():
    global IP
    global PORT
    sockfd = socket.socket()
    sockfd.bind((IP, PORT))

    print('\nListening ...\n')
    sockfd.listen(10)
    start_new_thread(schedule, ())

    while True:
        Client, address = sockfd.accept()
        start_new_thread(get_data, (Client,))

    sockfd.close()

#-----------------------------------------------------------------------------------------------#

# ME TO MAIN HUN

def main():
    if os.path.isfile("schedule.log"):
        f=open("schedule.log","r")
        x=f.readline()
        f.close()

    start_new_thread(process_request, ())
    while(True):
        schedule()

#-----------------------------------------------------------------------------------------------#

main()

