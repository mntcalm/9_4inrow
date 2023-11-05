from tkinter import *
from _thread import *
import socket
#import threading
#import asyncio
4inRversion="0.12"

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
PORT = 65434  # The port used by the server


in_game=0  # =1 - вы подключены к игре
my_hit=1   # чей сейчас ход. сравнивается с my_num, если совпадае - ход мой. Если НЕ совпадает - ход соперника


def h0():
  do_hit(0)

def h1():
  do_hit(1)

def h2():
  do_hit(2)

def h3():
  do_hit(3)

def h4():
  do_hit(4)

def h5():
  do_hit(5)

def h6():
  do_hit(6)

def do_hit(cn: int):
  global server
  global patter
  global patr # массив буквеного обозначения фишек
  global patr_col # массив цветового обозначения фишек
  global in_game # игра начата этим клиентом? 1 - начата 0 - не начата
  global my_hit # мой ход? если да, то совпадает с my_num
  global my_num # мой номер игрока, выдается сервером
  global whos_hit # кто сделал ход
  if (in_game == 1) and (my_hit == int(my_num)):
    for c in range (5, -1, -1):
      if game_field[cn][c] != "X" and game_field[cn][c] != "O":
        game_field[cn][c]=patr[int(my_num)]
        labels[cn][c].config(bg=patr_col[int(my_num)], text=patr[int(my_num)])
        label_status.config(bg="#2C2", text="Ход сделан, ожидаем хода соперника")
#       передача хода на сервер, цикл ожидания ответа
        msg = str(my_num)+"," + str(cn) + "," + str(c) + ";"
        server.send(bytes(msg, 'utf-8'))
        my_hit=1-int(my_num)
        return
  elif in_game == 0:
        label_status.config(bg="#2C5", text="--Начните игру соответствующей кнопкой--")
        return
  elif my_hit != my_num:
        label_status.config(bg="#5C2", text="--дождитесь хода соперника--")
        return
  label_status.config(bg="#F22", text="В этой колонке ход НЕВОЗМОЖЕН, сделайте ВОЗМОЖНЫЙ ход")


def h_strt():
  global in_game
  global my_hit
  global server
  global my_num
  global game_field
  if in_game != 1:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      server.connect((HOST, PORT))
    except:
      label_status.config(bg="#F22", text="Сервер не отвечает...")
      return
    data = server.recv(1024)
    tx=data.decode('utf-8').split(",")[0]
    my_num=data.decode('utf-8').split(",")[1]
    if my_num == "5":
      label_status.config(bg="#F22", text=tx)
      server.close()
      return
    in_game = 1
    label_status.config(bg="#2C2", text=tx)
    print("проверяем...", my_num)
    for i in range (0, 7):
      for j in range (0, 6):
        labels[i][j].config(text="{}-{}".format(i,j), bg="#333")
        game_field[i][j]="."
    color_igrok.config(bg=patr_col[int(my_num)], text=patr[int(my_num)])
    btn_strt.config(bg="#FFF")
#    asyncio.gather(process_game())
    start_new_thread(process_game,(server,))
    
#    my_thread.start()
#     если соперник есть - присваиваем мой паттерн,номер игрока выходим из функции
#       если соперника пока нет - цикл ожидания ответа сервера
#           присвоение моего паттерна, номера игрока, выход из функции
#  if my_hit !=1:
#      ждем своего хода

def process_game(server,):
  global in_game
  global my_hit
  global my_num
  global whos_hit
#  server.send(bytes("полу-----чено", 'utf-8'))

  while True:
  
    data_in = server.recv(1024)
    if data_in:
