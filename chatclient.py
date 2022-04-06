import socket
import threading

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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
client.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
FMT = 'utf-8'


def listen():
    lock.acquire()
    while True:
        message = client.recv(1024).decode(FMT)
        print(message)
    lock.release()

def receive():
    # handle username and password
    while True:
        # client.send(userName.encode(FMT)) # use this later
        lock.acquire()
        client.send(input("Enter username: ").strip().encode(FMT))  # delete this later
        client.send(input("Enter password: ").strip().encode(FMT))
        message = client.recv(1024).decode(FMT)
        if message != 'Password incorrect':  # if password is correct break out of loop
            print(f"Test: {message}")
            break
        else:
            print("Password incorrect, try again")
        lock.release()

    print("-----Options to input-----\nPM: Public Message, DM: Direct Messaging, EX: Exit")
    op = input("Enter Option: ").strip()

    while op != 'EX':
        if op == "PM":
            client.send('PM'.encode(FMT))
            #lock.acquire()
            print(f"Response: {client.recv(1024).decode(FMT)}")
            client.send(input("Enter message to send: ").encode(FMT))
            response = client.recv(1024).decode(FMT)
            print(f"Response: {response}")
            #lock.release()
        if op == "DM":
            client.send('DM'.encode(FMT))
            #lock.acquire()
            #getting names of online users
            gflag=1
            print(f"Active users are following\n")
            t=client.recv(1024).decode(FMT)
            print(t)
            m = t.split(",")
            #names=m
            names=[]
            names.extend(m)
            if len(names) == 1:
                gflag=0
                print("No other user online")
                client.send("No other user online".encode(FMT))
                #client.send("No other user online".encode(FMT))
            #if only one user is online that is you then do nothing
            if gflag==1:

               name=input("Who do you want to message privately: ").strip()
               while name not in names:
                    name = input("This user is either not active or does not exist,try again!: ")
               client.send(name.encode(FMT))
               response = client.recv(1024).decode(FMT)

               print(f"Response: {response}")
               if response=="User is online":
                   message = input("Enter message to send: ").encode(FMT)
                   client.send(message)
                   response = client.recv(1024).decode(FMT)
                   print(f"Response: {response}")
            #lock.release()

        print("-----Options to input-----\nPM: Public Message, DM: Direct Messaging, EX: Exit")
        op = input("Enter Option: ").strip()

    client.send('EX'.encode(FMT))
    response = client.recv(1024).decode(FMT)
    print(f"Response: {response}")
    return

# we don't actually need a separte thread to do this, but that's ok
# we will need to add a separate thread later for listening to broadcasts
lock=threading.Lock()
receive_thread = threading.Thread(target=receive)
receive_thread.start()

#broadcast_thread = threading.Thread(target=listen)
#broadcast_thread.start()

#receive_thread.join()
#broadcast_thread.join()