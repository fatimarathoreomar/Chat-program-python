import threading
import socket

# DO NOT DELETE, WILL NEED LATER
#check for correct number of args
# if (len(sys.argv) != 2):
#     print("Incorrect number of arguments")
#     print("Use: server_simple_udp.py <Port>")
#     sys.exit()
#PORT = int(sys.argv[1])  # port is an argument

IP = '127.0.0.1' # localhost
PORT = 5555 #for now, using hardcoded port
FMT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

#keep track of currently connected clients here
clients = []

def broadcast(message, user):
    for client in clients:
        if client == user: #skip the client broadcasting the message
            continue
        client['client'].send(message)

def getClientList():
    clientString = ''
    for i in range(len(clients)):
        clientString += f"{i + 1}. {clients[i]['nickname']}\n"
    return clientString

def checkUsernames(user):
    with open('users.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip().split(' ')
        print(f"stuff: {user} {line[0]}")
        if user == line[0]:
            f.close()
            return True
    f.close()
    return False

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

def createUser(userName, passWord):
    with open('users.txt', 'a') as f:
        f.write(f'{userName} {passWord}\n')

def handle(client):
    #first handle username/password situation
    while True:
        userName = client.recv(1024).decode(FMT)
        passWord = client.recv(1024).decode(FMT)
        if checkUsernames(userName): # see if userName exists
            if not checkPassword(userName, passWord): # check if password matches
                client.send("Password incorrect".encode(FMT))
            else:
                client.send("Password correct".encode(FMT))
                break
        else: # username doesn't exist, created new username
            createUser(userName, passWord)
            client.send("Created new user".encode(FMT))
            break
    #If password was correct we should end up here
    #add to list of connected clients
    user = {
        'client': client,
        'nickname': userName
    }
    clients.append(user)

    op = client.recv(1024).decode(FMT)
    while op != 'EX':
        if op == "PM":
            client.send("Ready".encode(FMT))
            message = client.recv(1024)
            broadcast(message, user)
            client.send("Message sent".encode(FMT))
        if op == "DM":
            return
        op = client.recv(1024).decode(FMT)

    #user chose exit
    clients.remove(user)




def receive():
    print("Server is ready to receive on port ", PORT)
    while True:
        print('Waiting...')
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()