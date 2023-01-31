import argparse
from pathlib import Path

import cv2
import torch
from emonet.models import EmoNet

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def load_emonet():
    torch.backends.cudnn.benchmark = True
    n_expression = 8

    print(f'Testing the model on {n_expression} emotional classes')

    state_dict_path = Path(__file__).parent.joinpath('pretrained', f'emonet_{n_expression}.pth')

    print(f'Loading the model from {state_dict_path}.')
    state_dict = torch.load(str(state_dict_path), map_location='cpu')
    state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}

    net = EmoNet(n_expression=n_expression).to('cpu')
    net.load_state_dict(state_dict, strict=False)
    net.eval()

    print(f'------------------------')
    return net
