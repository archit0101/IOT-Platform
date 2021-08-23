import sys
import time
import schedule
import requests
import json

#IP="127.0.0.1"
#PORT="8000"
IP=sys.argv[2]
PORT=int(sys.argv[3])
ipPort=IP+":"+str(PORT)

#curBus=sys.argv[1]
#while(1):
#	time.sleep(120)
def funcforUseCase3():
	# Dictionary received from kafka	
	coordinates=requests.get("http://"+ipPort+"/getSensorData/coordinates")
	print(coordinates.text)
	coordinates=json.loads(coordinates.text)
	
	for cur in coordinates:
		#cur=Coordinates[curBus]
		count=0
		list1=[]
		for key in coordinates:
			# Manhattan Distance is used
			if(abs(coordinates[key][0]-coordinates[cur][0])+abs(coordinates[key][1]-coordinates[cur][1])<=7):
				count+=1
				list1.append(key)
		if(count>=3):
			print("with ",end=" ")
			print(cur)		
			for i in list1:
				if(i!=cur):
					print(i)
					response = requests.get("http://"+ipPort+"/changeControllerState/"+i+"/"+"switchBuzzerState"+"/True")

funcforUseCase3()
