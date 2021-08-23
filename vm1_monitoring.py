def func1(fname):
	os.system("gnome-terminal -x python3 "+fname)

IP ='127.0.0.1'
PORT = 9001
sockfd = socket.socket()
sockfd.bind((IP, PORT))
sockfd.listen(10)
while True:
	Client, address = sockfd.accept()
	ans=Client.recv(5000).decode()
	if ans="platfom_manager.py":
		func1(ans)

sockfd.close()