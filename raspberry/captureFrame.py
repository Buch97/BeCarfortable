import ftplib
import os
import time
import cv2 as cv2
# import picamera
# from picamera.array import PiRGBArray

from socketRaspberry import sendExcludedEmotion


def capture_video():
    session = ftplib.FTP('192.168.1.59')
    session.login('pucci', 'pi')
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30

    camera.start_preview()
    time.sleep(2)

    frame_count = 0

    rawCapture = PiRGBArray(camera, size=(640, 480))

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        rawCapture.truncate(0)

        try:
            nameFile = 'frame' + str(frame_count) + '.jpg'
            img = face_detection(image)
            cv2.imwrite('frames/' + nameFile, img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except:
            print('Face not detected')
            continue

        try:
            file = open('frames/frame' + str(frame_count) + '.jpg', 'rb')
            ftpResponse = session.storbinary(f'STOR {nameFile}', file)
            print(ftpResponse)
            frame_count += 1
        except:
            print('Send failed')
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    session.quit()
    camera.stop_recording()
    camera.stop_preview()


def face_detection(img):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]
        return face







