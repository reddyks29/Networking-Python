import socket
import requests

target_host='www.google.com'
target_port=80

#create socket
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connect client
client.connect((target_host,target_port))

#send some data as bytes
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

#recieve some data
response=client.recv(4096)

print(response.decode())
print("-----------------------------------------------------------------------------------------------------------------------------")

#another method using request module
response1=requests.get("http://www.google.com")
#print status code
print(f"status code {response1.status_code}\n")
#print header
print(f"header {response1.headers}\n\n")
#print text
print(f"text {response1.text}\n")

print("---------------------------------------------------------------------------------------------------------------------------")
#to retrive head and options in request method
response2=requests.head("http://www.google.com")
print(f"request head {response1}")
response3=requests.options("http://www.amazon.com")
print(f"options {response2}")

client.close()
