def func(busname):
	os.system("gnome-terminal -- python3 busSensor.py "+busname)
def func1(fname):
	os.system("gnome-terminal -x python3 "+fname)

IP ='127.0.0.1'
PORT = 8001
sockfd = socket.socket()
sockfd.bind((IP, PORT))
sockfd.listen(10)
while True:
	Client, address = sockfd.accept()
	ans=Client.recv(5000).decode()
	if ans="sensor_manager.py":
		func1(ans)
	elif ans="bus1":
		func(1)
	elif ans="bus2":
		func(2)
	elif ans="bus3":
		func(3)
	elif ans="bus4":
		func(4)
	elif ans=="biometricsensor.py"
		func1(ans)

sockfd.close()
