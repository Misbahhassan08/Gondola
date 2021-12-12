import numpy as np
import cv2
import screeninfo
import os
import threading



class mediaplayer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        video_path = '{}/data/1.mp4'.format(ROOT_DIR)
        self.screen_id = 0
        self.fps = 31

        # get the size of the screen
        try:
            self.screen_id = 0
            self.screen = screeninfo.get_monitors()[self.screen_id]
            self.width, self.height = self.screen.width, self.screen.height
            pass
        except Exception as error:
            while True:
                print("********************************** CONNECTING SCREEEN ****************************************")
                self.screen_Fails = True
                self.screen_id = 0
                try:

                    self.screen = screeninfo.get_monitors()[self.screen_id]
                    self.width, self.height = self.screen.width, self.screen.height
                    if (self.width > 0) or (self.height > 0):
                        self.screen_Fails = False
                        break
                except:
                    pass

                pass
            pass

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.video_path = '{}/data/1.mp4'.format(ROOT_DIR)
        self.video = cv2.VideoCapture(video_path)
        self.window_name = 'projector'
        self.counter = 0

    def run(self):
        while True:
            et, imag = self.video.read()
            if et:
                try:
                    f = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
                    # print(f)
                    cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
                    cv2.moveWindow(self.window_name, self.screen.x - 1, self.screen.y - 1)
                    cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN,
                                          cv2.WINDOW_FULLSCREEN)

                    self.counter = self.counter + 1
                    if self.counter >= f:
                        self.video.set(cv2.CAP_PROP_POS_FRAMES, 1)
                        self.counter = 1
                        pass
                    cv2.imshow(self.window_name, imag)
                    cv2.waitKey(self.fps)
                except Exception as error:
                    print("error : ", error)
                    pass
                pass
        pass

    pass


if __name__ == '__main__':
    mp = mediaplayer()
    mp.start()
    pass
