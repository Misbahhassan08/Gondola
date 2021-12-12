import cv2
import jetson.inference
import jetson.utils
import time
import threading
from PIL import Image
import numpy as np
import imutils

import os
# os.environ['LD_PRELOAD'] = '/usr/lib/aarch64-linux-gnu/libgomp.so.1'

from HumanTracker.common.ImageHelper import ImageHelper
from HumanTracker.Tracker import Tracker
import cv2
from dotenv import load_dotenv


class AI(threading.Thread):
    def __init__(self, ROOT_PATH, cam_number, gender_cam, threshold):
        threading.Thread.__init__(self)
        self.th = threshold
        self.net = jetson.inference.detectNet("ssd-mobilenet-v2", 0.01)
        self.camera_number = cam_number
        self.gender_cam = gender_cam

        self.ROOT_PATH = ROOT_PATH
        self.Max_cameras = len(self.camera_number)

        self.average = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.count = [0, 0, 0, 0, 0]

        self.MAX = [100, 30, 30, 30, 30]

        self.total_bottles = [0, 0, 0, 0, 0]
        self.return_camera_test = []

        self.gender = None
        self.bol_gender = False

        self.faceImage = "FaceTrack.jpg"

        for x in range(len(self.camera_number)):
            self.return_camera_test.append({
                "ID": self.camera_number[x],
                "Name": "shelf_{}_camera".format(x),
                "file": "shelf_{}_camera.jpg".format(x),
                "file_AI": "shelf_{}_camera_AI.jpg".format(x),
                "total_bottles": 0,
                "Status": False
            })
        self.gender_camera_status = False

        # print(self.test_cameras())

        self.loop = True

        self.screenshoot = '{}/screen.jpg'.format(self.ROOT_PATH)
        execution_provider = os.environ.get(
            'EXECUTION_PROVIDER', 'CUDAExecutionProvider')
        self.match_thresh = os.environ.get('MATCH_THRESH', 0.6)
        self.track_thresh = os.environ.get('TRACK_THRESH', 0.4)
        self.min_box_area = os.environ.get('MIN_BOX_AREA', 100000)

        print("Model Path: " + os.environ.get('MODEL_PATH'))
        self.tracker = Tracker(min_face_area=2000, execution_provider=execution_provider,
                          match_thresh=self.match_thresh, track_thresh=self.track_thresh, min_box_area=self.min_box_area,
                          model_path=os.environ.get('MODEL_PATH'))

    def test_camera_gender(self):
        cap = cv2.VideoCapture(self.gender_cam)
        hasFrame, frame = cap.read()
        time.sleep(1)
        if hasFrame:
            self.gender_camera_status = True
        else:
            self.gender_camera_status = False
        cap.release()
        return self.gender_camera_status
        pass  # end of check_camera_status

    def test_cameras_bottle(self):

        for x in range(self.Max_cameras):
            cap = cv2.VideoCapture(self.camera_number[x])
            time.sleep(1)
            ret, frame = cap.read()
            if len(frame) > 0:
                self.return_camera_test[x]["Status"] = True
            else:
                self.return_camera_test[x]["Status"] = False
            cap.release()
        return self.return_camera_test

    def get_cameras_status(self):
        return self.return_camera_test

    def run(self):
        _count = 0
        _timeLimit = 10
        while self.loop:

            if _count >= _timeLimit:
                # write all bottle images
                for x in range(len(self.camera_number)):
                    cap = cv2.VideoCapture(self.return_camera_test[x]["ID"])
                    # time.sleep(0.1)
                    ret, frame = cap.read()
                    # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    im_pil = Image.fromarray(frame)

                    im_pil.save(self.return_camera_test[x]["file"], format='JPEG')

                    cap.release()
                    # time.sleep(0.3)
                # read all images
                for x in range(len(self.camera_number)):
                    frame = cv2.imread(self.return_camera_test[x]["file"])
                    frame = cv2.resize(frame, (640, 480))
                    imgCuda = jetson.utils.cudaFromNumpy(frame)
                    detections = self.net.Detect(imgCuda)

                    i = 0
                    for d in detections:
                        x1, y1, x2, y2 = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
                        className = self.net.GetClassDesc(d.ClassID)
                        if className == "bottle":
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                            cv2.putText(frame, className, (x1 + 5, y1 + 15), cv2.FONT_HERSHEY_DUPLEX, 0.75,
                                        (255, 0, 255),
                                        2)
                            i = i + 1
                    self.count[x] = self.count[x] + 1
                    self.average[x] = self.average[x] + i

                    # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    im_pil = Image.fromarray(frame)

                    im_pil.save(self.return_camera_test[x]["file_AI"], format='JPEG')

                    if self.count[x] == 10:
                        self.average[x] = self.average[x] / 10
                        # print(self.average[x])
                        self.total_bottles[x] = int(self.average[x])  # / 10)
                        self.count[x] = 0
                    if self.total_bottles[x] > self.MAX[x]:
                        self.total_bottles[x] = self.MAX[x]
                    if self.total_bottles[x] < 0:
                        self.total_bottles[x] = 0

                    self.return_camera_test[x]["total_bottles"] = self.total_bottles[x]
                # print(self.return_camera_test)
                _count = 0
            _count = _count + 1

            # write gender image

            cap = cv2.VideoCapture(self.gender_cam)
            ret, frame = cap.read()
            if ret:
                self.tracker.process(frame)
                # show total at the bottom of the image
                cv2.putText(frame, " M: {}, F: {}: U: {}".format(self.tracker.male, self.tracker.female, self.tracker.unknown),
                            (200, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.putText(frame, str(self.tracker.total), (10,
                                                        frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255),
                            3)

            frame_detection = frame
            im_pil = Image.fromarray(frame_detection)
            im_pil.save(self.faceImage, format='JPEG')

            cap.release()
            # time.sleep(0.3)
