# S16 Jocson & Rebano
# Server File

from socket import *
import threading
import sys
import tkinter as tk
from datetime import datetime
import os
import pathlib

clients = {}
clients_lock = threading.Lock()

# send message to all clients connected
def broadcast_msg(msg):
    for client_socket in clients.keys():
        try:
            client_socket.sendall(msg.encode())
            print('Broadcasted message')
        except IOError:
            print('Failed to send message to client.')

# /register
def register_user(connectionSocket, user):
    with clients_lock:
        if user in clients.values():
            connectionSocket.sendall('Error: Registration Failed. Handle or alias already exists'.encode())
        else:
            clients[connectionSocket] = user
            broadcast_msg('Welcome ' + user + '!')
            print(user + ' registered!')

# /store
def store_file(connectionSocket, filename):
    try:
        with open(filename, 'wb') as file:
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
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            broadcast_msg(user + '<' + formatted_datetime + '>: Uploaded ' + filename)
        print('File stored.')
        
    except IOError:
        print('Error: Failed to store file.')

# /dir
def send_directory(connectionSocket):
    try:
        files = [f.name for f in pathlib.Path(os.getcwd()).iterdir() if f.is_file()]
        msg = '\nServer Directory:\n'
        for file in files:
            if file != 'Server.py':
                msg += file + '\n'
        connectionSocket.sendall(msg.encode())    
    except Exception as e:
        print(f'Error: Failed to send directory - {e}')

# /send
def send_file(connectionSocket, filename):
    try:
        with open(filename, 'rb') as file:
            connectionSocket.sendall((filename + ' found in server.').encode())
            while True:
                file_data = file.read(1024)
                if not file_data:
                    break
                connectionSocket.sendall((file_data))
            print('File sent')
    except IOError:
        connectionSocket.sendall('Error: File not found in the server.'.encode())
        print('File not found')

def handle_command(connectionSocket, command_input):
    decoded = command_input.decode()
    split_command = decoded.strip().split()
    command = split_command[0]

    # /leave
    if command == '/leave':
        user = clients[connectionSocket]
        del clients[connectionSocket]
        if user == 'User':
            broadcast_msg('A user disconnected.')
        else:
            broadcast_msg(user + ' disconnected.')
        connectionSocket.sendall('Connection closed. Thank you!'.encode())

    # /register
    elif command == '/register':
        register_user(connectionSocket, split_command[1])

    # /store
    elif command == '/store':
        store_file(connectionSocket, split_command[1])

    # /dir
    elif command == '/dir':
        send_directory(connectionSocket)

    # /get
    elif command == '/get':
        send_file(connectionSocket, split_command[1])

    # /?
    

def handle_client(connectionSocket, addr):
    print('New client connected.')
    clients[connectionSocket] = 'User'
    try:
        while True:
            try:
                command = connectionSocket.recv(1024)
                if not command:
                    break
                handle_command(connectionSocket, command)

            except IOError:
                pass

    except Exception as e:
        print(f'Error occurred in handle_client - {e}')
    
    connectionSocket.close()

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = 12345
    serverSocket.bind(('127.0.0.1', serverPort))
    serverSocket.listen()
    server_running = True
    
    try:
        while True:
            connectionSocket, addr = serverSocket.accept()
            clients_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
            clients_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
        server_running = False
        serverSocket.close()
        sys.exit()

if __name__ == "__main__":
    main()