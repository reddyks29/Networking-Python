import socket
import sys
try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#will create the socket
    print("socket created successfully")
except socket.error as err:
    print(f"error occured")
port=80
try:
    host_ip=socket.gethostbyname("www.google.com")
except socket.gaierror():
    print("error resolving the host\n")
    sys.exit()
s.connect((host_ip,port))
print(f"socket is connected to git hub ={host_ip}")