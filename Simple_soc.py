import socket
import sys
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#AF_INET=address family of ipv4, SOCK_STREAM=TCP port
ip=socket.gethostbyname("www.google.com")#will give the ip address of the website
print(ip)
name=socket.gethostbyaddr("142.250.195.68")#will give the name of the ip address
print(name)