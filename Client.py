import socket
import threading


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 1239))
name = input("Please provide your name : ")


# To input the message and send it to the server
def send():
    while True:
        message = input().encode("utf-8")
        client.send(message)


def recieve():
    while True:
        message = client.recv(1024).decode("utf-8")

        # The first message recieved from the server asking for the name, in response to which the name of the client
        # is sent.
        if message == 'Name':
            client.send(name.encode("utf-8"))
            print("Waiting for server confirmation...")
        # If the message sent by the server has /private as the first word, it is avoided if it is not meant for the
        # client in question
        elif message.split()[2] == '/private':
            if len(message.split()) > 3:
                if message.split()[3] == name:
                    print(f"{message.split()[0].upper()} HAS SENT YOU A PRIVATE MESSAGE.")
                    print(f"{message.split()[0]} : {' '.join(message.split()[4:])}")
                else:
                    continue
            else:
                print(message)
        else:
            print(message)


write_thread = threading.Thread(target=send)
write_thread.start()

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
