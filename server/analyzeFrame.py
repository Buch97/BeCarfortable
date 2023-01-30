import ftplib
import io
import os
import time

import cv2 as cv2
import numpy as np
from PIL import Image

from emonet.evaluation import evaluate
from server.emotionDetector import classifyDeepFace
from server.socketServer import receiveExcludedEmotion
from emonet_classifier import load_emonet


def receiveFrame():
    while True:
        # wait frame from raspberry
        print('Waiting new frame to process...')
        # time.sleep(10)

        # while len(os.listdir(filezilla_folder)) == 0:
        #  pass

        print('New frame arrived! Start processing...')
        # frame = os.listdir(filezilla_folder).pop()
        file = str(filezilla_folder) + 'frame0.jpg'

        image_path = '../resources/frames/frame0.jpg'

        image = cv2.imread(image_path, cv2.IMREAD_COLOR)

        emonet_result = evaluate(net, image)
        deepface_result = classifyDeepFace(image_path)
        print("Emonet detect --> " + emonet_result)
        print("DeepFace detect --> " + str(deepface_result))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    session.quit()

receiveFrame()