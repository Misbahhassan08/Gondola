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

        # get the size of the screen
        try:
            self.screen_id = 0
            self.screen = screeninfo.get_monitors()[self.screen_id]
            self.width, self.height = self.screen.width, self.screen.height
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

        self.manImage1 = '{}/gender_files/Input_images/b1m.jpg'.format(self.ROOT_DIR)
        self.womanImage1 = '{}/gender_files/Input_images/b1f.jpg'.format(self.ROOT_DIR)

        self.manImage2 = '{}/gender_files/Input_images/b2m.jpg'.format(self.ROOT_DIR)
        self.womanImage2 = '{}/gender_files/Input_images/b2f.jpg'.format(self.ROOT_DIR)

        self.image = cv2.imread(self.manImage1)
        for i in range(10):
            cv2.imshow(self.window_name, self.image)
            cv2.waitKey(1)

        self.mf = [True, False]
        self.values = [True, False]

        try:
            self.ser = serial.Serial("/dev/ttyACM0", 115200)
        except Exception as error:
            self.port_fail = True
            pass

    def gettags(self):
        return [self.TAG1_active, self.TAG2_active]

    def getfails(self):
        return {'port': self.port_fail, 'screen': self.screen_Fails}
        pass

    def run(self):

        while True:
            file = open("gender.txt", mode="r", errors="strict")
            gender = file.readline()
            file.close()
            if gender == 'Male':
                self.mf = [True, False]
                pass
            elif gender == 'Female':
                self.mf = [False, True]
                pass
            self.values = self.gettags()
            print("TAG1: {}, TAG2: {}".format(self.values[0], self.values[1]))
            if self.mf[0]:
                if self.values[0]:
                    self.image = cv2.imread(self.manImage1)
                elif self.values[1]:
                    self.image = cv2.imread(self.manImage2)
                    # image = cv2.resize(image,(width,height))

            if self.mf[1]:
                if self.values[0]:
                    self.image = cv2.imread(self.womanImage1)
                    # image = cv2.resize(image,(width,height))
                elif self.values[1]:
                    self.image = cv2.imread(self.womanImage2)
                    # image = cv2.resize(image,(width,height))
                else:
                    self.image = cv2.imread(self.womanImage1)

            for i in range(10):
                cv2.imshow(self.window_name, self.image)
                cv2.waitKey(1)
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
