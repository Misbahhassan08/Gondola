import time
import serial
import threading
import screeninfo
import cv2
import numpy as np
import os

import io


class HW(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.TAG1 = "1117820"  # Please enter Tags here TAG1
        self.TAG2 = "247720"  # Enter Tag2
        self.bcolor = "B"
        self.gcolor = "G"
        self.wcolor = "W"

        self.match_tag_1 = [self.TAG1, self.gcolor]
        self.match_tag_2 = [self.TAG2, self.bcolor]

        self.TAG1_active = True
        self.TAG2_active = False

        self.port_fail = False
        self.screen_Fails = False

        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.video_path = '{}/data/1.mp4'.format(self.ROOT_DIR)
        self.video = cv2.VideoCapture(self.video_path)
        self.counter = 0

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

        self.window_name = 'projector'
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(self.window_name, self.screen.x - 1, self.screen.y - 1)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)

        try:
            self.ser = serial.Serial("/dev/ttyACM0", 115200)
        except Exception as error:
            self.port_fail = True
            pass

    def gettags(self):
        return [self.TAG1_active, self.TAG2_active]

    def getfails(self):
        v = ~self.screen_Fails
        return {'port': self.port_fail, 'screen': v}
        pass

    def run(self):

        while True:
            self.values = self.gettags()
            print("TAG1: {}, TAG2: {}".format(self.values[0], self.values[1]))

            et, imag = self.video.read()
            if et:
                try:
                    f = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
                    self.counter = self.counter + 1
                    if self.counter >= f:
                        self.video.set(cv2.CAP_PROP_POS_FRAMES, 1)
                        self.counter = 1
                        pass
                    cv2.imshow(self.window_name, imag)
                    cv2.waitKey(35)
                except Exception as error:
                    print("error : ", error)
                    pass
                pass
            if not self.port_fail:
                if self.ser.in_waiting > 0:
                    rx_data = self.ser.readline().decode("utf-8").strip()
                    if len(rx_data) > 0:

                        if rx_data == self.match_tag_1[0]:
                            print("tag1 received")

                            cmd = '%s' % self.match_tag_1[1]
                            cmd = cmd.encode('utf-8')

                            self.ser.write(cmd)
                            self.TAG1_active = True
                            self.TAG2_active = False

                        elif rx_data == self.match_tag_2[0]:
                            print("tag2 received")
                            cmd = '%s' % self.match_tag_2[1]
                            cmd = cmd.encode('utf-8')

                            self.ser.write(cmd)
                            self.TAG1_active = False
                            self.TAG2_active = True
                        pass

    pass


if __name__ == '__main__':
    arduino = HW()
    arduino.start()
