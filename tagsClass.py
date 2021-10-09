import time
import serial
import threading
import io


class HW(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.TAG1 = ""
        self.TAG2 = ""
        self.bcolor = "blue"
        self.gcolor = "green"
        self.wcolor = "white"

        self.match_tag_1 = [self.TAG1, self.bcolor]
        self.match_tag_2 = [self.TAG2, self.gcolor]
        self.ser = serial.Serial("/dev/ttyACM0", baudrate=115200)
        self.TAG1_active = False
        self.TAG2_active = False

    def gettags(self):
        return [self.TAG1_active, self.TAG2_active]

    def run(self):
        while True:
            rx_data = self.ser.readline()
            if len(rx_data) > 0:
                if rx_data == self.match_tag_1[0]:
                    time.sleep(0.1)
                    self.ser.write(b'%s' % self.match_tag_1[1])
                    self.TAG1_active = True
                    self.TAG2_active = False

                elif rx_data == self.match_tag_2[0]:
                    time.sleep(0.1)
                    self.ser.write(b'%s' % self.match_tag_2[1])
                    self.TAG1_active = False
                    self.TAG2_active = True
                pass

    pass
