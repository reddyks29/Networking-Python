import socket
import threading
import colorama
#import emoji_func

colorama.init(autoreset=True)



alias=input("choose an alias>>")
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.0.111',59000))



def client_recieve():

    while True:
        try:
            message=client.recv(1024).decode()
            if message=='alias?':
                client.send(alias.encode())
            else:
                print('\033[31m'+message)
                print('\033[39m')        
        except:
            print("error!")
            client.close()
            break

def client_send():
    while True:
        message=f'{alias}:{input("")}'
        client.send(message.encode())

recieve_thread=threading.Thread(target=client_recieve)
recieve_thread.start()

send_thread=threading.Thread(target=client_send)
send_thread.start()

