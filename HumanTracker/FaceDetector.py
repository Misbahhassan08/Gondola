from HumanTracker.common.Box import Box
from HumanTracker.common.ImageHelper import ImageHelper
import mediapipe as mp
import cv2
import time

class FaceDetector:
    model = None
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    mp.solutions
    def __init__(self, min_area=10000) -> None:
        self.model = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)
        self.min_area = min_area

    def detect(self, image):
        if(self.model is None):
            print("------- FaceDetector Model is not loaded -------")
            return None
        # COLOR CONVERSION BGR 2 RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        start = time.time()
        results = self.model.process(image)
        if not results or not results.detections:
            return 0, None
        # print("mp: {:.2f}".format(time.time() - start))
        return len(results.detections), results

    def getMaxBox(self, image, results):
        if not results:
            print("No faces to process")
            return None
        max_box = None
        max_area = 0
        for detection in results.detections:
            bBox = detection.location_data.relative_bounding_box
            box = Box(image, bBox)
            if(box.area > max_area):
                max_area = box.area
                max_box = box
        return max_box

    def draw(self, image, nb_faces, results):
        if not results.detections:
            print("No faces detected")
            return None
        for detection in results.detections:
            # print('Nose tip:')
            # print(self.mp_face_detection.get_key_point(detection, self.mp_face_detection.FaceKeyPoint.NOSE_TIP))
            # self.mp_drawing.draw_detection(image, detection)

            bBox = detection.location_data.relative_bounding_box
            box = Box(image, bBox)
            if(box.area > self.min_area * 2.5):
                cv2.rectangle(image, box.start, box.end,(0, 255, 0),2)
            elif (box.area > self.min_area):
                cv2.rectangle(image, box.start, box.end,(255, 0, 0),2)
            else:
                 cv2.rectangle(image, box.start, box.end,(0, 0, 255),2)
                # cv2.putText(image, str(int(avg)), (box.start_x, box.start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)