import socket
from _thread import *

game_field=[[None] * 6 for i in range(7)]

HOST = "127.0.0.1"
PORT = 65432
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(2)

list_of_clients = []

def clientthread(conn, addr, ami):
    
      
    # sends a message to the client whose user object is conn
    msg="Вы подключены!," + str(len(list_of_clients)-1)
    conn.send(bytes(msg, 'utf-8'))
    while True:

            try:
                message = conn.recv(1024).decode('utf-8')
                if message:
                    conn.send(bytes(message, 'utf-8'))
                    """prints the message and address of the
                    user who just sent the message on the server
                    terminal"""
                    print("< клиент номер ", ami , "> ", message)
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





