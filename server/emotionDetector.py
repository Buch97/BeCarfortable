from deepface import DeepFace


def classifyDeepFace(frame):
    # compareDetectionBackends(img_path)
    try:
        obj = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        print(obj['dominant_emotion'])
        emotion = [obj['dominant_emotion']]
        return emotion
    except:
        print('Deepface classification failed')
