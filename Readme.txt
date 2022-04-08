#go in projects directory
Authors=['fatima Rathore','Pavel Bondarenko']
star_id=['bl1713lh', bv2737dg]
python3 sever.py
python3 client.py

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
