#Server
from socket import *
import os
import threading
import sys


def send_file(connectionSocket, filename):
    try:
        file = open(filename, 'rb')
        file_data = file.read()
        connectionSocket.sendall(file_data)
        print('File was sent') 
    except IOError:
        connectionSocket.send('Error: File not found in the server.'.encode())
        print('File not found')

def handle_command(connectionSocket, command_input):
    split_command = command.strip().split()
    command = split_command[0]

    if command.startsWith('/'):
        pass
    
def handle_client(connectionSocket, addr):
    print('Server: New client connected.')
    while True:
        try:
            command = 'test'
            if not command:
                break
            handle_command(connectionSocket)
            

        except IOError:
            pass
            #connectionSocket.close()

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = 9999
    serverSocket.bind(('127.0.0.1', serverPort))
    serverSocket.listen()
    
    clients = []
    clients_lock = threading.Lock()
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        clients = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        clients.start()
    
    serverSocket.close()
    sys.exit()

