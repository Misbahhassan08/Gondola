
import cv2

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import tensorflow as tf
import tensorflow.keras

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# session = tf.Session(config=config)
# tensorflow.keras.backend.set_session(session)


from HumanTracker.FaceAttributeDetector import FaceAttributeDetector
from HumanTracker.common.ImageHelper import ImageHelper;

detector = FaceAttributeDetector()

camera = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = camera.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame = ImageHelper.resize(frame, height=256)
    try:
        result = detector.detect(
            frame)
        print(result)
    except Exception as e:
        print(e)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break
    
camera.release()
cv2.destroyAllWindows()