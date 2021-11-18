import socket
import threading
import time

host = socket.gethostbyname("localhost")
port = 9989
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
NUMBER_OF_PLAYER = 3
clients = []
nicknames = []

def start_socket():
    try:
        print(f"Listening the port {port}")

        server.bind((host, port))
        server.listen()
    except socket.error as message:
        print(f"Socket binding error: {message}")

def broadcast(message):
    for client in clients:
        client.send(message)

def accepting_client():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICKNAME".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        broadcast(f"{nickname} joined the game!\n".encode("ascii"))
        client.send("Connected to server\n".encode("ascii"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

        if len(clients) >= NUMBER_OF_PLAYER:
            break

def game_loop():
    while True:
        broadcast("Question 1: 1 + 1 = ?\n".encode("ascii"))
        broadcast("A. 1\n".encode("ascii"))
        broadcast("B. 2\n".encode("ascii"))
        broadcast("C. 3\n".encode("ascii"))
        broadcast("D. 4\n".encode("ascii"))

        for client in clients:
            client.send("YOURTURN".encode("ascii"))
            answer = client.recv(1024).decode("ascii")
            if answer == "B":
                index = clients.index(client)
                broadcast(f"{nicknames[index]} WONNNNNNNNNNNN".encode("ascii"))
                server.close()
                return

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nicknames.remove(nicknames[index])
            break


def main():
    start_socket()
    accepting_client()
    game_loop()

main()

