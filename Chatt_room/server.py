import socket
import  threading
#import emoji_func
host=' 192.168.0.111'
port=59000
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('192.168.0.111',59000))
server.listen()
clients=[]
aliases=[]



def broadcast(message):#sends msg to all
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            alias=aliases[index]
            broadcast(f'{alias}left the chatt room '.encode())
            aliases.remove(alias)
            break
#main
def recieve():
    while True:
        print("server is running and lisening.....")
        client,addr=server.accept()
        print(f'connection is established with{str(addr)}')
        client.send('alias?'.encode())
        alias=client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f"the alies of this client is {alias}".encode())
        broadcast(f'{alias} has connectd to the chatt room '.encode())
        client.send('you are now connected'.encode())
        #multithreading
        thread=threading.Thread(target=handle_client,args=(client,))
        thread.start()

if __name__=="__main__":
    recieve()
