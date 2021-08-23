import schedule
import time
import socket
import subprocess
from subprocess import call	
from _thread import *

def vm3():
	print("Re-initialsing module")
	subprocess.call("./aa.sh")

def vm2(txt):
	s.connect(('127.1.1.2',8001)) ##sensor manager
	print("connection made")
	s.sendall(txt.encode())

def vm1(txt):
	s.connect(('127.1.1.2',8001)) ##platform manager
	print("connection made")
	s.sendall(txt.encode())
			
def v1():
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
		try:
			#platform module
			print("Trying to make connection")
			s.connect(('127.0.0.1',9001))
			print("connection made")
			x="MontoringRequest"
			s.sendall(x.encode())
			print("recvd")
			#request=s.recv(5000).decode()
			#print(request)
			s.close()
			return
		except:
			
			start_new_thread(vm1,())


def v2():
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
		try:
			#sensor_manager module
			print("Trying to make connection")
			s.connect(('127.0.0.1',9001))
			print("connection made")
			x="MontoringRequest"
			s.sendall(x.encode())
			print("recvd")
			#request=s.recv(5000).decode()
			#print(request)
			s.close()
			return
		except:
			
			start_new_thread(vm2,())
		
		try:
			#biometricsensor module
			print("Trying to make connection")
			s.connect(('127.0.0.1',9001))
			print("connection made")
			x="MontoringRequest"
			s.sendall(x.encode())
			print("recvd")
			#request=s.recv(5000).decode()
			#print(request)
			s.close()
			return
		except:
			
			start_new_thread(vm2,("biometricsensor"))
		
		try:
			#bus1
			print("Trying to make connection")
			s.connect(('127.0.0.1',9001))
			print("connection made")
			x="MontoringRequest"
			s.sendall(x.encode())
			print("recvd")
			#request=s.recv(5000).decode()
			#print(request)
			s.close()
			return
		except:
			
			start_new_thread(vm2,("bus1"))
		
		try:
			#bus2
			print("Trying to make connection")
			s.connect(('127.0.0.1',9001))
			print("connection made")
			x="MontoringRequest"
			s.sendall(x.encode())
			print("recvd")
			#request=s.recv(5000).decode()
			#print(request)
			s.close()
			return
		except:
			
			start_new_thread(vm2,("bus2"))
		
		try:
			#bus3
			print("Trying to make connection")
			s.connect(('127.0.0.1',9001))
			print("connection made")
			x="MontoringRequest"
			s.sendall(x.encode())
			print("recvd")
			#request=s.recv(5000).decode()
			#print(request)
			s.close()
			return
		except:
			
			start_new_thread(vm2,("bus3"))
		
		try:
			#bus4
			print("Trying to make connection")
			s.connect(('127.0.0.1',9001))
			print("connection made")
			x="MontoringRequest"
			s.sendall(x.encode())
			print("recvd")
			#request=s.recv(5000).decode()
			#print(request)
			s.close()
			return
		except:
			
			start_new_thread(vm2,("bus4"))
		
		return

def v3():
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
		try:
			##scheduler module
			print("Trying to make connection")
			s.connect(('127.0.0.1',9001)) ##scheduler module
			print("connection made")
			x="MontoringRequest"
			s.sendall(x.encode())
			print("recvd")
			#request=s.recv(5000).decode()
			#print(request)
			s.close()
			return
		except:
			
			start_new_thread(vm3,())	
			return

schedule.every(10).seconds.do(v3)
schedule.every(2).seconds.do(v2)
schedule.every(5).seconds.do(v1)

while True:
	schedule.run_pending()
