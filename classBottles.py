import cv2
import jetson.inference
import jetson.utils
import time
import threading
import io
from PIL import Image


class Bottles(threading.Thread):
    def __init__(self, cam_number, gender_cam, threshold):
        threading.Thread.__init__(self)
        self.th = threshold
        self.net = jetson.inference.detectNet("ssd-mobilenet-v2", 0.01)
        self.camera_number = cam_number
        self.gender_cam = gender_cam

        self.Max_cameras = len(self.camera_number)

        self.average = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.count = [0, 0, 0, 0, 0]

        self.MAX = [100, 30, 30, 30, 30]

        self.total_bottles = [0, 0, 0, 0, 0]
        self.return_camera_test = []
        for x in range(len(self.camera_number)):
            self.return_camera_test.append({
                "ID": self.camera_number[x],
                "Name": "shelf_{}_camera".format(x),
                "file": "shelf_{}_camera.jpg".format(x),
                "file_AI":"shelf_{}_camera_AI.jpg".format(x),
                "total_bottles": 0,
                "Status": False
            })
        self.gender_camera_status = False

        # print(self.test_cameras())

        self.loop = True

        # -----------------------------------------------------

        self.male_detected = False
        self.female_detected = False

        faceProto = "/home/misbah/dev/V3/opencv_face_detector.pbtxt"
        faceModel = "/home/misbah/dev/V3/opencv_face_detector_uint8.pb"
        ageProto = "/home/misbah/dev/V3/age_deploy.prototxt"
        ageModel = "/home/misbah/dev/V3/age_net.caffemodel"
        genderProto = "/home/misbah/dev/V3/gender_deploy.prototxt"
        genderModel = "/home/misbah/dev/V3/gender_net.caffemodel"

        self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        self.ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
        self.genderList = ['Male', 'Female']

        self.faceNet = cv2.dnn.readNet(faceModel, faceProto)
        self.ageNet = cv2.dnn.readNet(ageModel, ageProto)
        self.genderNet = cv2.dnn.readNet(genderModel, genderProto)

        self.padding = 20

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

    def highlightFace(self, net, frame, conf_threshold):
        frameOpencvDnn = frame.copy()
        frameHeight = frameOpencvDnn.shape[0]
        frameWidth = frameOpencvDnn.shape[1]
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections = net.forward()
        faceBoxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                faceBoxes.append([x1, y1, x2, y2])
                cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
        return frameOpencvDnn, faceBoxes

    def run(self):
        while self.loop:

            # write all bottle images
            for x in range(len(self.camera_number)):
                cap = cv2.VideoCapture(self.return_camera_test[x]["ID"])
                #time.sleep(0.1)
                ret, frame = cap.read()
                #img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(frame)

                im_pil.save(self.return_camera_test[x]["file"], format='JPEG')

                cap.release()
                #time.sleep(0.3)

            # write gender image
            cap = cv2.VideoCapture(self.gender_cam)
            #time.sleep(0.1)
            ret, frame = cap.read()
            frame = cv2.resize(frame, (640, 480))  # 420,180
            resultImg, faceBoxes = self.highlightFace(self.faceNet, frame, 0.4)

            if not faceBoxes:
                print("No face detected")

            for faceBox in faceBoxes:
                face = frame[max(0, faceBox[1] - self.padding):
                             min(faceBox[3] + self.padding, frame.shape[0] - 1), max(0, faceBox[0] - self.padding)
                                                                                 :min(faceBox[2] + self.padding,
                                                                                      frame.shape[1] - 1)]

                blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
                self.genderNet.setInput(blob)
                genderPreds = self.genderNet.forward()
                gender = self.genderList[genderPreds[0].argmax()]
                print(f'--------------------------Gender------------------- : {gender}')

                self.ageNet.setInput(blob)
                agePreds = self.ageNet.forward()
                age = self.ageList[agePreds[0].argmax()]
                print(f'Age: {age[1:-1]} years')

                if gender == 'Male':
                    self.male_detected = True
                    self.female_detected = False
                    pass
                elif gender == 'Female':
                    self.female_detected = True
                    self.male_detected = False
                    pass
            img = cv2.cvtColor(resultImg, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)

            im_pil.save("FaceImage.jpg", format='JPEG')

            cap.release()
            #time.sleep(0.3)

            # read all images
            for x in range(5):
                frame = cv2.imread(self.return_camera_test[x]["file"])
                frame = cv2.resize(frame,(1640,1480))
                imgCuda = jetson.utils.cudaFromNumpy(frame)
                detections = self.net.Detect(imgCuda)

                i = 0
                for d in detections:
                    x1, y1, x2, y2 = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
                    className = self.net.GetClassDesc(d.ClassID)
                    if className == "bottle":
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                        cv2.putText(frame, className, (x1 + 5, y1 + 15), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 0, 255),
                                    2)
                        i = i + 1
                self.count[x] = self.count[x] + 1
                self.average[x] = self.average[x] + i

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(img)

                im_pil.save(self.return_camera_test[x]["file_AI"], format='JPEG')
                
                if self.count[x] == 10:
                    self.average[x] = self.average[x] / 10
                    print(self.average[x])
                    self.total_bottles[x] = int(self.average[x])#/ 10)
                    self.count[x] = 0
                if self.total_bottles[x] > self.MAX[x]:
                    self.total_bottles[x] = self.MAX[x]
                if self.total_bottles[x] < 0:
                    self.total_bottles[x] = 0

                self.return_camera_test[x]["total_bottles"] = self.total_bottles[x]
            print(self.return_camera_test)
