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

Q = [" What is the Italian word for PIE?|a.Mozarella|b.Pasty|c.Patty|d.Pizza",
     " Water boils at 212 Units at which scale?|a.Fahrenheit|b.Celsius|c.Rankine|d.Kelvin",
     " Which sea creature has three hearts?|a.Dolphin|b.Octopus|c.Walrus|d.Seal",
     " Who was the character famous in our childhood rhymes associated with a lamb?|a.Mary|b.Jack|c.Johnny|d.Mukesh",
     " How many bones does an adult human have?|a.206|b.208|c.201|d.196",
     " How many wonders are there in the world?|a.7|b.8|c.10|d.4",
     " What element does not exist?|a.Xf|b.Re|c.Si|d.Pa",
     " How many states are there in India?|a.24|b.29|c.30|d.31",
     " Who invented the telephone?|a.A.G Bell|b.John Wick|c.Thomas Edison|d.G Marconi",
     " Who is Loki?|a.God of Thunder|b.God of Dwarves|c.God of Mischief|d.God of Gods",
     " Who was the first Indian female astronaut ?|a.Sunita Williams|b.Kalpana Chawla|c.None of them|d.Both of them ",
     " What is the smallest continent?|a.Asia|b.Antarctic|c.Africa|d.Australia",
     " The beaver is the national embelem of which country?|a.Zimbabwe|b.Iceland|c.Argentina|d.Canada",
     " How many players are on the field in baseball?|a.6|b.7|c.9|d.8",
     " Hg stands for?|a.Mercury|b.Hulgerium|c.Argenine|d.Halfnium",
     " Who gifted the Statue of Libery to the US?|a.Brazil|b.France|c.Wales|d.Germany",
     " Which planet is closest to the sun?|a.Mercury|b.Pluto|c.Earth|d.Venus"]

A = ['d', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'd', 'c', 'a', 'b', 'a']

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
    clients[turn].send(f"error|{nicknames[turn]}".encode("ascii"))
    time.sleep(0.2)

def countdown():
    broadcast("time|")

def send_turn(turn):
    broadcast(f"turn|{nicknames[turn]}")

def correct(turn):
    broadcast(f"correct|{nicknames[turn]}")

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
                if message == A[question]:
                    correct(turn)
                    A.remove(A[question])
                    Q.remove(Q[question])
                    quiz()
                else:
                    incorrect(turn)

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

def remove(client):
    if client in clients:
        clients.remove(client)

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
