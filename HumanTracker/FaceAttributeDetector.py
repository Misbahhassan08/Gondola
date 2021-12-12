from os import stat
from deepface import DeepFace
import time
class FaceAttributeDetector:
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface']
    def detect(self, image_path):
        start = time.time()
        # DeepFace.allocateMemory()
        obj = DeepFace.analyze(img_path = image_path, actions = ['gender'], enforce_detection=True, prog_bar=False, detector_backend = 'ssd')
        #end time
        end = time.time()
        # print time
        print("time: " + str(end - start))
        return obj
