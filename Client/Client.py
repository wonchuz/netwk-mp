# S16 Jocson & Rebano
# Client File
from socket import *
import threading
import pickle
import select

# prints messages received from the server
def receive_messages(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024).decode('utf-8') # receive msg
            # prints all received messages except for file content
            if message.startswith("Error:"):
                print(message)
            elif message.startswith('[Message]'):
                print(message[9:])
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
    try:
        file = open(filename, 'wb')
        not_found = False

        while True:
            file_data = clientSocket.recv(1024)     # received data
            if not file_data:   # nothing left to receive
                break
            elif file_data == ('Error: File not found in the server.').encode():    # error received
                not_found = True
                break
            file.write(file_data)   # write content on file

            if len(file_data) < 1024:
                break

        file.close()

        if not not_found:
            print('File received from Server: ', filename)
    except IOError:
        print('Error: Unable to retrieve the file from the server')

# send file to server
def store(clientSocket, filename):
    try:
        file = open(filename, 'rb')
        file_data = file.read()
        clientSocket.sendall(file_data) # send content to server
    except IOError:
        print('Error: File not found.')
        
def receive_directory_list(clientSocket):
    try:
        file_list = b''
        while True:
            print('something1')
            
            # Check if there's data available for reading
            ready_to_read, _, _ = select.select([clientSocket], [], [], 0.1)

            if ready_to_read:
                data_chunk = clientSocket.recv(4096)
                if not data_chunk:
                    break
                file_list += data_chunk
                print('something2')
            else:
                # No data available, do something else or break the loop
                print('No data available')
                break

        if not file_list:
            print('Error: No data received.')
            return []
        
        print('something3')
        return pickle.loads(file_list)
    
    except pickle.UnpicklingError:
        print('Error: Failed to unpickle directory list.')
        return []
    except EOFError:
        print('Error: Ran out of input while unpickling directory list.')
        return []
    except IOError:
        print('Error: Failed to receive directory list from the server.')
        return []

def dir(clientSocket):
    try:
        clientSocket.sendall(('/dir').encode())
        server_files = receive_directory_list(clientSocket)

        print('test3')
        for file in server_files:
            print(file)

        print('test4')
    except IOError:
        print('Error: Failed to get directory list from the server.')

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
                    clientSocket.sendall(command_input.encode())
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
                    clientSocket.sendall(command_input.encode())
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
                    dir(clientSocket)
                else:
                    print(not_match_allowed)
            else:
                print(not_connected)
        # none of the commands
        else:
            print(not_found_msg)

if __name__ == "__main__":
    main()
