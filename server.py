# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    #print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
   # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import threading
import socket

host = '127.0.0.1' # localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames( index)
            broadcast(f'{nickname}) left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


def recieve():
    while True:
        client, address =server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('asci(i')
        nicknames.append(client)

        print(f'Nickname of client is {nickname}!')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

recieve()