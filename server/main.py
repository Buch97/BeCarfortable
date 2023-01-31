import argparse
import ftplib
import threading

import cv2
from PIL import Image

from server.analyzeFrame import receiveFrame
from server.socketServer import receiveExcludedEmotion

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='serverModule')
    parser.add_argument('-classifier', '--classifier', nargs=1, choices=['emonet', 'deepface'], default='emonet')
    args = parser.parse_args()
    classifier = args.classifier[0]

    session = ftplib.FTP('192.168.1.59', 'pucci', 'pi')
    session.encoding = 'utf-8'
    excluded_emotion = receiveExcludedEmotion()

    t1 = threading.Thread(target=receiveFrame, args=(classifier,excluded_emotion,))

    t1.start()
