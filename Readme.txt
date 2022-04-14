
Authors=['fatima Rathore','Pavel Bondarenko']
star_id=['bl1713lh', bv2737dg]

how to run files
#go in projects directory
python3 chatsever.py <port> #first you need to run this
python3 chatclient.py <server_name> <port> <username>  #you can open multiple clients on different terminals simultaneously

server accepts multiple simultaneous clients
open multiple clients on different terminals
using TCP so server needs to be started first.

run server first

chatserver.py

the client list is here
anything added removed or wanted from list is done here
requests are sent by client and the server only has acess to the clients and sends messages,or adds user,or removes user,
and sends a reply back to client that what it asked was done or not or an error occured
there is one thread that starts the server and that thread works as the reciever thread, as new connections are established
new threads are created for each connection
A thread listens to commands or messages from client

chatclient.py
there are two threads
one is the main thread that does the client work. meaning it's a thread for every client.
and in every client there is the listen thread which listens for incoming messages
the receive function is for receive thread which is the client thread
the recieve function also has a while loop which will not end untill EX command is inputted
the client sends the commands
you need to sign in first
if your username and passwords are correct
then you will be asked for the commands input
else you will be asked to reenter until a new user is made or your input match is found in current users
if your username is not found in the file a new user will be made
now you will be asked to input commands from the menu
this is a while loop until EX is inputted
each command is first checked if it is a command if it is then it is sent to the server who sends signal back to client that it is ready for that commands work
then the client send the message back and the server does the work and sends a message back to show the work is done
for example
for DM command
client send encoded DM op code to server to tell it to get ready for DM stuff
the server sends back a list of other users the client can message
the client than sends the name of user he wants to message and the message
the server recieves it and sends sends the message and reply's to client if the user went offline or the message was sent

