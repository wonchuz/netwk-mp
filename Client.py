#Cllient
import socket

def printCommands():
    print('Input Syntax commands:')
    print('/join <server_ip_add> <port>')
    print('/leave')
    print('/register <handle>')
    print('/store <filename>')
    print('/dir')
    print('/get <filename>')
    print('/?')
    print('\n\n')

def join(server_ip, port):
    try:
        s.connect((host, port))
        print('Connection closed. Thank you!')
    except IOError:
        print('Error: Connection to the Server has failed! Please check IP Address and Port Number')











s = socket.socket()
host = socket.gethostname()
port = 9999

s.connect((host, port))
print(s.recv(1024))     #1024 is bufsize or max amount of data to be received