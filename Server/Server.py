#Server
from socket import *
import threading
import sys
from datetime import datetime
import os
import pickle

clients = {}
clients_lock = threading.Lock() #idk what this does tbh

def send_file(connectionSocket, filename):
    try:
        file = open(filename, 'rb')
        file_data = file.read()
        connectionSocket.sendall(file_data)
    except IOError:
        connectionSocket.sendall('Error: File not found in the server.'.encode())
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
        
        with clients_lock:
            user = clients[connectionSocket]
            # Get the current date and time
            current_datetime = datetime.now()
            # Format the date and time as a string
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            send_to_all_clients(user + '<' + formatted_datetime + '>: Uploaded ' + filename)

        print('File stored.')
    except IOError:
        print('Error: Failed to store file.') # TODO: Print in Server or Client?

def send_to_all_clients(msg):
    for client_socket in clients.keys():
        client_socket.sendall(msg.encode())

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
        register_user(connectionSocket, split_command[1])
    
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
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        clients_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        print(clients_thread)
        clients_thread.start()
    
    serverSocket.close()
    sys.exit()

if __name__ == "__main__":
    main()