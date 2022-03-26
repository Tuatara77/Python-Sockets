import socket
import threading

HOST = ""  # who can connect to the server (blank means all)
PORT = 12345
BUFFERSIZE = 1024
QUEUESIZE = 5

STOPMESSAGE = "#64STOPorAng3"
SEPARATOR = "|"

running = True

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((HOST, PORT))
soc.listen(QUEUESIZE)

connectionlist = []

def listener():
    global running
    while running:
        while len(connectionlist) <= 3:
            clientsocket, clientaddress = soc.accept()
            if clientsocket:
                print(f"Connected to {clientaddress}")
                connectionlist.append(clientsocket)
                if len(connectionlist) == 1: receiver1.start()
                if len(connectionlist) == 2: receiver2.start()
                if len(connectionlist) == 3: receiver3.start()
                clientsocket = False


def bouncer(sock):
    global running
    while True:
        name, msg = sock.recv(BUFFERSIZE).decode().split(SEPARATOR)
        if msg == STOPMESSAGE:
            print(f"{name} left")
            for socke in connectionlist:
                if sock != socke: socke.send(f"{name}{SEPARATOR}left".encode())
            connectionlist.remove(sock)
            running = len(connectionlist)
            break
        print(f"{name}: {msg}")
        for socke in connectionlist: socke.send(f"{name}{SEPARATOR}{msg}".encode())


listenerthread = threading.Thread(target=listener, daemon=True)
listenerthread.start()

receiver1 = threading.Thread(target=lambda: bouncer(connectionlist[0]), daemon=True)
receiver2 = threading.Thread(target=lambda: bouncer(connectionlist[1]), daemon=True)
receiver3 = threading.Thread(target=lambda: bouncer(connectionlist[2]), daemon=True)

while running: pass # just to keep the program alive while the threads are running