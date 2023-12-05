#Cllient
from socket import *
import pickle
import select

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

def get(clientSocket, filename):
    clientSocket.sendall(('/get ' + filename).encode())

    try:
        file = open(filename, 'wb')
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

            if len(file_data) < 1024:
                break

        file.close()

        if not_found:
            print(error_msg)
        else:
            print('File received from Server: ', filename)

    except IOError:
        print('Error: Unable to retrieve the file from the server')

def store(clientSocket, filename):
    try:
        file = open(filename, 'rb')
        clientSocket.sendall(('/store ' + filename).encode())
        file_data = file.read()
        clientSocket.sendall(file_data)
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
    connected = False
    while True:
        command_input = input()
        split_command = command_input.strip().split()
        input_length = len(split_command)
        command =  split_command[0]

        not_found_msg = 'Error: Command not found'
        not_match_allowed = 'Error: Command parameters do not match or is not allowed.'

        # not connected
        if connected == False:
            if command == '/join':
                if input_length == 3:
                    try:
                        clientSocket = socket(AF_INET, SOCK_STREAM)
                        clientSocket.connect((split_command[1], int(split_command[2])))
                        print('Connection to the File Exchange Server is successful!')
                        connected = True
                    except IOError:
                        print('Error: Connection to the Server has failed! Please check IP Address and Port Number')
                else:
                    print(not_match_allowed)

            elif command == '/leave':
                if input_length == 1:
                    print('Error: Disconnected failed. Please connect to the server first.')
                else:
                    print(not_match_allowed)

            elif command == '/?':
                if input_length == 1:
                    printCommands()
                else:
                    print(not_match_allowed)
            
            elif command == '/register' or command == '/store' or command == '/dir' or command == '/get':
                print(not_match_allowed)
            else:
                print(not_found_msg)
        # connected to server
        else:
            # /join
            if command == "/join":
                if input_length == 3:
                    print('Error: Connection failed. Please disconnect from the server first.')
                else:
                    print(not_match_allowed)

            # /leave
            elif command == '/leave':
                if input_length == 1:
                    connected = False
                    clientSocket.sendall(('/leave').encode())
                    clientSocket.close()
                    print('Connection closed. Thank you!')
                    break
                else:
                    print(not_match_allowed)
            
            # /register
            elif command == '/register':
                if input_length == 2:
                    clientSocket.sendall(('/register ' + split_command[1]).encode())
                    print(clientSocket.recv(1024).decode())
                else:
                    print(not_match_allowed)

            # /store
            elif command == '/store':
                if input_length == 2:
                    store(clientSocket, split_command[1])
                else:
                    print(not_match_allowed)

            # /dir
            elif command == '/dir':
                if input_length == 1:
                    # TODO is this right?
                    dir(clientSocket)
                else:
                    print(not_match_allowed)

            # /get
            elif command == '/get':
                if input_length == 2:
                    get(clientSocket, split_command[1])
                else:
                    print(not_match_allowed)

            # /?
            elif command == '/?':
                if input_length == 1:
                    printCommands()
                else:
                    print(not_match_allowed)
            
            # none of the commands
            else:
                print(not_found_msg)

if __name__ == "__main__":
    main()