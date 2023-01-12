import os
import torchvision.transforms as transforms
import numpy as np
import torch
from cv2 import cv2

from matplotlib import pyplot as plt
from torch import nn


def softmax(z):
    assert len(z.shape) == 2

    s = np.max(z, axis=1)
    s = s[:, np.newaxis]
    e_x = np.exp(z - s)
    div = np.sum(e_x, axis=1)
    div = div[:, np.newaxis]
    return e_x / div


def evaluate(net):
    net.eval()

    for file in os.listdir('facial_expressions'):
        print(file)
        img = cv2.imread('facial_expressions/' + file, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (256, 256))

        img_tensor = torch.from_numpy(img)
        img_tensor = img_tensor.permute(2, 0, 1)
        image = img_tensor.float().to('cpu')
        image = image.reshape(1, 3, 256, 256)

        with torch.no_grad():
            out = net(image)

        expr = out['expression']
        val = out['valence']
        ar = out['arousal']
        print("Output expression tensor: " + str(expr))

        softmax_expression = nn.functional.softmax(expr)
        expr = np.argmax(np.squeeze(softmax_expression.cpu().numpy()))
        print("EXPR: " + str(expr))

        val = np.squeeze(val.cpu().numpy())
        ar = np.squeeze(ar.cpu().numpy())
        print("VAL: " + str(val))
        print("AR: " + str(ar))

        # expression_pred = np.concatenate([expr, expression_pred])
    return
