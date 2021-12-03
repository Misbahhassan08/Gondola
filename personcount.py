import cv2
import jetson.inference
import jetson.utils
import time
import threading
from PIL import Image
import numpy as np
import os
import getpass


class pd(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        self.ID = getpass.getuser()  # machine ID should be the unique

        self.net = jetson.inference.detectNet("ssd-mobilenet-v2", 0.02)

        self.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

        self.faceImage = "11.jpg"

        self.loop = True

        self.screenshoot = '{}/screen.jpg'.format(self.ROOT_PATH)

    def run(self):

        while self.loop:
            # test
            cap = cv2.VideoCapture(5)
            ret, fram = cap.read()
            fram = cv2.resize(fram, (640, 480))

            im_pil = Image.fromarray(fram)
            im_pil.save("11.jpg", format='JPEG')
            cap.release()

            frame = cv2.imread("11.jpg")
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            imgCuda = jetson.utils.cudaFromNumpy(frame)
            detections = self.net.Detect(imgCuda)
            print("-------------------------",len(detections))
            for d in detections:
                x1, y1, x2, y2 = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
                className = self.net.GetClassDesc(d.ClassID)
                if className == "person":
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                    cv2.putText(frame, className, (x1 + 5, y1 + 15), cv2.FONT_HERSHEY_DUPLEX, 0.75,
                                        (255, 0, 255),
                                        2)
            im_pil = Image.fromarray(frame)
            im_pil.save("12.jpg", format='JPEG')



            # time.sleep(0.3)
if __name__ == '__main__':
    status = False
    mainobj = pd()
    mainobj.start()
