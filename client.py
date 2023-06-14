#-----------Bolierplate Code Start -----
import socket
from threading import Thread
from tkinter import *
from tkinter import ttk


PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096
name = None
listbox = None



def openChatWindow():
    global name
    global SERVER

    windows = Tk()

    windows.title("Chat")
    windows.geometry("500x350")

    nameLabel = Label(windows, text="Enter your name", font= ("Arial", 10))
    nameLabel.place(x=10, y=10)

    name = Entry(windows, text= "", font= ("Arial", 10), width= 30)
    name.place(x=120, y=10)
    name.focus()

    connectServer = Button(windows, text="Connect to Chat Server", font= ("Arial", 10), command= connectToServer)
    connectServer.place(x=350, y=6)

    seperator = ttk.Separator(windows, orient=HORIZONTAL)
    seperator.place(x=0, y=50, relwidth= 1, height= 0.1)

    labelUsers = Label(windows, text="Active Users", font= ("Arial", 10))
    labelUsers.place(x=10, y=80)

    listbox = Listbox(windows, height= 5, width= 67, activestyle= 'dotbox', font= ("Arial", 10))
    listbox.place(x=10, y=100)

    scrollbar1 = ttk.Scrollbar(windows, orient=HORIZONTAL)
    scrollbar1.place(relx=1, y=100, relwidth= 1, relheight= 1)
    scrollbar1.config(command=listbox.yview)
                     
    connectButton = Button(windows, text="Connect", font= ("Arial", 10), command= connectWithClient)
    connectButton.place(x=282, y=200)

    disconnectButton = Button(windows, text="Disconnect", font= ("Arial", 10), command= dissconnectWithClient)
    disconnectButton.place(x=350, y=200)

    refreshButton = Button(windows, text="Refresh", font= ("Arial", 10), command= showClientsList)
    refreshButton.place(x=435, y=200)

    windows.mainloop()

def receiveMessage():
    print("received message from server")
    global SERVER
    global name
    global listbox
    global BUFFER_SIZE

    while True:
        chunk = SERVER.recv(BUFFER_SIZE)
        print(chunk.decode())
            
            #listbox.insert(END, name + ": " + chunk)
        try: 
            if "tiul" in chunk.decode():
                letter_list = chunk.decode().split(",")
                listbox.insert( letter_list[0] + ": " + letter_list[1])
                print(letter_list)
        except:
            pass
        

def connectToServer():
    global SERVER
    global name
    cname = name.get()

    SERVER.send(cname.encode())

def showClientsList():
    global listbox
    global SERVER

    listbox.delete(0, "END")
    SERVER.send(b'show list').encode('ascii')

def connectWithClient():
    global SERVER
    global listbox

    text = listbox.get(ANCHOR)
    list_item = text.split(":")
    msg = "connect " + list_item[1]
    print(msg)
    SERVER.send(msg.encode('ascii'))

def dissconnectWithClient():
    global SERVER
    global listbox

    text = listbox.get(ANCHOR)
    list_item = text.split(":")
    msg = "disconnect " + list_item[1]
    SERVER.send(msg.encode('ascii'))

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    recieve_thread = Thread(target=receiveMessage)
    recieve_thread.start()

    openChatWindow()


setup()


#-----------Bolierplate Code Start -----