import os

import torchvision.transforms as transforms
import numpy as np
import torch
from PIL import Image
from cv2 import cv2

from matplotlib import pyplot as plt
from torch import nn

from emonet.data_augmentation import DataAugmentor


def evaluate(net):

    for file in os.listdir('facial_expressions'):
        print(file)
        img = cv2.imread('facial_expressions/' + file, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (256, 256))
        img = Image.fromarray(img)
        fun = transforms.ToTensor()
        img = fun(img)

        image = img.unsqueeze(0)

        with torch.no_grad():
            out = net(image)


        print(out['expression'])
        emotion = torch.softmax(out['expression'][0], dim=0)
        index = emotion.argmax(dim=0).item()
        print("INDEX: " + str(index))

        # expr = out['expression']
        val = out['valence']
        ar = out['arousal']

        val = np.squeeze(val.cpu().numpy())
        ar = np.squeeze(ar.cpu().numpy())
        print("VAL: " + str(val))
        print("AR: " + str(ar))
        print("-------------------------------------------------")

        # expression_pred = np.concatenate([expr, expression_pred])
    return
