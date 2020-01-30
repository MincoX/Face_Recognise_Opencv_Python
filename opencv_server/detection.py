import cv2
import datetime

from utils import logger, redis_pool
from asynchronous import tasks

time_list = []


class FaceDetect:

    def __init__(self, face_xml='D:/Opencv/build/etc/haarcascades/haarcascade_frontalface_alt.xml'):
        self.face_xml = cv2.CascadeClassifier(face_xml)
        self.video = cv2.VideoCapture(0)
        self.redis_cli = redis_pool.RedisModel()
        self.origin = None

    def video_frame(self):
        """
        获取视频中的每一帧
        :return:
        """
        c = 1
        time_frame = 10
        while self.video.isOpened():
            if c > 10000:
                c = 1
            suc, frame = self.video.read()
            if suc and (c % time_frame == 0):
                self.pretreatment(frame)
            c += 1

            self.pretreatment(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def pretreatment(self, frame):
        """
        图像预处理
        :return:
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.detect_face(frame, gray)

    def detect_face(self, frame, gray):
        """
        检测人脸
        :return:
        """
        face_areas = self.face_xml.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(80, 80))
        if len(face_areas) > 0:
            for face in face_areas:
                x, y, w, h = face
                face = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                cv2.rectangle(frame, (x - 10, y - 10), (x + h + 10, y + w + 10), (0, 255, 0), 2)
                self.save_face(face)

        cv2.imshow("Image", frame)

    def save_face(self, face):
        """
        保存人脸
        :param face:
        :return:
        """
        global time_list
        cur_time = datetime.datetime.now().strftime('%H:%M:%S')
        time_list.append(cur_time)

        if len(time_list) > 50:
            time_list.clear()
        else:
            return

        try:
            resize = cv2.resize(face, (200, 200), interpolation=cv2.INTER_CUBIC)
            cur_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            res = cv2.imwrite(f'../static/cutout/{cur_time}.jpg', resize)
            if res:
                logger.debug(f'>>> 图片 {cur_time}.jpg，保存成功！')
            tasks.recognise.delay(f'{cur_time}.jpg')
        except Exception as e:
            logger.info(e)

    @classmethod
    def run(cls):
        obj = cls()
        obj.video_frame()


if __name__ == '__main__':
    FaceDetect.run()
