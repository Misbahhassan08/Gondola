import numpy as np
import cv2
import time
import io
from PIL import Image

while (True):
    # Capture frame-by-frame
    for x in range(5):
        cap = cv2.VideoCapture(x)
        time.sleep(1)
        ret, frame = cap.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)

        im_pil.save('bufferimage.jpg', format='JPEG')

        cap.release()
        time.sleep(2)

        cv2.imread('bufferimage.jpg')


