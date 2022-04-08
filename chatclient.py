# names="Fatima Rathore (bl1713lh), Pavel Bondarenko (bv2737dg)"
# Chat app using TCP connection.

import socket
import threading
import time
import sys
# DO NOT DELETE, WILL NEED LATER
# check for cort number of args
# if (len(sys.argv) != 4):
#     print("Incorrect number of arguments")
#     print("Use: client_simple_udp.py <Server Host> <Port> <username>")
#     sys.exit()

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
        client.send(input("Enter username: ").encode(FMT))  # delete this later
        client.send(input("Enter password: ").encode(FMT))
        message = client.recv(1024).decode(FMT)
        if message != 'Password incorrect':  # if password is correct break out of loop
            print(f"Test: {message}")
            break
        else:
            print("Password incorrect, try again")

    broadcast_thread = threading.Thread(target=listen)
    broadcast_thread.start()

    print("-----Options to input-----\nPM: Public Message, DM: Direct Messaging, EX: Exit")
    op = input("Enter Option: ").strip()

    while op != 'EX':
        if op == "PM":
            client.send('PM'.encode(FMT))
            time.sleep(0.1)
            # print(f"Response: {client.recv(1024).decode(FMT)}")
            client.send(input("Enter message to send: ").encode(FMT))
            time.sleep(0.1)
            # response = client.recv(1024).decode(FMT)
            # print(f"Response: {response}")
        elif op == "DM":
            client.send('DM'.encode(FMT))
            time.sleep(0.1)
            global usersOnline
            if usersOnline:
                client.send(input("Enter user: ").encode(FMT))
                client.send(input("Enter message to send: ").encode(FMT))
                time.sleep(0.1)
            usersOnline = True
        else:
            print("Not valid option")
        print("-----Options to input-----\nPM: Public Message, DM: Direct Messaging, EX: Exit")
        op = input("Enter Option: ").strip()

    client.send('EX'.encode(FMT))
    broadcast_thread.join()
    return

# we don't actually need a separte thread to do this, but that's ok
# we will need to add a separate thread later for listening to broadcasts
#lock=threading.Lock()
receive_thread = threading.Thread(target=receive)
receive_thread.start()

receive_thread.join()