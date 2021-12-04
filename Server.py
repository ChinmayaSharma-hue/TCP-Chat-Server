import socket
import threading
from colorama import Fore, Style

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 1239))

server.listen()
clients = []
names = {}


def send(message):
    for client in clients:
        client.send(message)


def process(client):
    while True:
        message = client.recv(1024)

        # To convert to bold - The text which is to be made bold is extracted from the message and the required strings
        # to make it bold are added to it and this is inserted back into the message. Note that the message is encoded
        # here because all the functions like /private and /color take in message in encoded form and then process,
        # therefore encoding here will allow multiple functions to be used together.
        bold_list = message.decode("utf-8").split('*')
        is_bold_list = False
        for i in range(len(bold_list)):
            try:
                if (bold_list[i] == '') and (bold_list[i + 2] == ''):
                    is_bold_list = True
                    bold_text = bold_list[i + 1]
                    index = i + 1
            except:
                pass
        if is_bold_list:
            bold_list[index] = '\033[1m' + bold_text + '\033[0m'
            bold_list.remove('')
            bold_list.remove('')
            message = ' '.join(bold_list).encode("utf-8")

        # To convert to italics - The text which is to be made italics is extracted from the message and the required
        # strings to make it bold are added to it and this is inserted back into the message. Note that the message is
        # encoded here because all the functions like /private and /color take in message in encoded form and then
        # process, therefore encoding here will allow multiple functions to be used together.
        italics_list = message.decode("utf-8").split('_')
        is_italics_list = False
        for i in range(len(italics_list)):
            try:
                if (italics_list[i] == '') and (italics_list[i + 2] == ''):
                    is_italics_list = True
                    italics_text = italics_list[i + 1]
                    index = i + 1
            except:
                pass
        if is_italics_list:
            italics_list[index] = '\x1B[3m' + italics_text + '\x1B[0m'
            italics_list.remove('')
            italics_list.remove('')
            message = ' '.join(italics_list).encode("utf-8")

        # To strikethrough text - The text that is to be striked through is extracted, and a new text is made by adding
        # u'\u0336' to each character in the text. The rest of the code is the same as the ones used for bold and
        # italics
        strike_list = message.decode("utf-8").split('~')
        is_strike_list = False
        for i in range(len(strike_list)):
            try:
                if (strike_list[i] == '') and (strike_list[i + 2] == ''):
                    is_strike_list = True
                    strike_text = strike_list[i + 1]
                    index = i + 1
            except:
                pass
        if is_strike_list:
            final_text = ''
            for character in strike_text:
                final_text = final_text + (character + u'\u0336')
            strike_list[index] = final_text
            strike_list.remove('')
            strike_list.remove('')
            message = ' '.join(strike_list).encode("utf-8")

        # If the first word of the message is /leave, the client is removed from the list of clients and then from the
        # dictionary of names
        if message.decode("utf-8").startswith('/leave'):
            client.send('You have left the chat.'.encode("utf-8"))
            clients.remove(client)
            send(f'{names[client]} has left the chat.'.encode("utf-8"))
            names.pop(client)
        # If the first word of the message is /color, then the appropriate color is extracted from the message and is
        # added to the required text using Fore from colorama.
        elif (message.decode("utf-8").startswith('/color')) and (len(message.decode("utf-8").split()) > 2):
            try:
                message = message.decode("utf-8")
                color = message.split()[1].upper()
                processed_message = ' '.join(message.split()[2:])
                processed_message = (getattr(Fore, color) + processed_message + Style.RESET_ALL)
                processed_message = f'{names[client]} : {processed_message}'.encode("utf-8")
            except:
                processed_message = f'{names[client]} : {message}'.encode("utf-8")
            send(processed_message)
        # If private is given along with color, then color would be in a different position in the message, therefore
        # the function that can detect that has to be defined.
        elif (len(message.decode("utf-8").split()) > 4) and (message.decode("utf-8").split()[0] == '/private') and (message.decode("utf-8").split()[2] == '/color'):
            message = message.decode("utf-8")
            color = message.split()[3].upper()
            processed_message = ' '.join(message.split()[4:])
            processed_message = (getattr(Fore, color) + processed_message + Style.RESET_ALL)
            processed_message = f'{names[client]} : /private {message.split()[1]} {processed_message}'.encode("utf-8")
            send(processed_message)
        else:
            processed_message = f'{names[client]} : {message.decode("utf-8")}'.encode("utf-8")
            send(processed_message)


# This function is made to recieve the requests in an infinite loop, so that it keeps accepting new requests.
# Multi-threading is used to run multiple instances of the function 'process' above for all the clients.
def recieve():
    while True:
        client, address = server.accept()
        print(f'{str(address)} is trying to join the server!')

        # Ask for the name
        client.send('Name'.encode("utf-8"))
        name = client.recv(1024).decode("utf-8")

        # Decide if client can stay
        accept = input(f'Should {name} be accepted into the server? (y/n) : ')
        if accept == 'y':
            print(f"{name} has been added to the chat-room")
            clients.append(client)
            names[client] = name
            send(f'{name} has joined the chat.'.encode("utf-8"))
            client.send('Welcome to the server!'.encode("utf-8"))
        else:
            client.send('Your request to join has been denied.'.encode("utf-8"))

        thread = threading.Thread(target=process, args=(client,))
        thread.start()


print("The server is online.")
recieve()
