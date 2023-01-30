import cv2
from deepface import DeepFace


def classifyDeepFace(frame):
    try:
        obj = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = obj[0]['dominant_emotion']
        return emotion
    except:
        print('Deepface classification failed')
