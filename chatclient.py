# names="Fatima Rathore (bl1713lh), Pavel Bondarenko (bv2737dg)"
# Chat app using TCP connection.

import socket
import threading
import time
import sys
# DO NOT DELETE, WILL NEED LATER
# check for cort number of args
if (len(sys.argv) != 1):
     print("Incorrect number of arguments")
     print("Use: chatclient.py")
     print("for simplicity the port and host are hardcoded")
     print("the username will also be asked later")
     sys.exit()

# IP = sys.argv[1]
IP = '127.0.0.1'
# PORT = int(sys.argv[2])
PORT = 5555
# userName = sys.argv[3]
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
#print(messagesizecheck("hbxhbhbhh".encode(FMT)))

def listen():
    while True:
        message = client.recv(1024).decode(FMT)
        print(message)
        if message == "No other users online":
            global usersOnline
            usersOnline = False

def receive():
    # handle username and password
    while True:
        # client.send(userName.encode(FMT)) # use this later
        myname=input("Enter username: ").strip().encode(FMT)
        client.send(myname)
        client.send(input("Enter password: ").encode(FMT))
        message = client.recv(1024).decode(FMT)
        if message != 'Password incorrect':  # if password is correct break out of loop
            print(f"Test: {message}")
            break
        else:
            print("Password incorrect, try again")
    #thread to broadcast messages
    broadcast_thread = threading.Thread(target=listen)
    broadcast_thread.start()

    print("-----Options to input-----\nPM: Public Message, DM: Direct Messaging, EX: Exit")
    op = input("Enter Option: ").strip()

    while op != 'EX':
        if op == "PM":
            client.send('PM'.encode(FMT))
            time.sleep(0.1)
            # print(f"Response: {client.recv(1024).decode(FMT)}")
            message=input("Enter message to send: ").strip().encode(FMT)
            #client.send(input("Enter message to send: ").strip().encode(FMT))
            if messagesizecheck(message)==-1:
                print("Message size too big some will be lost")
            client.send(message)
            time.sleep(0.1)
            # response = client.recv(1024).decode(FMT)
            # print(f"Response: {response}")
        elif op == "DM":
            client.send('DM'.encode(FMT))
            time.sleep(0.1)
            global usersOnline
            if usersOnline:
                name=input("Enter user: ").strip().encode(FMT)
                while name==myname:
                    print("Select a name from list!why do you want to message to yourself ")
                    name = input("Enter user: ").strip().encode(FMT)

                client.send(name)

                #client.send(input("Enter message to send: ").strip().encode(FMT))
                message = input("Enter message to send: ").strip().encode(FMT)
                if messagesizecheck(message) == -1:
                    print("Message size too big some will be lost")
                client.send(message)
                time.sleep(0.1)
            usersOnline = True
        else:
            print("Not valid option")
        print("-----Options to input-----\nPM: Public Message, DM: Direct Messaging, EX: Exit")
        op = input("Enter Option: ").strip()

    client.send('EX'.encode(FMT))
    broadcast_thread.join()
    return


#lock=threading.Lock()
receive_thread = threading.Thread(target=receive)
receive_thread.start()

receive_thread.join()