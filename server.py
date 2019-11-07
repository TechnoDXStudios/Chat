from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():

 while True:
     client, client_address = SERVER.accept()
     print("%s:%s has connected." % client_address)
     client.send(bytes("Добро пожаловать, введите своё имя▓#84c257", "utf8"))
     addresses[client] = client_address
     Thread(target=handle_client, args=(client,)).start()

def interpret(s):
    if "(" in s and ")" in s:
        s = s[: s.find("(")].replace(" ", "") + s[s.find("("):]
        com = s[1:s.find("(")]
        arg = s[s.find("(") + 1: s.find(")")].split(",")
    else:
        s = s.replace(" ", "")
        com = s[1:].replace(" ", "")
        arg = []
    return [com, arg]

def handle_client(client):  

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Добро пожаловать %s! Если вы захотите выйти, напишите (выход)▓#317fe3' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!▓#dddddd" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    color = "#dddddd"

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("(выход)", "utf8"):
            mes = msg.decode("utf-8")
            if mes[0] != ">":
                broadcast(bytes(name + ": " + mes + "▓" + color, "utf8"))
            else:
                get = interpret(mes)
                print(get)
                if get[0] == "color":
                    color = get[1][0].replace(" ", "")
                    print(color)
        else:
            client.send(bytes("(выход)", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s покинул чат.▓#992c34" % name, "utf8"))
            break


def broadcast(msg, prefix=""): 

 for sock in clients:
     sock.send(bytes(prefix, "utf8")+msg)

    
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
 SERVER.listen(10)
 print("Ждёим подключений! ...")
 ACCEPT_THREAD = Thread(target=accept_incoming_connections)
 ACCEPT_THREAD.start()
 ACCEPT_THREAD.join()
 SERVER.close()
