from os import stat
import cvlib as cv
import time
import cv2
import numpy as np
from HumanTracker.common.Box import Box
from HumanTracker.FaceDetector import FaceDetector

class Face:
    def __init__(self, frame, f, padding) -> None:
        self.start_x = max(0, f[0]-padding)
        self.start_y = max(0, f[1]-padding)
        self.end_x = min(frame.shape[1]-1, f[2]+padding)
        self.end_y = min(frame.shape[0]-1, f[3]+padding)
        self.width = self.end_x - self.start_x
        self.height = self.end_y - self.start_y

    @property
    def start(self):
        return (self.start_x, self.start_y)

    @property
    def end(self):
        return (self.end_x, self.end_y)

    @property
    def area(self):
        return self.width * self.height

    def add_offset(self, x, y):
        self.start_x += x
        self.start_y += y
        self.end_x += x
        self.end_y += y


class GenderDetector:
    def __init__(self, min_area=10000):
        self.padding = 0
        self.min_area = min_area
        self.start_time=0

    def detectFace(self, frame):
        self.start_time = time.time()
        response = cv.detect_face(frame)
        if response:
            faces, confidence = cv.detect_face(frame,enable_gpu=True)
            max_area = 0
            max_face = None
            max_face_confidence = 0
            if faces is not None:
                for idx, f in enumerate(faces):
                    face = Box(frame, f, self.padding)
                    if face.area > max_area:
                        max_area = face.area
                        max_face = face
                        max_face_confidence = confidence[idx]
            if max_face is not None:
                return max_face, max_face_confidence
        return None, 0

    def detectGender(self, frame, face: Box):
        start = time.time()
        cv2.rectangle(frame, face.start, face.end, (0, 255, 0), 2)
        face_crop = np.copy(
            frame[face.start_y:face.end_y, face.start_x:face.end_x])
        (label, confidence) = cv.detect_gender(face_crop, enable_gpu=True)
        idx = np.argmax(confidence)
        gender = label[idx]
        if(confidence[idx] < 0.90):
            gender= "unknown"
        
        
        # end time
        end = time.time()

        # print time
        print("gender: {}, confidence: {:2f}, time: {:3f}".format(
            gender, confidence[idx], end - start))
        return gender, confidence[idx]

    def draw(self, frame, face: Face, gender, confidence, start_x=0, start_y=0):
        if start_x !=0 or start_y !=0:
            face.add_offset(start_x, start_y)
        if gender is not None:
            imagelabel = "{}: {:.2f}%".format(gender, confidence * 100)
            Y = face.start_y - 20 if face.start_y - 10 > 10 else face.start_y + 20
            cv2.putText(frame, imagelabel, (face.start_x, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 255, 0), 2)
        if(face.area > self.min_area * 2.5):
            cv2.rectangle(frame, face.start, face.end, (0, 255, 0), 2)
        elif (face.area > self.min_area):
            cv2.rectangle(frame, face.start, face.end,(255, 0, 0),2)
        else:
            cv2.rectangle(frame, face.start, face.end,(0, 0, 255),2)

if __name__ == '__main__':
    webcam = cv2.VideoCapture(0)
    # webcam = cv2.VideoCapture('input/mask_male.mp4')
    padding = 20
    detector = GenderDetector()
    faceDetector = FaceDetector()
    while webcam.isOpened():
        status, frame = webcam.read()
        # face, confidence = detector.detectFace(frame)
        num_faces, faces = faceDetector.detect(frame)
        if num_faces > 0:
            face = faceDetector.getMaxBox(frame, faces)
            if face is not None:
                try:
                    gender, confidence = detector.detectGender(frame, face)
                    detector.draw(frame, face, gender, confidence)
                    cv2.imshow("Gender", frame)
                except Exception as e:
                    print(face)

        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            break
