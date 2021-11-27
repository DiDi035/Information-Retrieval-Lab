import sys
import pygame
import socket
import threading

host = socket.gethostbyname("localhost")
port = 9989
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

pygame.init()
# width: 1000, height: 600
screen = pygame.display.set_mode((1000, 600))

# game's logo and name
pygame.display.set_caption("Da Quiz")
logo = pygame.image.load('media/logo.png')
pygame.display.set_icon(logo)

# fonts
font = pygame.font.Font('media/Brick Comic.ttf', 32)
title_font = pygame.font.Font('media/Brick Comic.ttf', 100)

# colors
darkGreen = (102, 128, 106)
lightGreen = (180, 198, 166)
orange = (255, 194, 134)
yellow = (255, 241, 175)

# global
GAME_START = False
nickname = ''
answer = ''
alert = ''

receivedMessage = ''
receivedError = ''
receivedTime = ''
receivedRemain = ''
receivedQuestion = ''
receivedAnswers = []
receivedPlayers = []


def receive():
    global receivedMessage, receivedError, receivedTime, receivedRemain, receivedQuestion, receivedAnswers, receivedPlayers
    while True:
        message = client.recv(1024).decode("ascii")
        message_arr = message.split("|")
        prefix = message_arr[0]
        print(message_arr)
        if prefix == "question":
            receivedQuestion = message_arr[1]
            receivedAnswers = []
            for i in range(2, 6):
                receivedAnswers.append(message_arr[i])
        elif prefix == "remainquestion":
            receivedRemain = message_arr[1]
        elif prefix == "wrongturn":
            receivedError = "This is not your turn !\n"
        elif prefix == "turn":
            receivedError = ''
            if message_arr[1] == nickname:
                receivedMessage = f"Your's turn\n"
            else:
                receivedMessage = f"{message_arr[1]}'s turn\n"
        elif prefix == "correct":
            receivedMessage = f"{message_arr[1]}'s answer is correct !!!!!\n"
        elif prefix == "incorrect":
            receivedMessage = f"{message_arr[1]}'s answer is wrong !!!!!\n"
        elif prefix == "passtonextplayer":
            receivedMessage = f"{message_arr[1]} refuse to answer this question\n"
        elif prefix == "notallowedtopass":
            receivedError = "You are only allowed to pass once each game"
        elif prefix == "remainplayers":
            receivedPlayers = []
            for player in message_arr:
                if player != "remainplayers":
                    receivedPlayers.append(player)


def renderWelcomePage():
    renderTitle = title_font.render("Da Quiz", True, darkGreen)
    # (width, height)
    screen.blit(renderTitle, (380, 100))

    renderAlert = font.render(
        alert, True, darkGreen)
    screen.blit(renderAlert, (380, 300))

    renderNickname = font.render(nickname, True, darkGreen)
    screen.blit(renderNickname, (400, 370))

    # (left, top) (width, height)
    input_box = pygame.Rect((380, 400), (300, 1))
    pygame.draw.rect(screen, (0, 0, 0), input_box)

    renderInstruction = font.render('Press Space to Start', True, darkGreen)
    screen.blit(renderInstruction, (380, 480))


def renderGamePage():
    global receivedMessage, receivedError, receivedTime, receivedRemain, receivedQuestion, receivedAnswers, receivedPlayers

    # render messages
    renderBg1 = pygame.Rect((300, 0), (700, 150))
    pygame.draw.rect(screen, yellow, renderBg1)
    renderMessage = font.render(receivedMessage, True, darkGreen)
    screen.blit(renderMessage, (400, 30))
    renderError = font.render(receivedError, True, darkGreen)
    screen.blit(renderError, (400, 100))
    renderTime = font.render(receivedTime, True, darkGreen)
    screen.blit(renderTime, (900, 50))
    divider1 = pygame.Rect((300, 150), (700, 1))
    pygame.draw.rect(screen, (0, 0, 0), divider1)

    # render list of users
    renderBg2 = pygame.Rect((0, 0), (300, 600))
    pygame.draw.rect(screen, orange, renderBg2)
    renderRemain = font.render('Remain: ' + receivedRemain, True, darkGreen)
    screen.blit(renderRemain, (60, 20))
    for i in range(len(receivedPlayers)):
        text = font.render(str(i + 1) + '. ' +
                           receivedPlayers[i], True, darkGreen)
        screen.blit(text, (50, i * 80 + 100))
    divider2 = pygame.Rect((300, 0), (1, 600))
    pygame.draw.rect(screen, (0, 0, 0), divider2)

    # render question and answers
    for i in range(0, len(receivedQuestion), 50):
        renderQuestion = font.render(
            receivedQuestion[i:i+50], True, darkGreen)
        screen.blit(renderQuestion, (350, i*20 + 180))

    posX = [400, 400, 700, 700]
    posY = [300, 400, 300, 400]
    keys = ['A. ', 'B. ', 'C. ', 'D. ']
    for i in range(len(receivedAnswers)):
        renderAnswer = font.render(keys[i] + receivedAnswers[i], True, darkGreen)
        screen.blit(renderAnswer, (posX[i], posY[i]))

    # render instructions
    renderInstruction1 = font.render(
        "Press A or B or C or D to answer", True, darkGreen)
    screen.blit(renderInstruction1, (400, 500))
    renderInstruction2 = font.render("Press Q to pass", True, darkGreen)
    screen.blit(renderInstruction2, (400, 550))


receive_thread = threading.Thread(target=receive)

while True:
    screen.fill(lightGreen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if GAME_START:
                if event.key == pygame.K_a or event.key == pygame.K_b or event.key == pygame.K_c or event.key == pygame.K_d or event.key == pygame.K_q:
                    answer = event.unicode
                    print(answer)
                    client.send(answer.encode("ascii"))
                else:
                    answer = ''
            else:
                if event.key == pygame.K_SPACE:
                    if nickname == '':
                        alert = 'Please type in your nickname'
                    else:
                        # check nickname
                        client.send(nickname.encode("ascii"))
                        message = client.recv(1024).decode("ascii")
                        if message == "valid":
                            receive_thread.start()
                            GAME_START = True
                        else:
                            alert = 'This nickname is taken'
                elif event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                else:
                    if len(nickname) < 10:
                        nickname += event.unicode
    if GAME_START:
        renderGamePage()
    else:
        renderWelcomePage()

    pygame.display.update()
