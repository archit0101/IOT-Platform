import sys
import time
import socket

ip = '127.0.0.1'
port = 5656
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.connect((ip, port))

st=time.time()
endtime = sys.argv[1]
et = st + float(endtime)

while(st<=et):
    #print(et)
    st=time.time()
    i = input()
    if i == '4':
        sockfd.send("4".encode())
        sys.exit()
    print(i)

sockfd.send("4".encode())
sockfd.close()
sys.exit()