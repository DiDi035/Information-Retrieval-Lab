import socket
import threading

nickname = input("Choose a nickname: ")
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
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICKNAME":
                client.send(nickname.encode("ascii"))
            elif message == "YOURTURN":
                print("Your turn to answer !!!")
                answer = input("Answer: ")
                client.send(answer.encode("ascii"))
            else:
                print(message)
        except:
            print("An error occurred")
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
