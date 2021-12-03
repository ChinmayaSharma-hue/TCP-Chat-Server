import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 1236))

nickname = input("Choose a nickname : ")


def recieve():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == 'NICK':
                client.send(nickname.encode("utf-8"))
            else:
                message_list = message.split(" ")
                try:
                    if (message_list[1] == r"\private") and (message_list[2] != nickname):
                        continue
                    elif (message_list[1] == r"\private") and (message_list[2] == nickname):
                        print(str(message_list[0][:-1]).upper(), "HAS SENT YOU A PRIVATE MESSAGE")
                        message = message_list[0] + " " + " ".join(message_list[3:])
                except:
                    pass
                print(message)
        except:
            print("An error has occured.")
            client.close()
            break


def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode("utf-8"))


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()