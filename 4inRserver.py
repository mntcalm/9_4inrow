import socket
import time
from _thread import *

game_field=[[None] * 6 for i in range(7)]
num_of_hit = 0
patr=["X", "O"]
HOST = "127.0.0.1"
PORT = 65434
winner=5
status_of_end=0
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

list_of_clients = []
who_active = 1 # чей сейчас ход

def s_od():
  global num_of_hit
  global list_of_clients
  global game_field
  del list_of_clients[0:]
  game_field=[[None] * 6 for i in range(7)]
  num_of_hit=0


def check_win(who_isit,x,y):
  global game_field
  clcltr = 0
  for i in range (0,6):
    if game_field[x][i] == patr[who_isit]:
      clcltr = clcltr + 1
      if clcltr >=4:
        winner=who_isit
#        print("Ура, 4 в ряд!!!", winner)
        return who_isit
    else:
      clcltr=0
  clcltr = 0
  for i in range (0,7):
    if game_field[i][y] == patr[who_isit]:
      clcltr = clcltr + 1
      if clcltr >=4:
        winner=who_isit
#        print("Ура, 4 в ряд!!!", winner)
        return who_isit
    else:
      clcltr=0

  clcltr = 0 # диагональ слева и вниз
  x0 = x - min(x,y)
  y0 = y - min(x,y)
  while ((7-x0)*(6-y0) != 0):
    if game_field[x0][y0] == patr[who_isit]:
      clcltr = clcltr + 1
      if clcltr >=4:
        winner=who_isit
#        print("Ура, 4 в ряд!!!", winner)
        return who_isit
    else:
      clcltr=0
    x0=x0+1
    y0=y0+1
  

  clcltr=0 # диагональ слева и вверх
  x0 = x - min(x,5-y)
  y0 = y + min(x,5-y)
  while ((7-x0)*(y0+1) != 0):
    if game_field[x0][y0] == patr[who_isit]:
      clcltr = clcltr + 1
      if clcltr >=4:
        winner=who_isit
#        print("Ура, 4 в ряд!!!", winner)
        return who_isit
    else:
      clcltr=0
    x0=x0+1
    y0=y0-1
  return 5


def time_control():
  global who_active
  global list_of_clients
  time_f=[180.0, 180.0]
  time_i=[int(180), int(180)]

  while True:
    time.sleep(0.25)
    time_f[who_active] = time_f[who_active] - 0.25
#    print(time_f[who_active])
    if time_f[who_active] < 0:
      msg=str(who_active) + ",0,0,8;"
      list_of_clients[0].send(bytes(msg, 'utf-8'))
      list_of_clients[1].send(bytes(msg, 'utf-8'))
      list_of_clients[0].close()
      list_of_clients[1].close()
      s_od()
#    print(time_i)
    if (round(time_f[0]) != time_i[0]) or (round(time_f[1]) != time_i[1]):
      time_i[0] = round(time_f[0])
      time_i[1] = round(time_f[1])
      msg=str(time_i[0]) + "," + str(time_i[1]) + ",0,5;"
      list_of_clients[0].send(bytes(msg, 'utf-8'))
      list_of_clients[1].send(bytes(msg, 'utf-8'))
#      break

def clientthread(conn, addr, ami):
    global num_of_hit
    global who_active
    global patr
    global status_of_end
    # sends a message to the client whose user object is conn
    if len(list_of_clients) > 2:
      msg="Игра занята!," + "5;"
      conn.send(bytes(msg, 'utf-8'))
      list_of_clients.remove(conn)
      conn.close()
      return
    elif len(list_of_clients) == 1:
      msg="4in1 test branch v 0.12 Вы подключены - ожидаем соперника," + str(len(list_of_clients)-1)
      conn.send(bytes(msg, 'utf-8'))
    elif len(list_of_clients) == 2:
      msg="Соперник подключился - игра началась!," + str(len(list_of_clients)-1)
      conn.send(bytes(msg, 'utf-8'))
      
      who_active=int(time.time())%2
      msg=str(who_active) + ",0,0,4;"
      start_new_thread(time_control,())
            # + str(len(list_of_clients)-1)
#      conn.send(bytes(msg, 'utf-8'))
      list_of_clients[0].send(bytes(msg, 'utf-8'))
      list_of_clients[1].send(bytes(msg, 'utf-8'))

    while True:
            try:
                message_in = conn.recv(1024).decode('utf-8')
                if message_in:
                  message_sp = message_in.split(";")
                  for i in range (0, len(message_sp)):
                    message = message_sp[i]
#                    print(message, "----------")
                    who_isit=int(message.split(",")[0])
                    if who_isit == who_active:
                      x=int(message.split(",")[1])
                      y=int(message.split(",")[2])
                      game_field[x][y]=patr[who_isit]
#-----------------здесь логика, закончена ли игра и как 


                      clcltr=0
                      if check_win(who_isit,x,y) !=5:
#                        print("Победитель",who_isit)
                        msg=str(who_isit) + "," + str(x) + "," + str(y) + ",1;"
                        list_of_clients[0].send(bytes(msg, 'utf-8'))
                        list_of_clients[0].close()
                        list_of_clients[1].send(bytes(msg, 'utf-8'))
                        list_of_clients[1].close()
                        s_od()
                      else:
                        msg=str(who_isit) + "," + str(x) + "," + str(y) + ",0;"
                        list_of_clients[1-ami].send(bytes(msg, 'utf-8'))
                        list_of_clients[ami].send(bytes(msg, 'utf-8'))
                        who_active = 1 - who_active
#                        print("Шлем сообщение о продолж.игры")

#                      if winner != 5:
#                        msg=str(winner) + "," + str(x) + "," + str(y) + ",1"
#                        list_of_clients[1].send(bytes(msg, 'utf-8'))
#                        list_of_clients[0].send(bytes(msg, 'utf-8'))



# формат сообщений игрокам:
# НОМЕР_ИГРОКА,Х_хода,Y_хода,ТИП_СООБЩЕНИЯ,текст(необязательное поле)
#    0           1       2         3            4

# (третее поле)
# 0 - игра продолжается
# 1 - выиграл игрок номер в поле 0
# 2 - кто-то сдался (тот, кто в поле 0)
# 3 - ничья: 42 хода сделано, свободных ячеек нет, но нет и победителя
# 4 - игра началась
# 5 - отчет о времени у игроков: нулевое поле = оставшееся время у игрока 0. первое поле - у первого игрока
# 7 - неигровое действие, на перспективу, например сообщение в чате
# 8 - время кончилось у игрока N в нулевом поле
                      
                    """prints the message and address of the



                    user who just sent the message on the server
                    terminal"""
                    num_of_hit = num_of_hit + 1
#                    print(ami,who_active, "ходов сделано = ",num_of_hit)
#                    print("< клиент номер ", ami , "> ", message)
                    # Calls broadcast function to send message to all
#                    message_to_send = "<" + addr[0] + "> " + message
#                    broadcast(message_to_send, conn)
#                    conn.send(bytes("Получение сообщения", 'utf-8'))
#                    sender(message_to_send, conn)
                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    remove(conn)
                    #continue
            except:
                continue

def sender(mesg, connection):
  try:
    connection.send(bytes(mesg, 'utf-8'))
  except:
    print("я пытался...")

while True:
  if len(list_of_clients) < 5:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    start_new_thread(clientthread,(conn,addr,(len(list_of_clients)-1)))
server.close()





