import socket

ip = "192.168.1.59"
ipRaspberry = "192.168.1.54"


def sendExcludeEmotion(excluded_emotion):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.connect((ip, 8080))
    encodedMessage = bytes(excluded_emotion, 'utf-8')

    serv.send(encodedMessage)

    encodedAckText = serv.recv(1024)
    ackText = encodedAckText.decode('utf-8')

    if ackText == "OK":
        print('server acknowledged reception of text')
    else:
        print('error: server has sent back ' + ackText)


def receiveMessageSkip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ipRaspberry, 8080))
    sock.listen()
    conn, addr = sock.accept()
    encodedMessage = bytes("OK", 'utf-8')

    while 1:
        skip = conn.recv(4096).decode()

        if skip != "skip":
            print("SERVER: Input not valid.")
            continue
        else:
            print("SERVER: Message received: " + skip + ".")
            conn.send(encodedMessage)
            # submitVideo()
