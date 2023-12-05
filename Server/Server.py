# S16 Jocson & Rebano
# Server File
from socket import *
import os
import threading
import sys
from datetime import datetime

clients = {}
clients_lock = threading.Lock()

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
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            broadcast_msg('[Message] ' + user + '<' + formatted_datetime + '>: Uploaded ' + filename)

        print('File stored.')
    except IOError:
        print('Error: Failed to store file.')

def broadcast_msg(msg):
    for client_socket in clients.keys():
        try:
            client_socket.sendall(msg.encode())
        except IOError:
            print('Failed to send message to client.')
                
def register_user(connectionSocket, user):
    with clients_lock:
        if user in clients.values():
            connectionSocket.sendall('Error: Registration Failed. Handle or alias already exists'.encode())
        else:
            clients[connectionSocket] = user
            broadcast_msg('[Message] ' + 'Welcome ' + user + '!')

def get_directory_list():
    current_directory = os.getcwd()
    return os.listdir(current_directory)

def req_dir(connectionSocket):
    try:
        file_list = get_directory_list()
        serialized_file_list = pickle.dumps(file_list)
        connectionSocket.sendall(serialized_file_list)
    except IOError:
        print('Error: Failed to send directory list.')

def handle_command(connectionSocket, command_input):
    decoded = command_input.decode()
    split_command = decoded.strip().split()
    command = split_command[0]

    if command == '/get':
        send_file(connectionSocket, split_command[1])
    elif command == '/store':
        store_file(connectionSocket, split_command[1])
    elif command == '/register':
        register_user(connectionSocket, split_command[1])
    elif command == '/dir':
        req_dir(connectionSocket)
    elif command == '/leave':
        user = clients[connectionSocket]
        del clients[connectionSocket]
        broadcast_msg('[Message] ' + user + ' disconnected.')
    
def handle_client(connectionSocket, addr):
    print('New client connected.')
    try:
        while True:
            try:
                command = connectionSocket.recv(1024)
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
        clients_thread.start()
        
    
    serverSocket.close()
    sys.exit()

if __name__ == "__main__":
    main()