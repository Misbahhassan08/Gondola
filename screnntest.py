import numpy as np
import cv2
import screeninfo
import os

screen_id = 0
is_color = False

# get the size of the screen
screen = screeninfo.get_monitors()[screen_id]
width, height = screen.width, screen.height
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
video_path = '{}/data/1.mp4'.format(ROOT_DIR)
vide0 = cv2.VideoCapture(video_path)
frame = []
_frame = 0
while True:
    print(_frame)
    et, image = vide0.read()
    if et:
        frame.append(image)
        _frame = _frame + 1
    if _frame >= 1154:
        break
    pass
vide0.release()
if __name__ == '__main__':
    window_name = 'projector'
    i = 0
    while True:
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)
        if i == 1154:
            i = 0
        else:
            print(i)
            try:
                cv2.imshow(window_name, frame[i])
                cv2.waitKey(40)
                i = i + 1
            except:
                pass
