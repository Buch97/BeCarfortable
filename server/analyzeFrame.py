import time

import cv2 as cv2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from emonet.evaluation import evaluate
from emonet_classifier import load_emonet
from server.emotionDetector import classifyDeepFace

filezilla_folder = '../resources/frames/'


class FileHandler(FileSystemEventHandler):
    def __init__(self, classifier):
        if classifier == 'emonet':
            self.net = load_emonet()
        else:
            self.net = None

    def on_created(self, event):
        print('New frame %s has arrived! Start processing...' % event.src_path)
        image_path = event.src_path
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)

        if self.net is not None:
            emonet_result = evaluate(self.net, image)
            print("Emonet detect --> " + emonet_result)
        else:
            deepface_result = classifyDeepFace(image_path)
            print("DeepFace detect --> " + str(deepface_result))


def receiveFrame(classifier):
    while True:

        # wait frame from raspberry
        print('Waiting new frame to process...')
        # time.sleep(10)

        observer = Observer()
        event_handler = FileHandler(classifier)
        observer.schedule(event_handler, path='/folder/to/watch')
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # receiveFrame()
