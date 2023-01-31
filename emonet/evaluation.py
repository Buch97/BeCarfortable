import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image
from cv2 import cv2

emotions = {0: "neutral",
            1: "happy",
            2: "sad",
            3: "surprise",
            4: "fear",
            5: "disgust",
            6: "angry",
            7: "contempt"}


def evaluate(net, image):
    # for file in os.listdir('facial_expressions'):
    # print(file)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(image, (256, 256))
    img = Image.fromarray(img)
    fun = transforms.ToTensor()
    img = fun(img)

    image = img.unsqueeze(0)

    with torch.no_grad():
        out = net(image)

    emotion = torch.softmax(out['expression'][0], dim=0)
    index = emotion.argmax(dim=0).item()
    # print("EXPRESSION: " + str(index))

    # expr = out['expression']
    # val = out['valence']
    # ar = out['arousal']

    # val = np.squeeze(val.cpu().numpy())
    # ar = np.squeeze(ar.cpu().numpy())
    # print("VAL: " + str(val))
    # print("AR: " + str(ar))
    # print("-------------------------------------------------")

    # expression_pred = np.concatenate([expr, expression_pred])
    return emotions.get(index)
