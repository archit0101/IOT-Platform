import  socket

IP = "127.0.0.1"
PORT = 2121

sockfd = socket.socket()
sockfd.bind((IP, PORT))

print('\nListening ...\n')
sockfd.listen(10)

while True:
    Client, address = sockfd.accept()
    Client.sendall("127.0.0.1:2213".encode())

sockfd.close()