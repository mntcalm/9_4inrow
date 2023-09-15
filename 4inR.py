from tkinter import *
from _thread import *
import socket

patter="O"
patt_x="#1E1"
patt="#E11"
patt_o="#E11"

patr=["X", "O"]
patr_col=["#1E1", "#E11"]

your_patt="X"
your_col="#1E1"
sope_patt="O"
sope_col="#E11"

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


in_game=0  # =1 - вы подключены к игре
my_hit=1   # чей сейчас ход. сравнивается с my_num, если совпадае - ход мой. Если НЕ совпадает - ход соперника


def h0():
  global server
  global patter
  global patr
  global patr_col
  global in_game
  global my_hit
  if (in_game == 1) and (my_hit == my_num):
    for c in range (5, -1, -1):
      if game_field[0][c] != "X" and game_field[0][c] != "O":
        game_field[0][c]=patr[int(my_num)]
        labels[0][c].config(bg=patr_col[int(my_num)], text=patr[int(my_num)])
        label_status.config(bg="#2C2", text="Ход сделан, ожидаем хода соперника")
#       передача хода на сервер, цикл ожидания ответа
        x = "0," + str(c) + ",запись"
        server.send(bytes(x, 'utf-8'))
#        my_hit=0
        return
  elif in_game == 0:
        label_status.config(bg="#2C5", text="--Начните игру соответствующей кнопкой--")
        return
  elif my_hit != my_num:
        label_status.config(bg="#5C2", text="--дождитесь хода соперника--")
        return
  label_status.config(bg="#F22", text="В этой колонке ход НЕВОЗМОЖЕН, сделайте ВОЗМОЖНЫЙ ход")

def h1():
  for c in range (5, -1, -1):
    global patter
    global patt_o
    global patt_x
    if game_field[1][c] != "X" and game_field[1][c] != "O":
      game_field[1][c]=patter
      labels[1][c].config(bg="#1E1", text=patter)
      return
  label_status.config(bg="#F22", text="В этой колонке ход НЕВОЗМОЖЕН")

def h2():
  for c in range (5, -1, -1):
    global patter
    global patt_o
    global patt_x
    if game_field[2][c] != "X" and game_field[2][c] != "O":
      game_field[2][c]=patter
      labels[2][c].config(bg="#1E1", text=patter)
      break
def h3():
  for c in range (5, -1, -1):
    global patter
    global patt_o
    global patt_x
    global s
    if game_field[3][c] != "X" and game_field[3][c] != "O":
      game_field[3][c]=patter
      labels[3][c].config(bg="#1E1", text=patter)
      break
def h4():
  for c in range (5, -1, -1):
    global patter
    global patt_o
    global patt_x
    if game_field[4][c] != "X" and game_field[4][c] != "O":
      game_field[4][c]=patter
      labels[4][c].config(bg="#1E1", text=patter)
      break
def h5():
  for c in range (5, -1, -1):
    global patter
    global patt_o
    global patt_x
    if game_field[5][c] != "X" and game_field[5][c] != "O":
      game_field[5][c]=patter
      labels[5][c].config(bg="#1E1", text=patter)
      break
def h6():
  for c in range (5, -1, -1):
    global patter
    global patt_o
    global patt_x
    if game_field[6][c] != "X" and game_field[6][c] != "O":
      game_field[6][c]=patter
      labels[6][c].config(bg="#1E1", text=patter)
      break

def h_strt():
  global in_game
  global my_hit
  global server
  global my_num
  if in_game != 1:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    in_game = 1
    data = server.recv(1024)
    tx=data.decode('utf-8').split(",")[0]
    my_num=data.decode('utf-8').split(",")[1]
    label_status.config(bg="#2C2", text=tx)
    color_igrok.config(bg=patr_col[int(my_num)], text=patr[int(my_num)])
#     если соперник есть - присваиваем мой паттерн,номер игрока выходим из функции
#       если соперника пока нет - цикл ожидания ответа сервера
#           присвоение моего паттерна, номера игрока, выход из функции
#  if my_hit !=1:
#      ждем своего хода

cli_pol = Tk()

cli_pol.title("4 in a row")
cli_pol.geometry("800x650")

game_field=[[None] * 6 for i in range(7)]
labels=[[None] * 6 for i in range(7)]

for i in range (0, 7):
  for j in range (0, 6):
    labels[i][j] = Label(text="{}-{}".format(i,j), bd=1, bg="#333", height="2", width="3")
    labels[i][j].grid(row=j, column=i, ipadx=15, ipady=15, padx=3, pady=3)

btn0 = Button(text="T", padx="3", pady="3", font="13", command=h0)
btn0.place(x="3", y="510", width="65")

btn1 = Button(text="T", padx="3", pady="3", font="13", command=h1)
btn1.place(x="73", y="510", width="65")

btn2 = Button(text="T", padx="3", pady="3", font="13", command=h2)
btn2.place(x="143", y="510", width="65")

btn3 = Button(text="T", padx="3", pady="3", font="13", command=h3)
btn3.place(x="213", y="510", width="65")

btn4 = Button(text="T", padx="3", pady="3", font="13", command=h4)
btn4.place(x="283", y="510", width="65")

btn5 = Button(text="T", padx="3", pady="3", font="13", command=h5)
btn5.place(x="353", y="510", width="65")

btn6 = Button(text="T", padx="3", pady="3", font="13", command=h6)
btn6.place(x="423", y="510", width="65")
label_status = Label(text="-------------- НАДПИСЬ  ----------", bg="#CFC", font="15")
label_status.place(x="3", y="600", width="750", height="50")

#labels[2][4].config(bg="#999", text="УРА")

label_igrok = Label(text="Вы играете \n фишками: ", font="30")
label_igrok.place(x="500", y="20", width="200", height="80")
color_igrok = Label(text=" ", bg="#111", font="30")
color_igrok.place(x="700", y="50", width="60", height="70")
label_yrti = Label(text="00:00")
label_yrti.place(x="550", y="100", width="140", height="30")


label_sopern = Label(text="Соперник  \n  играет:")
label_sopern.place(x="500", y="200", width="200", height="30")
color_sopern = Label(text=" ", bg="#111")
color_sopern.place(x="700", y="200", width="40", height="30")
label_soti = Label(text="00:00")
label_soti.place(x="550", y="230", width="140", height="30")

btn_strt = Button(text="начать игру", padx="3", pady="3", font="13", command=h_strt)
btn_strt.place(x="500", y="450", width="250")


cli_pol.mainloop()
