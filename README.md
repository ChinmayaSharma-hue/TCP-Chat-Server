# TCP-Chat-Server

A chat server that can accept requests from clients and serve as the intermediary between different clients to talk to each other in a chat-room.

***
## Approach
There are two python files, one for the server and the other for the client. <br> <br>
In the server file,
* A server socket is defined which is set to listen mode
* Following functions are used,
    1. The broadcast function is used to send the message that is recieved from one client to all
       the clients that are connected to the server socket.
    2. The handle function is used to process the message that is recieved from one of the clients
       Additional features can be defined in this function, by doing string formatting on the 
       recieved messages. If no error is observed in recieving the messages, they are 
       broadcasted.
    3. The recieve function is used to recieve new requests and add them to the list of clients
        broadcast messages to. Multithreading is used to handle multiple clients at once.
* Finally, the recieve function is called which starts running the server.

<br><br>
In the client file,
* A client socket is defined which is then connnected to the port the server socket is 
connected to.
* The first message recieved from the server is a request to input the name of the client,
which is inputted and saved to be sent later.
* Following functions are used,
    1. The recieve function is used to recieve the messages from the server and format them
    if necessary and output them.
   2. The write function is used to input a message from the client's end and send the message to
    the server.
* Multithreading is used to run multiple instances of recieve and write at the same time.

***
## Features
* Clients can join the server only if the server authorizes it.
* Clients can join and leave the server whenever they want.
* Clients can send private messages to other clients in the chat-room.
* Clients can colorize their text.
* Clients can make parts of their text **bold**, _italic_, or 
~~strike-through~~ (This can be used with any of the features above)
### Commands
* ```/private <name> <message>``` is used to send the message to only a specific client
in the chat-room.
* ```/leave``` is used to leave the chat-room whenever the client feels like it.
* ```/color <color> <text>``` is used to colorize the text that is broadcasted to all the clients.
* ```/private <name> /color <color> <text>``` is used to send colored text to a specific client 
in the chat room.
* ```**<text>**``` is used to make the text in between the star symbols bold.
* ```__<text>__``` is used to italicize the text in between the double underscores.
* ```~~<text>~~``` is used to strike through the text in between the tilde symbols.
***

## Instructions
* Run ```Server.py``` to start the chat-room.
* Run ```Client.py``` for each client.
Note that as soon as ```Client.py``` is run, the server needs to authorize the connection.
  