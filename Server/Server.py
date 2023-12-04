#Server
from socket import *
import os
import threading
import sys


def send_file(connectionSocket, filename):
    print('SENDING FILE')
    print(filename)
    try:
        file = open(filename, 'rb')
        file_data = file.read()
        print(file_data)
        connectionSocket.sendall(file_data)
        print('File was sent') 
    except IOError:
        connectionSocket.send('Error: File not found in the server.'.encode())
        print('File not found')

def handle_command(connectionSocket, command_input):
    decoded = command_input.decode()
    split_command = decoded.strip().split()
    command = split_command[0]

    if command == '/get':
        send_file(connectionSocket, split_command[1])

    # Send file to server
    elif command == '/store':
        # TODO
        try:
            file_data = connectionSocket.recv(1024)
            with open(filename, 'wb') as file:
                while file_data:
                    file.write(file_data)
                    file_data = connectionSocket.recv(1024)
            print(f"File {filename} received and stored.")
        except Exception as e:
            print(f"Error receiving file: {e}")
            
    elif command == '/register':
        # TODO
        pass
    elif command == '/dir':
        # TODO
        pass
    
def handle_client(connectionSocket, addr):
    print('Server: New client connected.')
    try:
        while True:
            print('Waiting for Command')
            try:
                command = connectionSocket.recv(1024)
                print(command)
                if not command:
                    break
                handle_command(connectionSocket, command)

            except IOError:
                pass

    except IOError:
        print('errpr')
    finally:
        connectionSocket.close()

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

if __name__ == "__main__":
    main()