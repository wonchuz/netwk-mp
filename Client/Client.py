# S16 Jocson & Rebano
# Client File
from socket import *
import threading
import os

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

# prints messages received from the server
def receive_messages(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024).decode() # receive msg
            if message.endswith('found in server.'):
                get(clientSocket, message.split()[0])
            else: 
                print(message)
        except IOError:
            print('Error: Failed to receive message from the server.')
            break

# send file to server
def store(clientSocket, filename):
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
            clientSocket.sendall(('/store ' + filename).encode())
            clientSocket.sendall(file_data) # send content to server
    except IOError:
        print('Error: File not found.')

def get(clientSocket, filename):
    try:
        with open(filename, 'wb') as file:
            while True:
                file_data = clientSocket.recv(1024)
                if not file_data:
                    break
                file.write(file_data)
                if len(file_data) < 1024:
                    break
        print('File saved.')
    except IOError:
        print('Error: Unable to retrieve the file from the server')


def main():
    connected = False   # not connected to server
    registered = False  # not registered in server
    clientSocket = socket(AF_INET, SOCK_STREAM)

    while True:
        try:
            command_input = input()
            split_command = command_input.strip().split()
            input_length = len(split_command)
            command =  split_command[0]

            # messages
            not_found_msg = 'Error: Command not found'
            not_match_allowed = 'Error: Command parameters do not match or is not allowed.'
            not_connected = 'Error: Please connect to the server first.'

            # /join
            if command == '/join':
                if input_length == 3:
                    if connected:
                        print('Error: Connection failed. Please disconnect from the server first.')
                    # not connected
                    else:
                        try:
                            clientSocket.connect((split_command[1], int(split_command[2])))
                            receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,))
                            receive_thread.start()
                            print('Connection to the File Exchange Server is successful!')
                            connected = True
                        except IOError:
                            print('Error: Connection to the Server has failed! Please check IP Address and Port Number')      
                else:
                    print(not_match_allowed) # invalid parameters

            # /leave
            elif command == '/leave':
                if input_length == 1:
                    if connected:
                        connected = False
                        clientSocket.sendall(('/leave').encode())
                        if clientSocket.recv(1024).decode().startswith('Connection closed'):
                            clientSocket.close()
                        break
                    else:
                        print('Error: Disconnected failed. Please connect to the server first.')
                else:
                    print(not_match_allowed)

            # /register
            elif command == '/register':
                if input_length == 2:
                    if connected and not registered:
                        clientSocket.sendall(command_input.encode())
                        if clientSocket.recv(10.24).decode().startswith('Welcome'):
                            registered = True
                    elif connected and registered:
                        print('Error: Registration Failed. You already registered.')
                    else:
                        print(not_connected)
                else:
                    print(not_match_allowed)
                    
            # /store
            elif command == '/store':
                if input_length == 2:
                    if connected and registered:
                        store(clientSocket, split_command[1])
                    elif connected and not registered:
                        print(not_match_allowed)
                    else:
                        print(not_connected)
                else:
                    print(not_match_allowed)

            # /dir
            elif command == '/dir':
                if input_length == 1:
                    if connected and registered:
                        clientSocket.sendall(('/dir').encode())
                    elif connected and not registered:
                        print(not_match_allowed)
                    else:
                        print(not_connected)
                else:
                    print(not_match_allowed) 

            # /get
            elif command == '/get':
                if input_length == 2:
                    if connected and registered:
                        clientSocket.sendall(('/get ' + split_command[1]).encode())
                    elif connected and not registered:
                        print(not_match_allowed)
                    else:
                        print(not_connected)
                else:
                    print(not_match_allowed)

            # /?
            elif command == '/?':
                if input_length == 1:
                    printCommands()
                else:
                    print(not_match_allowed)

            elif command == '/broadcast':
                if connected and registered:
                    clientSocket.sendall('/broadcast ' + split_command[1:].encode())
                elif connected and not registered:
                    print(not_match_allowed)
                else:
                    print(not_connected)
            
            else:
                print(not_found_msg)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
