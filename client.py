import socket
import threading

# DO NOT DELETE, WILL NEED LATER
# check for correct number of args
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
FMT = 'utf-8'


def listen():
    while True:
        message = client.recv(1024).decode(FMT)
        print(message)


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
    print('Options:')
    print("PM: Public Message, DM: Direct Messaging, EX: Exit")
    op = input("Enter Option: ")

    while op != 'EX':
        if op == "PM":
            client.send('PM'.encode(FMT))
            print(f"Response: {client.recv(1024).decode(FMT)}")
            client.send(input("Enter message to send: ").encode(FMT))
            response = client.recv(1024).decode(FMT)
            print(f"Response: {response}")
        if op == "DM":
            return
        else:
            print("Not valid option")
        op = input("Enter Option: ")

    client.send('EX'.encode(FMT))


# we don't actually need a separte thread to do this, but that's ok
# we will need to add a separate thread later for listening to broadcasts
receive_thread = threading.Thread(target=receive)
receive_thread.start()

broadcast_thread = threading.Thread(target=listen)
broadcast_thread.start()

receive_thread.join()
