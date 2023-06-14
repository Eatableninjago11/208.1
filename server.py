# ------- Bolierplate Code Start -----


import socket
from  threading import Thread
import time
IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
clients = {}


def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        print(client, addr)
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
            'client': client,
            'addr': addr,
            'connected_with': '',
            'file_name': '',
            'file_size': 4096,
        }
        print(f'{client_name} connected')
        thread = Thread(target=handle_client, args=(client_name, client))
        thread.start()


def handle_client(client_name, client):
    global clients

    banner1 = f'Welcome to the server, {client_name}!\n click on refresh to see available users\n select the user you and click on connect to start chatting\n'
    client.send(banner1.encode())

    while True: 
        try:
            buffer_size = clients[client_name]['file_size']
            chunk = client.recv(buffer_size)
            message = chunk.decode().strip().lower()

            if(message):
                handle_messages(client_name, message, client)

            else:
                remove_client(client_name)
        except:
            pass

def handle_messages(client_name, message, client):
    global clients

    if message == 'show list':
        handleshowlist(client)
    elif message == 'connect':
        handleconnect(client)
        console.log(message)

# when a client request a list of active users
def handleshowlist(client):
    global clients
    counter = 0

    for c in clients:
        counter = counter + 1
        client_address = clients[c]['addr'][0]
        connected_with = clients[c]['connected_with']
        message = ''
        if(connected_with):
                message = f'{counter}; {c}; {client_address}; connected with {connected_with}; tiul, \n '
        else:
                message = f'{counter}; {c}; {client_address}; Available, tiul \n '

        client.send(message.encode())
        time.sleep(1)
        
def remove_client(client_name):
     global clients
     clients.pop(client_name)
     print(f'{client_name} disconnected')


def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup_thread = Thread(target=setup)           #receiving multiple messages
setup_thread.start()

# ------ Bolierplate Code End -----------
