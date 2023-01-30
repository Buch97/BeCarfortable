import argparse
import ftplib
import sys
import threading

from emonet_classifier import load_emonet
from server.analyzeFrame import receiveFrame
from server.socketServer import receiveExcludedEmotion


if __name__ == '__main__':
    session = ftplib.FTP('192.168.1.59', 'pucci', 'pi')
    session.encoding = 'utf-8'
    filezilla_folder = '../resources/frames/'
    net = load_emonet()
    emotion_count = 0

    # excluded_emotion = receiveExcludedEmotion()
    print("QUI")
    parser = argparse.ArgumentParser(prog='serverModule')
    parser.add_argument('--classifier', nargs=1, choices=['emonet', 'deepface'], default='emonet')
    print(str(parser.parse_args()))
    # t1 = threading.Thread(target=receiveExcludedEmotion)
    # t2 = threading.Thread(target=receiveFrame)

    # t1.start()
    # t1.join()
    # t2.start()
