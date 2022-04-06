import threading
import socket
name="fatima_rathore"
star_id="bl1713lh"
name2="Pavel_bond"
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
server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
server.bind((IP, PORT))
server.listen()

#keep track of currently connected clients here
clients = []

def broadcast(message, user):
    lock.acquire()
    for client in clients:
        if client == user: #skip the client broadcasting the message
            continue
        client['client'].send(message)
    lock.release()

def broadcasttospecificuser(message, user):
    lock.acquire()
    for client in clients:
        if client == user: #skip the client broadcasting the message
           client['client'].send(message)
    lock.release()

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
        f.write(f'{userName} {passWord}')

def handle(client):
    #first handle username/password situation
    while True:

        userName = client.recv(1024).decode(FMT)
        passWord = client.recv(1024).decode(FMT)
        if checkUsernames(userName): # see if userName exists
            if not checkPassword(userName, passWord): # check if password matches
                client.send("Password incorrect".encode(FMT))
            else:
                lock.acquire()
                client.send("Password correct".encode(FMT))
                user = {
                    'client': client,
                    'nickname': userName
                }

                clients.append(user)
                lock.release()
                break
        else: # username doesn't exist, created new username
            lock.acquire()
            createUser(userName, passWord)
            user = {
                'client': client,
                'nickname': userName
            }

            clients.append(user)
            lock.release()
            client.send("Created new user".encode(FMT))
            break
    #If password was correct we should end up here
    #add to list of connected clients


    op = client.recv(1024).decode(FMT)
    while True:
        if op == "PM":
            lock.acquire()
            client.send("Ready".encode(FMT))
            message = client.recv(1024)
            broadcast(message, user)
            client.send("Message sent".encode(FMT))
            lock.release()
        if op == "DM":
            #over here sending online users to client
            #client.send("Ready for DM".encode(FMT))
            #clientnames=[]
            #lock.acquire()
            for i in range(len(clients)):
                #clientnames.append(clients[i]['nickname'])
                if (i!=(len(clients)-1)):
                   client.send((clients[i]['nickname']+",").encode(FMT))
                else:
                    client.send((clients[i]['nickname']).encode(FMT))



            #lock.release()
            #client.send(",stop".encode(FMT))
            #now client should select a user name and send one back
            selectedname=client.recv(1024).decode(FMT)

            print(selectedname)
            if selectedname!="No other user online":
               testFlag=0
               #checking if the user is still online
               for i in range(len(clients)):
                   if selectedname==clients[i]['nickname']:
                       client.send("User is online".encode(FMT))
                       uu=clients[i]
                       testFlag = 1
                       break
               if testFlag == 0 :
                  client.send("User is offline".encode(FMT))
               else:
                #sending message to specific user
                #client.send("Ready".encode(FMT))
                  message = client.recv(1024)
                  broadcasttospecificuser(message, uu)
                  client.send("sent".encode(FMT))
            #lock.release()    #send to message to that user only
        if op == "EX":
            # user chose exit
            lock.acquire()
            clients.remove(user)
            client.send("you can exit".encode(FMT))
            lock.release()

        op = client.recv(1024).decode(FMT)





lock = threading.Lock()
def receive():
    print("Server is ready to receive on port ", PORT)
    while True:
        print('Waiting...')
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()