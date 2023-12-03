#Cllient
from socket import *

def printCommands():
    print('Input Syntax commands:')
    print('/join <server_ip_add> <port>')
    print('/leave') # just do break
    print('/register <handle>')
    print('/store <filename>')
    print('/dir')
    print('/get <filename>')
    print('/?')
    print('\n\n')

def get(s, filename):
    file = open(filename, 'wb')
    error_msg = 'Error: File not found in the server.'
    not_found = False
    buffer = b''

    while True:
        file_data = s.recv(1024)
        if not file_data:
            break
        
        buffer += file_data
        if file_data == error_msg.encode():
            not_found = True
            break

        file.write(file_data)
    
    file.close()
    if not_found:
        print(error_msg)
    else:
        print('File received from Server: ', filename)

def store(s, filename):
    try:
        file = open(filename, 'rb')
        file_data = file.read()
        s.sendall(file_data)
    except IOError:
        print('Error: File not found.')
        
def main():
    while True:
        command_input = input()
        split_command = command_input.strip().split()
        input_length = len(split_command)
        command =  split_command[0]
        connected = False

        not_found_msg = 'Error: Command not found'
        not_match_allowed = 'Error: Command parameters do not match or is not allowed.'

        # not connected
        if connected == False:
            if command == '/join':
                if input_length == 3:
                    try:
                        client_socket = socket(AF_INET, SOCK_STREAM)
                        client_socket.connect((split_command[1], int(split_command[2])))
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

            elif command == '/register' or command == '/store' or command == '/dir' or command == '/get' or command == '?':
                print(not_match_allowed)
            else:
                print(not_found_msg)
        else:
            # join
            if command == "/join":
                if input_length == 3:
                    print('Error: Connection failed. Please disconnect from the server first.')
                else:
                    print(not_match_allowed)

            # leave
            elif command == '/leave':
                if input_length == 1:
                    connected = False
                    client_socket.close()
                    break
                else:
                    print(not_match_allowed)
            
            # /register
            elif command == '/register':
                if input_length == 2:
                    # TODO 
                    pass
                else:
                    print(not_match_allowed)

            # /store
            elif command == '/store':
                if input_length == 2:
                    # TODO 
                    pass
                else:
                    print(not_match_allowed)

            # /dir
            elif command == '/dir':
                if input_length == 1:
                    # TODO 
                    get()
                else:
                    print(not_match_allowed)

            # /get
            elif command == '/get':
                if input_length == 2:
                    # TODO 
                    pass
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

