from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def send(event=None):
    msg = my_msg.get()
    my_msg.set("") 
    client_socket.send(bytes(msg, "utf8"))
    if msg == "(выход)":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("(выход)")
    send()

top = tkinter.Tk()
top.title("Окно чата")
top.geometry("1024x340")
top.configure(bg = "#282c34")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame)
entry_field = tkinter.Entry(top, textvariable=my_msg, background = "#21252b", width = 150, fg = "#dddddd", borderwidth = 0, insertbackground = "#2277dd", font='Consolas 12')
entry_field.bind("<Return>", send)
entry_field.pack()
msg_list = tkinter.Listbox(messages_frame, height=15, width=150, yscrollcommand=scrollbar.set)
msg_list.configure(fg = "#dddddd", bg = "#282c34", highlightbackground = "#282c34", highlightcolor = "#282c34", borderwidth = 0, font='Consolas 10')
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

send_button = tkinter.Button(top, text="Отправить", command=send, background = "#2a2e36", width = 150, fg = "#dddddd", borderwidth = 0, font='Consolas 10')
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input("Введите адрес сервера(можно узнать у человека, который запустил сервер): ")
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
