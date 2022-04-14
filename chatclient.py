# names="Fatima Rathore (bl1713lh), Pavel Bondarenko (bv2737dg)"
# Chat app using TCP connection.

import socket
import threading
import time
import sys

# check for cort number of args
if (len(sys.argv) != 4):
     print("Incorrect number of arguments")
     print("Enter arguments: <chatclient.py> <Server_Name> <Port> <Username>")
     sys.exit()

IP = sys.argv[1]
PORT = int(sys.argv[2])
myName = sys.argv[3]
# create socket and catch errors
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    client.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
except:
    print("Error creating socket")
    sys.exit(1)


FMT = 'utf-8'
usersOnline = True
myname="test"


#message size check
#cannot recieve a message bigger than 1024 bytes
def messagesizecheck(message):
    #print(len(message))
    if(len(message)>1024):
        return -1
    else:
        return 1

# thread to listen to all messages from server after password validated
def listen():
    while True:
        message = client.recv(1024).decode(FMT)
        print(message)
        if message == "No other users online":
            global usersOnline
            usersOnline = False
        elif message == 'you can exit':
            break

def receive():
    # handle username and password
    while True:
        client.send(myName.encode(FMT)) # use this later
        client.send(input("Enter password: ").encode(FMT))
        message = client.recv(1024).decode(FMT)
        if message != 'Password incorrect':  # if password is correct break out of loop
            print(f"{message}")
            break
        else:
            print("Password incorrect, try again")
    #thread to broadcast messages
    broadcast_thread = threading.Thread(target=listen)
    broadcast_thread.start()

    print("-----Options to input-----\nPM: Public Message, DM: Direct Messaging, EX: Exit")
    op = input("Enter Option: ").strip()

    # loop while EX is not chosen
    while op != 'EX':
        # public message
        if op == "PM":
            client.send('PM'.encode(FMT))
            time.sleep(0.1)
            # message to PM to everyone
            message=input("Enter message to send: ").strip().encode(FMT)
            # check size of message
            if messagesizecheck(message)==-1:
                print("Message size too big some will be lost")
            client.send(message)
            # sleep to make sure the response comes in before menu
            time.sleep(0.1)

        # Direct Message
        elif op == "DM":
            client.send('DM'.encode(FMT))
            time.sleep(0.1)
            global usersOnline
            # if there are other users online
            if usersOnline:
                name = input("Enter user: ")
                # make sure person can't DM themselves
                while name == myname:
                    print("Select a name from list! Why do you want to message yourself?")
                    name = input("Enter user: ")

                client.send(name.strip().encode(FMT))
                # send DM
                message = input("Enter message to send: ").strip().encode(FMT)
                # see if message is more than 1024 bytes
                if messagesizecheck(message) == -1:
                    print("Message size too big some will be lost")
                client.send(message)
                time.sleep(0.1)
            usersOnline = True
        else:
            print("Not valid option")
        print("-----Options to input-----\nPM: Public Message, DM: Direct Messaging, EX: Exit")
        op = input("Enter Option: ").strip()
    # send EX command and exit
    client.send('EX'.encode(FMT))
    broadcast_thread.join()
    return

receive()
client.close()