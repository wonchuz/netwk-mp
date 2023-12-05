# S16 Jocson & Rebano
# Client File
from socket import *
import threading

# prints messages received from the server
def receive_messages(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024).decode() # receive msg
            # prints all received messages except for file content
            if message.startswith("Error:"):
                print(message)
            elif message.startswith('[Message] '):
                print(message[10:])
        except IOError:
            print('Error: Failed to receive message from the server.')

# prints commands
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

# gets a file from the server
def get(clientSocket, filename):
    clientSocket.sendall(('/get ' + filename).encode())
    try:
        with open(filename, 'wb') as file:
            error_msg = 'Error: File not found in the server.'
            not_found = False
            while True:
                file_data = clientSocket.recv(1024)
                if not file_data:
                    break
                
                elif file_data == error_msg.encode():
                    not_found = True
                    break
                file.write(file_data)
            file.close()
            if not not_found:
                print('File received from Server: ', filename)
    except IOError:
        print('Error: Unable to retrieve the file from the server')

# send file to server
def store(clientSocket, filename):
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
            clientSocket.sendall(('/store ' + filename).encode())
            clientSocket.sendall(file_data) # send content to server
    except IOError:
        print('Error: File not found.')

def main():
    connected = False   # not connected to server
    registered = False  # not registered in server
    clientSocket = socket(AF_INET, SOCK_STREAM)

    while True:
        command_input = input()
        split_command = command_input.strip().split()
        input_length = len(split_command)
        command =  split_command[0]

        not_found_msg = 'Error: Command not found'
        not_match_allowed = 'Error: Command parameters do not match or is not allowed.'
        not_connected = 'Error: Please connect to the server first.'

        if command == '/join':
            if connected:
                if input_length == 3:
                    print('Error: Connection failed. Please disconnect from the server first.')
                else:
                    print(not_match_allowed)
    
            else:
                if input_length == 3:
                    try:
                        clientSocket.connect((split_command[1], int(split_command[2])))
                        receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,))
                        receive_thread.start()
                        print('Connection to the File Exchange Server is successful!')
                        connected = True
                    except IOError:
                        print('Error: Connection to the Server has failed! Please check IP Address and Port Number')
                else:
                    print(not_match_allowed)
        elif command == '/leave':
            if input_length == 1:
                if connected:
                    connected = False
                    clientSocket.sendall(('/leave').encode())
                    clientSocket.close()
                    print('Connection closed. Thank you!')
                    break
                else:
                    print('Error: Disconnected failed. Please connect to the server first.')
            else:
                print(not_match_allowed)
        elif command == '/?':
            if input_length == 1:
                    printCommands()
            else:
                print(not_match_allowed)
        elif command == '/register':
            if connected and not registered:
                if input_length == 2:
                    clientSocket.sendall(command_input.encode())
                    registered = True
                else:
                    print(not_match_allowed)
            elif connected and registered:
                print('Error: Registration Failed. You already registered.')
            else:
                print(not_connected)
        elif command == '/get':
            if connected and registered:
                if input_length == 2:
                    get(clientSocket, split_command[1])
                else:
                    print(not_match_allowed)
            elif connected and not registered:
                print(not_match_allowed)
            else:
                print(not_connected)
        elif command == '/store':
            if connected and registered:
                if input_length == 2:
                    store(clientSocket, split_command[1])
                else:
                    print(not_match_allowed)
            elif connected and not registered:
                print(not_match_allowed)
            else:
                print(not_connected)
        elif command == '/dir':
            if connected:
                if input_length == 1:
                    clientSocket.sendall(('/dir').encode())
                else:
                    print(not_match_allowed)
            else:
                print(not_connected)
        # none of the commands
        else:
            print(not_found_msg)

if __name__ == "__main__":
    main()
