import cv2
import jetson.inference
import jetson.utils
import time
import threading
from PIL import Image
import numpy as np
from centroidtracker import CentroidTracker
import imutils


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

        self.male_detected = False
        self.female_detected = False
        self.gender = None
        self.bol_gender = False

        self.faceImage = "FaceTrack.jpg"
        self.tempid = 0
        self.newid = False
        self.obid = 0
        self.send_count = 0

        protopath = "{}/MobileNetSSD_deploy.prototxt".format(self.ROOT_PATH)
        modelpath = "{}/MobileNetSSD_deploy.caffemodel".format(self.ROOT_PATH)
        self.detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                   "sofa", "train", "tvmonitor"]

        self.tracker = CentroidTracker(maxDisappeared=10, maxDistance=10)

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

        # -----------------------------------------------------

        self.male_detected = False
        self.female_detected = False

        faceProto = '{}/gender_files/models/opencv_face_detector.pbtxt'.format(self.ROOT_PATH)
        faceModel = '{}/gender_files/models/opencv_face_detector_uint8.pb'.format(self.ROOT_PATH)
        ageProto = '{}/gender_files/models/age_deploy.prototxt'.format(self.ROOT_PATH)
        ageModel = '{}/gender_files/models/age_net.caffemodel'.format(self.ROOT_PATH)
        genderProto = '{}/gender_files/models/gender_deploy.prototxt'.format(self.ROOT_PATH)
        genderModel = '{}/gender_files/models/gender_net.caffemodel'.format(self.ROOT_PATH)

        self.screenshoot = '{}/screen.jpg'.format(self.ROOT_PATH)

        self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 144.895847746) # (78.4263377603, 87.7689143744, 114.895847746)
        self.ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
        self.genderList = ['Male', 'Female']

        self.faceNet = cv2.dnn.readNet(faceModel, faceProto)
        self.ageNet = cv2.dnn.readNet(ageModel, ageProto)
        self.genderNet = cv2.dnn.readNet(genderModel, genderProto)
        self.padding = 20

    def non_max_suppression_fast(self, boxes, overlapThresh):
        try:
            if len(boxes) == 0:
                return []

            if boxes.dtype.kind == "i":
                boxes = boxes.astype("float")

            pick = []

            x1 = boxes[:, 0]
            y1 = boxes[:, 1]
            x2 = boxes[:, 2]
            y2 = boxes[:, 3]

            area = (x2 - x1 + 1) * (y2 - y1 + 1)
            idxs = np.argsort(y2)

            while len(idxs) > 0:
                last = len(idxs) - 1
                i = idxs[last]
                pick.append(i)

                xx1 = np.maximum(x1[i], x1[idxs[:last]])
                yy1 = np.maximum(y1[i], y1[idxs[:last]])
                xx2 = np.minimum(x2[i], x2[idxs[:last]])
                yy2 = np.minimum(y2[i], y2[idxs[:last]])

                w = np.maximum(0, xx2 - xx1 + 1)
                h = np.maximum(0, yy2 - yy1 + 1)

                overlap = (w * h) / area[idxs[:last]]

                idxs = np.delete(idxs, np.concatenate(([last],
                                                       np.where(overlap > overlapThresh)[0])))

            return boxes[pick].astype("int")
        except Exception as e:
            print("Exception occurred in non_max_suppression : {}".format(e))
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

    def get_gender_dect(self):
        if self.send_count <= self.obid:
            self.send_count = self.send_count + 1
            return[True, False]
        else:
            return [False, False]
        # return [self.male_detected, self.female_detected]
        pass
    

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
    
    def reset_gender(self):
        self.male_detected = False
        self.female_detected = False
        self.newid = False

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
                        #print(self.average[x])
                        self.total_bottles[x] = int(self.average[x])  # / 10)
                        self.count[x] = 0
                    if self.total_bottles[x] > self.MAX[x]:
                        self.total_bottles[x] = self.MAX[x]
                    if self.total_bottles[x] < 0:
                        self.total_bottles[x] = 0

                    self.return_camera_test[x]["total_bottles"] = self.total_bottles[x]
                #print(self.return_camera_test)
                _count = 0
            _count = _count + 1

            # write gender image
            
            cap = cv2.VideoCapture(self.gender_cam)
            ret, frame = cap.read()
            frame_detection = frame
            frame_detection = imutils.resize(frame_detection, width=600)

            (H, W) = frame_detection.shape[:2]
            blob_d = cv2.dnn.blobFromImage(frame_detection, 0.007843, (W, H), 127.5)
            self.detector.setInput(blob_d)
            person_detections = self.detector.forward()
            rects = []
            for i in np.arange(0, person_detections.shape[2]):
                confidence = person_detections[0, 0, i, 2]
                if confidence > 0.5:
                    idx = int(person_detections[0, 0, i, 1])

                    if self.CLASSES[idx] != "person":
                        continue

                    person_box = person_detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                    (startX, startY, endX, endY) = person_box.astype("int")
                    rects.append(person_box)

            boundingboxes = np.array(rects)
            boundingboxes = boundingboxes.astype(int)
            rects = self.non_max_suppression_fast(boundingboxes, 0.3)

            objects = self.tracker.update(rects)
            for (objectId, bbox) in objects.items():
                x1, y1, x2, y2 = bbox
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)

                cv2.rectangle(frame_detection, (x1, y1), (x2, y2), (0, 0, 255), 2)
                text = "ID: {}".format(objectId)
                cv2.putText(frame_detection, text, (x1, y1 - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
                self.obid= objectId
                print("---------------------------- > ID : ",objectId)
                #self.newid = True
            if self.tempid >= self.obid:
                pass
            else:
                self.tempid = self.obid
                self.newid = True
            try:
                frame = cv2.resize(frame, (640, 480))  # 420,180
                resultImg, faceBoxes = self.highlightFace(self.faceNet, frame, 0.4)
                self.gender = "None"
                if not faceBoxes:
                    #print("No face detected")
                    self.gender = "None"

                for faceBox in faceBoxes:
                    face = frame[max(0, faceBox[1] - self.padding):
                                 min(faceBox[3] + self.padding, frame.shape[0] - 1),
                           max(0, faceBox[0] - self.padding)
                           :min(faceBox[2] + self.padding,
                                frame.shape[1] - 1)]

                    blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
                    self.genderNet.setInput(blob)
                    genderPreds = self.genderNet.forward()
                    self.gender = self.genderList[genderPreds[0].argmax()]
                    print(f'--------------------------Gender------------------- : {self.gender}')
                    file = open("gender.txt", mode="w", errors="strict")
                    file.writelines(self.gender)
                    file.close()
                    if self.gender == "Male":
                        self.male_detected = True
                        self.female_detected = False
                        pass
                    elif self.gender == "Female":
                        self.male_detected = False
                        self.female_detected = True
                        pass

                    self.bol_gender = False
                    #print("--------- face detected", face)
                    blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
                    self.genderNet.setInput(blob)
                    genderPreds = self.genderNet.forward()
                    self.gender = self.genderList[genderPreds[0].argmax()]
                    print(f'--------------------------Gender------------------- : {self.gender}')
                    file = open("gender.txt", mode="w", errors="strict")
                    file.writelines(self.gender)
                    file.close()
                    if self.gender == "Male":
                        self.male_detected = True
                        self.female_detected = False
                        pass
                    elif self.gender == "Female":
                        self.male_detected = False
                        self.female_detected = True
                        pass
                    self.ageNet.setInput(blob)
                    agePreds = self.ageNet.forward()
                    age = self.ageList[agePreds[0].argmax()]
                    self.bol_gender = True
                    # print(f'Age: {age[1:-1]} years')
                im_pil = Image.fromarray(frame_detection)
                im_pil.save(self.faceImage, format='JPEG')

            except Exception as error:
                print("Error in face detection : ",error)
                pass
            



            cap.release()
            # time.sleep(0.3)
