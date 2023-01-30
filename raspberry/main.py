import os
import threading

from raspberry.captureFrame import capture_video
from raspberry.playVideo import vlc_player
from raspberry.socketRaspberry import receiveMessageSkip, sendExcludedEmotion

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

    sendExcludedEmotion(text)

    print("Starting the video...")
    isExist = os.path.exists("frames")
    if not isExist:
        os.makedirs("frames")

    t1 = threading.Thread(target=capture_video)
    t2 = threading.Thread(target=vlc_player, args=(text,))
    t3 = threading.Thread(target=receiveMessageSkip)

    t1.start()
    t2.start()
    t3.start()
