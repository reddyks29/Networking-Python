import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


def execute(cmd):
    #strips white spaces in cmd
    cmd=cmd.strip()
    #if there is nothing after stripped then return 
    if not cmd:
        return
    #split will help cmd to split and gets stored in list, stderr will return if any error occured
    output=subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)
    return output.decode()


#main function

if __name__=='__main__':
    parser=argparse.ArgumentParser(
        description='BHP NET TOOL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            '''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c #command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt #upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" #execute command
            netcat.py -t 192.168.1.108 -p 5555 #connect to server
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 #echo text to port 135'''
        )
    )

    parser.add_argument('-c','--command',action='store_true',help='command shell')
    parser.add_argument('-e','--execute',help='execute specified command')
    parser.add_argument('-l','--listen',action='store_true',help='listen')
    parser.add_argument('-p', '--port',type=int,default=5555, help='specified port')
    parser.add_argument('-u','--upload',help='upload file')
    args=parser.parse_args()
    #without listen arguments echo "Hello, World!" | python script.py
    #with listen argumetns python script.py --listen

    if args.listen:
        buffer=''
    else:
        buffer=sys.stdin.read()
    nc=NetCat(args,buffer.encode())
    nc.run()

   
#NetCat class

class NetCat:
    def __init__(self,args,buffer=None):
        self.args=args
        self.buffer=buffer
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #udp stream
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        #setsockopt(level, optname, value)

    def run(self):
        if self.args.listen:
            #if listener then listen function called else send function
            self.listen()
        else:
            self.send()

    def send(self):
        #connect target and port
        self.socket.connect((self.args.target,self.args.port))
        if self.buffer:
            #if buffer present then send to reciever
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len=1
                response=''
                while recv_len:
                    data=self.socket.recv(4096)
                    recv_len=len(data)
                    response+=data.decode()
                    if recv_len<4096:
                        break
                    #recieve data from target, if no data then terminate from the loop
                if response:
                    #print response and get input in the shell "> "
                    print(response)
                    buffer=input('> ')
                    buffer+='\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    
    def listen(self):
        self.socket.bind((self.args.target,self.args.port))
        self.socket.listen(5)
        #listen to maximum of 5 instanses
        #thread handling of connected instanses

        while True:
            client_socket,_=self.socket.accept()
            client_thread=threading.Thread(target=self.handle,args=(client_socket,))
            client_thread.start()

    def handle(self,client_socket):
        if self.args.execute:
            output=execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:
            file_buffer=b''
            while True:
                data=client_socket.recv(4096)
                if data:
                    file_buffer+=data
                else:
                    break

            with open(self.args.upload,'wb')as f:
                f.write(file_buffer)
            message=f'saved file {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer=b''
            while True:
                try:
                    client_socket.send(b'BHP: #>  ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer+=client_socket.recv(64)
                    response=execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer=b''

                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()