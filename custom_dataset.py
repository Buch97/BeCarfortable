import os

import matplotlib.pyplot as plt
import torch
from PIL import Image
from cv2 import cv2
from setuptools import glob
from torch.utils.data import Dataset


class CustomDataset(Dataset):
    def __init__(self):
        self.imgs_path = "facial_expressions"
        file_list = glob.glob(self.imgs_path + "*")
        print(file_list)
        self.data = []
        for img in os.listdir(self.imgs_path):
            print(img)
            self.data.append("facial_expressions/"+img)
        print(self.data)
        # self.class_map = {"person": 0}
        self.img_dim = (256, 256)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path = self.data[idx]
        print(img_path)
        img = cv2.imread(img_path)
        img = cv2.resize(img, self.img_dim)
        # class_id = self.class_map[class_name]
        img_tensor = torch.from_numpy(img)
        img_tensor = img_tensor.permute(2, 0, 1)
        # class_id = torch.tensor([class_id])
        return img_tensor.float()
