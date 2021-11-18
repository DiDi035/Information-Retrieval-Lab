import socket
import threading

nickname = input("Choose a nickname: ")
host = socket.gethostbyname("localhost")
port = 9989
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def write():
    while True:
        message = input(f"{nickname}: ")
        client.send(message.encode("ascii"))

def receive():
    while True:
        message = client.recv(1024).decode("ascii")
        if message == "NICKNAME":
            client.send(nickname.encode("ascii"))
        else:
            print(message)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()