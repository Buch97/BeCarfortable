import ftplib
import io
import os

import cv2 as cv2
import numpy as np
from emonet.evaluation import evaluate
from server.emotionDetector import classifyDeepFace
from test import load_emonet

session = ftplib.FTP('192.168.1.59', 'pucci', 'pi')
filezilla_folder = '../resources/frames/'
net = load_emonet()

while True:
    # wait frame from raspberry
    print('Waiting new frame to process...')

    while os.listdir(filezilla_folder) is None:
        pass

    print('New frame arrived! Start processing...')
    frame = os.listdir(filezilla_folder).pop()
    file = str(filezilla_folder) + str(frame)

    # retrieve file from server folder
    r = io.BytesIO()
    ftpResponse = session.retrbinary('RETR ' + str(frame), r.write)
    print(ftpResponse)

    # binary to jpg conversion
    image = np.asarray(bytearray(r.getvalue()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # compute emotion on both models
    emonet_result = evaluate(net, image)
    deepface_result = classifyDeepFace(image)

    cv2.imwrite("../resources/output/" + str(frame), image)

    # if pop operation not enough
    ftpResponse = session.delete(str(frame))
    print(ftpResponse)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

session.quit()

