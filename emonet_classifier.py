import argparse
from pathlib import Path

import cv2
import torch
from emonet.models import EmoNet

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

        ret, frame = vid.read(cv2.IMREAD_COLOR)

        if ret:
            if frame_count % (interval * fps) == 0:
                face = face_cascade.detectMultiScale(frame, 1.1, 4)
                X, Y, W, H = face[0]
                img = frame[int(Y):int(Y + H), int(X):int(X + W)]
                cv2.imwrite("facial_expressions/frame%d.jpg" % (frame_count / 10), img)

            # frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
            cv2.imshow('Cam', frame)
            frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


def load_emonet():
    torch.backends.cudnn.benchmark = True


    # Parameters of the experiments
    n_expression = 8
    batch_size = 1
    n_workers = 1
    device = 'cpu'
    image_size = 256
    subset = 'test'

    print(f'Testing the model on {n_expression} emotional classes')

    # capture_video()
    # dataset = CustomDataset()
    # data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    state_dict_path = Path(__file__).parent.joinpath('pretrained', f'emonet_{n_expression}.pth')

    print(f'Loading the model from {state_dict_path}.')
    state_dict = torch.load(str(state_dict_path), map_location='cpu')
    state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}

    net = EmoNet(n_expression=n_expression).to('cpu')
    net.load_state_dict(state_dict, strict=False)
    net.eval()

    print(f'------------------------')
    # evaluate(net)
    return net
