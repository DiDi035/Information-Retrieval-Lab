import socket
import threading

host = socket.gethostbyname("localhost")
port = 9989
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def write():
    while True:
        message = input("")
        client.send(message.encode("ascii"))

def receive():
    while True:
        message = client.recv(1024).decode("ascii")
        message_arr = message.split("|")
        prefix = message_arr[0]
        if prefix == "question":
            for item in message_arr:
                if item != "question":
                    print(item + "\n")
        elif prefix == "remainquestion":
            print(f"Remain questions: {message_arr[1]}\n")
        elif prefix == "wrongturn":
            print("This is not your turn !!!!!\n")
        elif prefix == "turn":
            print(f"{message_arr[1]}'s turn\n")
        elif prefix == "correct":
            print(f"{message_arr[1]}'s answer is correct !!!!!\n")
        elif prefix == "incorrect":
            print(f"{message_arr[1]}'s answer is wrong !!!!!\n")
        elif prefix == "passtonextplayer":
            print(f"{message_arr[1]} refuse to answer this question\n")
        elif prefix == "notallowedtopass":
            print("You are only allowed to pass once each game")
        elif prefix == "remainplayers":
            for player in message_arr:
                if player != "remainplayers":
                    print(player + "\n")

while True:
    nickname = input("Choose a nickname: ")
    client.send(nickname.encode("ascii"))
    message = client.recv(1024).decode("ascii")
    if message == "valid":
        break
    else:
        print("This nickname is taken")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
