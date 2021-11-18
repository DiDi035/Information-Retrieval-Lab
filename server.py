import socket
import threading
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = socket.gethostbyname("localhost")
port = 9989

print(f"Listening the port {port}")
server.bind((host, port))
server.listen(100)

NUMBER_OF_PLAYER = 3
clients = []
nicknames = []
question = 0
turn = 0
game_start = False

Q = [" What is the Italian word for PIE? \n a.Mozarella b.Pasty c.Patty d.Pizza\n",
     " Water boils at 212 Units at which scale? \n a.Fahrenheit b.Celsius c.Rankine d.Kelvin\n",
     " Which sea creature has three hearts? \n a.Dolphin b.Octopus c.Walrus d.Seal\n",
     " Who was the character famous in our childhood rhymes associated with a lamb? \n a.Mary b.Jack c.Johnny d.Mukesh\n",
     " How many bones does an adult human have? \n a.206 b.208 c.201 d.196\n",
     " How many wonders are there in the world? \n a.7 b.8 c.10 d.4\n",
     " What element does not exist? \n a.Xf b.Re c.Si d.Pa\n",
     " How many states are there in India? \n a.24 b.29 c.30 d.31\n",
     " Who invented the telephone? \n a.A.G Bell b.John Wick c.Thomas Edison d.G Marconi\n",
     " Who is Loki? \n a.God of Thunder b.God of Dwarves c.God of Mischief d.God of Gods\n",
     " Who was the first Indian female astronaut ? \n a.Sunita Williams b.Kalpana Chawla c.None of them d.Both of them \n",
     " What is the smallest continent? \n a.Asia b.Antarctic c.Africa d.Australia\n",
     " The beaver is the national embelem of which country? \n a.Zimbabwe b.Iceland c.Argentina d.Canada\n",
     " How many players are on the field in baseball? \n a.6 b.7 c.9 d.8\n",
     " Hg stands for? \n a.Mercury b.Hulgerium c.Argenine d.Halfnium\n",
     " Who gifted the Statue of Libery to the US? \n a.Brazil b.France c.Wales d.Germany\n",
     " Which planet is closest to the sun? \n a.Mercury b.Pluto c.Earth d.Venus\n"]

A = ['d', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'd', 'c', 'a', 'b', 'a']

def broadcast(message):
    for client in clients:
        client.send(message.encode("ascii"))

def quiz():
    global question

    question = random.randint(0,10000)%len(Q)
    broadcast(Q[question])

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
                current_client +=1
            print(f"turn: {turn}")
            print(f"current: {current_client}")
            if current_client == turn:
                if message == A[question]:
                    broadcast(f"{nicknames[turn]}'s answer is correct !!!!\n")
                    quiz()
                else:
                    broadcast(f"{nicknames[turn]}'s answer is wrong !!!!\n")

                turn+=1
                if turn >= len(clients):
                    turn = 0
                clients[turn].send("yourturn\n".encode("ascii"))
            else:
                clients[current_client].send("You are only allowed to answer when it is your turn".encode("ascii"))
        else:
            remove(client)

def remove(client):
    if client in clients:
        clients.remove(client)

while True:
    client, address = server.accept()
    print(f"Connected with {str(address)}")

    client.send("NICKNAME".encode("ascii"))
    nickname = client.recv(1024).decode("ascii")
    nicknames.append(nickname)
    clients.append(client)

    thread = threading.Thread(target=client_thread, args=(client,))
    thread.start()

    if len(clients) >= NUMBER_OF_PLAYER:
        game_start = True
        clients[turn].send("yourturn\n".encode("ascii"))
        quiz()