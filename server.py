exec(open("./question.py").read())
import socket
import threading
import random
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = socket.gethostbyname("localhost")
port = 9989

print(f"Listening the port {port}")
server.bind((host, port))
server.listen(100)

NUMBER_OF_PLAYER = 2
clients = []
nicknames = []
question = 0
turn = 0
game_start = False

Q, A = get_multiple_question_and_answer()

ALLOWED_TO_PASS = [1]*NUMBER_OF_PLAYER

def broadcast(message):
    for client in clients:
        client.send(message.encode("ascii"))
    time.sleep(0.2)

def quiz():
    global question

    question = random.randint(0,10000)%len(Q)
    question_str = "question|"
    question_str += Q[question]
    broadcast(question_str)

def remain_questions():
    broadcast(f"remainquestion|{len(Q)}")

def wrong_turn_error(turn):
    clients[turn].send(f"wrongturn|{nicknames[turn]}".encode("ascii"))
    time.sleep(0.2)

def not_allowed_to_pass_error(turn):
    clients[turn].send(f"notallowedtopass|{nicknames[turn]}".encode("ascii"))
    time.sleep(0.2)

def pass_to_next_player(turn):
    broadcast(f"passtonextplayer|{nicknames[turn]}")

def countdown():
    broadcast("time|")

def send_turn(turn):
    broadcast(f"turn|{nicknames[turn]}")

def correct(turn):
    broadcast(f"correct|{nicknames[turn]}")

def win(turn):
    broadcast(f"win|{nicknames[turn]}")

def game_over():


def incorrect(turn):
    broadcast(f"incorrect|{nicknames[turn]}")

def remain_players():
    broadcast("remainplayers|" + "|".join(nicknames))

def client_thread(client):
    global turn

    while game_start == False:
        pass

    while True:
        message = client.recv(1024).decode("ascii")

        if message:
            current_client = 0
            while current_client < len(clients):
                if clients[current_client] == client:
                    break
                current_client += 1
            if current_client == turn:
                go_next_player = True

                if message == "q":
                    if ALLOWED_TO_PASS[current_client] == 1:
                        pass_to_next_player(current_client)
                        ALLOWED_TO_PASS[current_client] = 0
                    else:
                        not_allowed_to_pass_error(current_client)
                        go_next_player = False
                elif message == "timeout":
                    remove(current_client)
                    if current_client >= len(clients):
                        current_client = 0

                    go_next_player = False
                elif len(clients) == 1:
                    win(current_client)
                elif message == A[question]:
                    correct(turn)
                    A.remove(A[question])
                    Q.remove(Q[question])
                    quiz()
                else:
                    incorrect(current_client)

                if go_next_player == True:
                    turn+=1
                    if turn >= len(clients):
                        turn = 0

                remain_players()
                remain_questions()
                send_turn(turn)
            else:
                wrong_turn_error(current_client)
        else:
            remove(client)

def remove(index):
    clients.remove(clients[index])
    nicknames.remove(nicknames[index])

while True:
    client, address = server.accept()
    print(f"Connected with {str(address)}")

    while True:
        nickname = client.recv(1024).decode("ascii")
        if nickname:
            if nickname not in nicknames:
                client.send("valid".encode("ascii"))
                break
            else:
                client.send("invalid".encode("ascii"))

    nicknames.append(nickname)
    clients.append(client)

    thread = threading.Thread(target=client_thread, args=(client,))
    thread.start()

    if len(clients) >= NUMBER_OF_PLAYER:
        game_start = True
        broadcast(f"This is {nicknames[turn]}'s turn\n")
        remain_players()
        remain_questions()
        send_turn(turn)
        quiz()
