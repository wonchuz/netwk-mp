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
    except IOError:
        connectionSocket.send('Error: File not found in the server.'.encode())
        print('File not found')

def store_file(connectionSocket, filename):
    try:
        file = open(filename, 'wb')

        while True:
            file_data = connectionSocket.recv(1024)

            if not file_data:
                break

            file.write(file_data)

            if len(file_data) < 1024:
                break

        file.close()
        # TODO
        # User1<2023-11-06 16:48:05>: Uploaded Hello.txt
        # must send to all users connected?
        print('File stored.')
    except IOError:
        print('Error: Failed to store file.') # TODO: Print in Server or Client?

def send_to_all_clients(msg, clients):
    for client_socket in clients:
        client_socket.send(msg.encode())
    pass
            

def handle_command(connectionSocket, command_input):
    decoded = command_input.decode()
    split_command = decoded.strip().split()
    command = split_command[0]

    # Send file to client
    if command == '/get':
        send_file(connectionSocket, split_command[1])

    # Store file to server
    elif command == '/store':
        store_file(connectionSocket, split_command[1])

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
        print('Error')
    finally:
        connectionSocket.close()

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = 12345
    serverSocket.bind(('127.0.0.1', serverPort))
    serverSocket.listen()
    
    clients = []
    clients_lock = threading.Lock() #idk what this does tbh
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        clients = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        clients.start()
    
    serverSocket.close()
    sys.exit()

if __name__ == "__main__":
    main()