#      server.send(bytes("получено", 'utf-8'))
#      label_status.config(bg="#F22", text="процесс пошел")
#      print(data_in)
      data_sp = data_in.decode('utf-8').split(";")
      for i in range (0, (len(data_sp) - 1)):
        data=str(data_sp[i])
        type_of_smsg = int(data.split(",")[3])
        whos_hit=int(data.split(",")[0])
        x=int(data.split(",")[1])
        y=int(data.split(",")[2])
        if type_of_smsg == 4:
          my_hit = whos_hit
          if my_hit == int(my_num):
            label_status.config(bg="#2C2", text="Игра началась,СДЕЛАЙТЕ ВАШ ХОД")
          else:
            label_status.config(bg="#2D2", text="Игра началась, сейчас ХОД СОПЕРНИКА")
          continue
        if type_of_smsg == 1:
          if whos_hit == int(my_num):
            label_status.config(bg="#2C2", text="игра закончена - ВЫ ВЫИГРАЛИ!!!")
          else:
            label_status.config(bg="#C22", text="ПОРАЖЕНИЕ... игра закончена !!!")
          labels[x][y].config(bg="#FD0", text=patr[whos_hit])
          game_field[x][y]=patr[whos_hit]
          btn_strt.config(bg="#1C1")
          in_game=0
        if type_of_smsg == 5:
          times=[int(whos_hit), int(x)]
          yrti=str(times[int(my_num)]//60) + ":" + str(f"{times[int(my_num)]%60:02}")
          if int(whos_hit) <= 60:
            mybg="#F33"
          else:
            mybg="#1EE"

          soti=str(times[1 - int(my_num)]//60) + ":" + str(f"{times[1 - int(my_num)]%60:02}")
          if int(x) <= 60:
            sobg="#F33"
          else:
            sobg="#1EE"
          label_yrti.config(text=yrti, bg=mybg, font="30")
          label_soti.config(text=soti, bg=sobg, font="30")


        if type_of_smsg == 8:
          if whos_hit == int(my_num):
            label_status.config(bg="#C22", text="ПОРАЖЕНИЕ --- у Вас закончилось время")
          else:
            label_status.config(bg="#2C2", text="Вы выиграли - у соперника закончилось время !!!")
          in_game=0
          btn_strt.config(bg="#1C1")


#        server.close()

        print(type_of_smsg, my_num, whos_hit)

        if (type_of_smsg == 0) and (int(whos_hit) == (1 - int(my_num))):
          labels[x][y].config(bg=patr_col[1 - int(my_num)], text=patr[1 - int(my_num)])
          label_status.config(bg="#2C2", text="-----Ваш ход-----")
          game_field[x][y]=patr[1 - int(my_num)]
          my_hit = 1 - whos_hit



cli_pol = Tk()
cli_pol.title("4 in a row  (beta-Version)")
cli_pol.geometry("800x650")

game_field=[[None] * 6 for i in range(7)]
labels=[[None] * 6 for i in range(7)]

for i in range (0, 7):
  for j in range (0, 6):
    labels[i][j] = Label(text="{}-{}".format(i,j), bd=1, bg="#333")
#    labels[i][j].grid(row=j, column=i, ipadx=15, ipady=15, padx=3, pady=3, height=20, width=30)
    xx= 3 + i*70
    yy= 3 + j*80
    labels[i][j].place(x=str(xx), y=str(yy), height="70", width="65")




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
color_igrok.place(x="700", y="40", width="60", height="70")
label_yrti = Label(text="03:00", bg="#1EE", font="30")
label_yrti.place(x="550", y="100", width="140", height="30")


label_sopern = Label(text="Соперник  \n  играет:", font="30")
label_sopern.place(x="500", y="250", width="200", height="80")
color_sopern = Label(text=" ", bg="#111", font="30")
color_sopern.place(x="700", y="260", width="60", height="70")

label_soti = Label(text="03:00", bg="#1EE", font="30")
label_soti.place(x="550", y="350", width="140", height="30")

btn_strt = Button(text="начать игру", padx="3", pady="3", font="13", bg="#1C1", command=h_strt)
btn_strt.place(x="500", y="450", width="250")


cli_pol.mainloop()
