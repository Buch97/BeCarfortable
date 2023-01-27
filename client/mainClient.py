import ftplib
import os
import time
import cv2 as cv2
import picamera
from picamera.array import PiRGBArray


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
            image = face_detection(image)
            cv2.imwrite('frames/' + nameFile, image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except:
            print('Face not detected')
            continue

        try:
            file = open('frames/frame' + str(frame_count) + '.jpg', 'rb')
            ftpResponse = session.storbinary(f'STOR {nameFile}', file)
            print(ftpResponse)
        except:
            print('Send failed')
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    session.quit()
    camera.stop_recording()
    camera.stop_preview()


def face_detection(img):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        face = img[y:y + h, x:x + w]
        return face


if __name__ == '__main__':

    emotion_list = ['sad', 'angry', 'disgust', 'happy', 'fear', 'surprise']
    while True:
        print("Welcome to the demo of the project of Industrial Application.\nType the emotion that you don't want to "
              "feel ", end='')
        print(emotion_list, end=':\n')

        text = input()
        if text not in emotion_list:
            print("Emotion not supported.")
        else:
            break

    print("Starting the video...")
    isExist = os.path.exists("frames")
    if not isExist:
        os.makedirs("frames")

    capture_video()


