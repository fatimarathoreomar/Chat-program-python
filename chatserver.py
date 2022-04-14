# names="Fatima Rathore (bl1713lh), Pavel Bondarenko (bv2737dg)"
# Chat app using TCP connection.

import threading
import socket
import sys

#check for correct number of args
if (len(sys.argv) != 2):
     print("Incorrect number of arguments")
     print("Enter arguments: <chatcserver.py> <PORT>")
     sys.exit()

PORT = int(sys.argv[1])  # port is an argument
IP = '127.0.0.1' # localhost
FMT = 'utf-8' # encoding format

# make socket
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    server.bind((IP, PORT))
    server.listen()
except socket.error:
    print("Error creating socket")
    sys.exit(1)

#keep track of currently connected clients here
clients = []

# PM for all, skips user who sent message
def broadcast(message, user):
    # loop through connected clients
    for client in clients:
        if client == user: #skip the client broadcasting the message
            continue
        client['client'].send('\nIncoming broadcast:'.encode(FMT))
        client['client'].send(message)

# DM to particular user
def broadcastToUser(message, toUser, fromUser):
    # loop through all users to find the correct one, return false if not found
    for client in clients:
        if client['nickname'] == toUser:
            client['client'].send(f'\nMessage from {fromUser}: {message}'.encode(FMT))
            return True
    return False

# checks usernames to see if it exists on file
def checkUsernames(user):
    with open('users.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip().split(' ')
        if user == line[0]:
            f.close()
            return True
    f.close()
    return False

# checks the password of given username
def checkPassword(user, passWord):
    with open('users.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip().split(' ')
        if user == line[0]:
            if passWord == line[1]:
                f.close()
                return True
            else:
                f.close()
                return False
    f.close()
    return False

# creates user and adds to file
def createUser(userName, passWord):
    with open('users.txt', 'a+') as f:
        f.seek(0)
        data=f.read()
        if len(data) > 0:
            f.write("\n")
        f.write(f'{userName} {passWord}')

# thread to handle communication between clients
def handle(client):
    #first handle username/password validation
    while True:
        userName = client.recv(1024).decode(FMT)
        passWord = client.recv(1024).decode(FMT)
        if checkUsernames(userName): # see if userName exists
            if not checkPassword(userName, passWord): # check if password matches
                client.send("Password incorrect".encode(FMT))
            else: # username exists but password is wrong
                client.send("Password correct".encode(FMT))
                break
        else: # username doesn't exist, created new username
            createUser(userName, passWord)
            client.send("Created new user".encode(FMT))
            break
    # password validated
    #add user to list of connected clients
    user = {
        'client': client,
        'nickname': userName
    }
    clients.append(user)

    # receive option from user
    op = client.recv(1024).decode(FMT)
    # while the command is not EX to exit
    while op != 'EX':
        # send public message broadcast
        if op == "PM":
            client.send("Ready".encode(FMT))
            message = client.recv(1024)
            # broadcast message
            broadcast(message, user)
            client.send("Message sent".encode(FMT))
        # Direct message
        elif op == "DM":
            # if there is no one to broadcast to
            if len(clients) == 1:
                client.send("No other users online".encode(FMT))
            else:
                client.send("Other users:".encode(FMT))
                num = 1
                # send the list of all the users currently connected
                for i in range(len(clients)):
                    if clients[i] == user:
                        continue # we only want to send OTHER users
                    client.send(f"{num}. {clients[i]['nickname']}".encode(FMT))
                    num += 1
                # get nickname to broadcast to
                userToSend = client.recv(1024).decode(FMT)
                message = client.recv(1024).decode(FMT)
                sent = broadcastToUser(message, userToSend, user['nickname'])
                if sent:
                    client.send(f"Message sent to user '{userToSend}'".encode(FMT))
                else:
                    client.send(f"User not found".encode(FMT))
        # next command/option from user
        op = client.recv(1024).decode(FMT)

    # if EX command, breaks out of loop, user removed
    clients.remove(user)
    client.send("you can exit".encode(FMT))

# accept new client connections
def accept():
    print("Server is ready to receive on port ", PORT)
    while True:
        print('Waiting...')
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


accept()
server.close()