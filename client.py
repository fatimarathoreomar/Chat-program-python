import socket
import threading

# DO NOT DELETE, WILL NEED LATER
#check for correct number of args
# if (len(sys.argv) != 4):
#     print("Incorrect number of arguments")
#     print("Use: client_simple_udp.py <Server Host> <Port> <username>")
#     sys.exit()

#IP = sys.argv[1]
IP = '127.0.0.1'
#PORT = int(sys.argv[2])
PORT = 5000
#userName = sys.argv[3]
#create socket and catch errors

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
FMT = 'utf-8'

def receive():

    #handle username and password
    while True:
        # client.send(userName.encode(FMT)) # use this later
        client.send(input("Enter username: ").encode(FMT)) # delete this later
        client.send(input("Enter password: ").encode(FMT))
        message = client.recv(1024).decode(FMT)
        if message != 'Password incorrect':  # if password is correct break out of loop
            print(message)
            break
        else:
            print("Password incorrect, try again")
    print('Options:')
    print("PM: Public Message, DM: Direct Messaging, EX: Exit")
    op = input("Enter Option: ")

    while(op != 'EX'):
        if op == "PM":
            return # FIXME




receive_thread = threading.Thread(target=receive)
receive_thread.start()

