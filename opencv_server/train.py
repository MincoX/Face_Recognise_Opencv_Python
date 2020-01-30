import os

import cv2
import numpy as np
from PIL import Image


class Train:
    """训练人脸，获得 xml 文件"""

    def __init__(self, train_path='../static/train/'):
        self.detector = cv2.CascadeClassifier('D:/Opencv/build/etc/haarcascades/haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.train_path = train_path
        self.train_info = self.train

    @property
    def train(self):
        train_faces = []
        ids = []
        for img_path in os.listdir(self.train_path):
            print(img_path)
            image = Image.open(os.path.join(self.train_path, img_path)).convert('L')
            image_np = np.array(image, 'uint8')

            if os.path.split(img_path)[-1].split(".")[-1] != 'jpg':
                continue

            image_id = int(os.path.split(img_path)[-1].split(".")[1])
            faces = self.detector.detectMultiScale(image_np)

            for (x, y, w, h) in faces:
                train_faces.append(image_np[y:y + h, x:x + w])
                ids.append(image_id)

        return train_faces, ids

    def get_xml(self):

        self.recognizer.train(self.train_info[0], np.array(self.train_info[1]))
        self.recognizer.save('train.yml')

    @classmethod
    def run(cls):
        runner = cls()
        runner.get_xml()


if __name__ == '__main__':
    Train.run()
