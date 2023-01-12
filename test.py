import os

from pathlib import Path
import argparse

import torch
from cv2 import cv2
from emonet.models import EmoNet
from emonet.evaluation import evaluate

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def capture_video():
    vid = cv2.VideoCapture(0)
    scaling_factor = 1
    frame_count = 0
    interval = 1

    vid.set(cv2.CAP_PROP_POS_MSEC, (frame_count * 1000))
    vid.set(cv2.CAP_PROP_FPS, 60)
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    dominant_emotion_list = []

    while vid.isOpened():

        ret, frame = vid.read()

        if ret:
            if frame_count % (interval * fps) == 0:
                face = face_cascade.detectMultiScale(frame, 1.1, 4)
                X, Y, W, H = face[0]
                img = frame[int(Y):int(Y + H), int(X):int(X + W)]
                cv2.imwrite("facial_expressions/frame%d.jpg" % (frame_count / 10), img)

            frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
            cv2.imshow('Cam', frame)
            frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


# torch.backends.cudnn.benchmark = True

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--nclasses', type=int, default=8, choices=[5, 8],
                    help='Number of emotional classes to test the model on. Please use 5 or 8.')
args = parser.parse_args()

# Parameters of the experiments
n_expression = args.nclasses
batch_size = 1
n_workers = 1
device = 'cpu'
image_size = 256
subset = 'test'

print(f'Testing the model on {n_expression} emotional classes')

# Loading the model

frame_count = 0
for file in os.listdir('web_faces'):
    print(file)
    photo = cv2.imread('web_faces/' + file)
    face = face_cascade.detectMultiScale(photo, 1.1, 4)
    X, Y, W, H = face[0]
    img = photo[int(Y):int(Y + H), int(X):int(X + W)]
    cv2.imwrite("web_face_detected/face%d.jpg" % (frame_count), img)
    frame_count += 1

capture_video()
# dataset = CustomDataset()
# data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

state_dict_path = Path(__file__).parent.joinpath('pretrained', f'emonet_{n_expression}.pth')

print(f'Loading the model from {state_dict_path}.')
state_dict = torch.load(str(state_dict_path), map_location='cpu')
state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}

net = EmoNet(n_expression=n_expression).to('cpu')
net.load_state_dict(state_dict, strict=False)

print(f'------------------------')
evaluate(net)
