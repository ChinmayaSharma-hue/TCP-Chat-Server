import socket
import threading
from colorama import Fore, Style

HEADERSIZE = 10

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 1236))
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
            index = clients.index(client)
            nickname = nicknames[index]
            message_list = message.decode("utf-8").split(" ")
            if message.decode("utf-8")[len(nickname)+2:] == r"\leave":
                client.send("You have left the chat".encode("utf-8"))
                index = clients.index(client)
                clients.remove(client)
                nickname = nicknames[index]
                broadcast(f"{nickname} has left the chat.".encode("utf-8"))
                nicknames.remove(nickname)
            if message.decode("utf-8")[len(nickname) + 2:].split(" ")[0] == r"\color":
                message = " ".join(message_list[3:])
                color = message_list[2].upper()
                message = (getattr(Fore, color) + message + Style.RESET_ALL)
                message = f"{nickname} : {message}".encode("utf-8")
                broadcast(message)
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f"{nickname} has left the chat.".encode("utf-8"))
            nicknames.remove(nickname)
            break


def recieve():
    while True:
        client, address = server.accept()
        accept = input(f"{address} is trying to connect. Accept connection? : ")
        if accept == 'yes':
            print(f"Connected with {str(address)}")

            clients.append(client)

            client.send("NICK".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")
            nicknames.append(nickname)
            print(f"Nickname of {str(address)} is {nickname}")

            broadcast(f"{nickname} has joined the chat".encode("utf-8"))
            client.send("Connected to the server!".encode("utf-8"))
        else:
            client.send("Your request to join is denied".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("The server is listening...")
recieve()
