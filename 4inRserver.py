import socket
from _thread import *

game_field=[[None] * 6 for i in range(7)]
num_of_hit = 0
patr=["X", "O"]
HOST = "127.0.0.1"
PORT = 65432
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(2)

list_of_clients = []
who_active = 1 # чей сейчас ход

def clientthread(conn, addr, ami):
    global num_of_hit
    global who_active
    global patr
    # sends a message to the client whose user object is conn
    msg="Вы подключены!," + str(len(list_of_clients)-1)
    conn.send(bytes(msg, 'utf-8'))
    while True:

            try:
                message = conn.recv(1024).decode('utf-8')
                if message:
                    who_isit=int(message.split(",")[0])
                    if who_isit == who_active:
                      x=int(message.split(",")[1])
                      y=int(message.split(",")[2])
                      game_field[x][y]=patr[who_isit]
#-----------------здесь будет логика, закончена ли игра и как (третее поле)
# 0 - игра продолжается
# 1 - выиграл игрок номер в поле 0
# 2 - кто-то сдался (тот, кто в поле 0)
# 3 - ничья: 42 хода сделано, свободных ячеек нет, но нет и победителя
                      status_of_end=0
                      msg=str(who_isit) + "," + str(x) + "," + str(y) + "," + str(status_of_end)
                      list_of_clients[1-ami].send(bytes(msg, 'utf-8'))
                      who_active = 1 - who_active
                    """prints the message and address of the
                    user who just sent the message on the server
                    terminal"""
                    num_of_hit = num_of_hit + 1
                    print("ходов сделано = ",num_of_hit)
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
    print("я пытался")

while True:
  if len(list_of_clients) < 2:
    conn, addr = server.accept()
#  print(conn, "-------------", addr)
    print (conn, "--------", addr,  " connected")

    list_of_clients.append(conn)
    start_new_thread(clientthread,(conn,addr,(len(list_of_clients)-1)))
server.close()





