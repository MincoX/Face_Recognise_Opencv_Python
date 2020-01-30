import cv2
import numpy as np


class Recognise:
    """人脸识别"""

    def __init__(
            self,
            recognise_path,
            train_yml='F:/Program/Tensorflow/case/01.face_server_opencv/opencv_server/train.yml'
    ):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(train_yml)
        self.cascade = cv2.CascadeClassifier('D:/Opencv/build/etc/haarcascades/haarcascade_frontalface_default.xml')
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.video = cv2.VideoCapture(0)
        self.recognise_path = recognise_path

    def recognise(self):
        repath = 'F:/Program/Tensorflow/case/01.face_server_opencv/static/cutout/' + self.recognise_path
        img = cv2.imread(repath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_id, conf = self.recognizer.predict(gray)
        if conf > 50:
            if img_id == 1:
                img_id = f'xh:{conf}'
            elif img_id == 2:
                img_id = 'gm'
        else:
            img_id = "Unknown"

        print(f'识别结果： {img_id}')

    @classmethod
    def run(cls, recognise_path):
        runner = cls(recognise_path)
        runner.recognise()


# class Recognise:
#     """人脸识别"""
#
#     def __init__(self, train_yml='train.yml'):
#         self.recognizer = cv2.face.LBPHFaceRecognizer_create()
#         self.recognizer.read(train_yml)
#         self.cascade = cv2.CascadeClassifier('D:/Opencv/build/etc/haarcascades/haarcascade_frontalface_default.xml')
#         self.font = cv2.FONT_HERSHEY_SIMPLEX
#         self.video = cv2.VideoCapture(0)
#
#     def video_frame(self):
#         """
#         获取视频中的每一帧
#         :return:
#         """
#         c = 1
#         time_frame = 10
#         while self.video.isOpened():
#             if c > 10000:
#                 c = 1
#             suc, frame = self.video.read()
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#             if suc and (c % time_frame == 0):
#                 self.detect_face(frame, gray)
#             c += 1
#
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#
#     def detect_face(self, frame, gray):
#         """
#         检测人脸
#         :return:
#         """
#         face_areas = self.cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
#         for (x, y, w, h) in face_areas:
#             cv2.rectangle(frame, (x - 50, y - 50), (x + w + 50, y + h + 50), (225, 0, 0), 2)
#             img_id, conf = self.recognizer.predict(gray[y:y + h, x:x + w])
#             if conf > 70:
#                 if img_id == 1:
#                     img_id = f'xh:{conf}'
#                 elif img_id == 2:
#                     img_id = 'gm'
#             else:
#                 img_id = "Unknown"
#             cv2.putText(frame, str(img_id), (x, y), self.font, 1, (0, 255, 0), 1)
#             cv2.imshow('im', frame)
#
#     @classmethod
#     def run(cls):
#         runner = cls()
#         runner.video_frame()
#
#
# if __name__ == '__main__':
#     Recognise.run()


if __name__ == '__main__':
    Recognise.run()
