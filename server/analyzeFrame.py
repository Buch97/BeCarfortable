import time

import cv2 as cv2
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from emonet.evaluation import evaluate
from emonet_classifier import load_emonet
from server.emotionDetector import classifyDeepFace
from server.socketServer import send_skip

filezilla_folder = '../resources/frames/'

class FileHandler(FileSystemEventHandler):
    def __init__(self, classifier, emotion):
        self.emotion = emotion
        self.emotion_count = 0
        if classifier == 'emonet':
            self.net = load_emonet()
        else:
            self.net = None

    def on_created(self, event):
        print('New frame %s has arrived! Start processing...' % event.src_path)
        image_path = event.src_path
        time.sleep(0.2)

        image = cv2.imread(image_path)

        if self.net is not None:
            result = evaluate(self.net, image)
            print("Emonet detect --> " + result)
        else:
            result = classifyDeepFace(image)
            print("DeepFace detect --> " + str(result))

        if result == self.emotion:
            self.emotion_count += 1
        else:
            self.emotion_count = 0

        if self.emotion_count == 3:
            self.emotion_count = 0
            print("Sending skip message to Raspberry")
            send_skip()


def receiveFrame(classifier, emotion):
    while True:

        # wait frame from raspberry
        print('Waiting new frame to process...')
        # time.sleep(10)

        observer = Observer()
        event_handler = FileHandler(classifier, emotion)
        observer.schedule(event_handler, path='../frames')
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # receiveFrame()
