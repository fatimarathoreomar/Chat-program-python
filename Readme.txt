
Authors=['fatima Rathore','Pavel Bondarenko']
star_id=['bl1713lh', bv2737dg]

how to run files
#go in projects directory
python3 chatsever.py #first you need to run this
python3 chatclient.py #you can open multiple clients on different terminals simultaneously

for ease we will have the client ask for name later
server accepts multiple simultaneous client
open multiple clients on different terminals
using udp so no need to start server first.

There are two types of message frames: 1) data message and 2) command message. A data message is exchanged between clients
(i.e., the Public and Direct messages described in the following online chat room protocol).
A command message is exchanged between a client and the server (e.g., operation, acknowledgment, confirmation messages described below).
Define the message format to encode the message type.
For example, the first character of the message can be used to distinguish between the two types of messages (e.g., "C" for command message and "D" for data message).
The sender is responsible for encoding the type of information into the message frame. The receiver is responsible for extracting the type of information from the message and performs accordingly.
The server checks whether it is a new user or an existing user and requests a password. Note: Store usernames and passwords in a file rather than in memory (otherwise, the credentials will get lost once the server program is terminated).

chatserver.py

the client list is here
anything added removed or wanted from list is done here
requests are sent by client and the server only has acess to the clients and sends messages,or adds user,or removes user,and sends a reply back to client that what it asked was done or not or an error occured
there is one thread that starts the server and that thread works as the reciever thread
it is a while loop
in which it checks which command was sent by the client and replies accordingly

chatclient.py
there are two threads
one is the main thread that does the client work. meaning it's a thread for every client.
and in every client there is the broadcast thread that broadcast any reply sent by server
the listen function is for the broadcast thread
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

