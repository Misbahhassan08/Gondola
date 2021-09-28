import cv2
import jetson.inference
import jetson.utils
import time
import RPi.GPIO as GPIO
from classGender import Gender
from classBottles import Bottles
import requests
import screeninfo
import numpy as np


class MainCode:
    def __init__(self):
        self.input_pin1 = 21
        self.input_pin2 = 20

        self.camera_gender = 0
        self.shelf = [1, 2, 3, 4, 5]

        self.gender_camera = False
        self.bottle_camera = False
        self.loop = True

        GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
        GPIO.setup(self.input_pin1, GPIO.IN)
        GPIO.setup(self.input_pin2, GPIO.IN)

        self.bottle = Bottles(cam_number=self.shelf, gender_cam=self.camera_gender, threshold = 0.01)

        self.url = "http://inovat-ioi.com/app_api/index.php/Admin/updateStockByShelf"

    def update_shelf_to_cloud(self):
        for shelf_id in range(len(self.shelf)):
            x = shelf_id + 1
            bt = self.bottle.get_cameras_status()
            # print(bt)
            payload = "{\r\n        \"shelf_id\":%d,\r\n        \"current_stock\": \"%s\"\r\n}" % (
                x, str(bt[shelf_id]["total_bottles"]))
            headers = {'Content-Type': 'text/plain'}
            response = requests.request("POST", self.url, headers=headers, data=payload)

            # print(response)
            # print(payload)
            # print('***************************************')
            # print('\n')

    def check_bottle_cameras(self):
        self.bottle.test_cameras_bottle()
        camera_status_bottles = self.bottle.get_cameras_status()
        print(camera_status_bottles)
        if camera_status_bottles[len(self.shelf) - 1]["Status"]:
            return True
            pass

    def run_bottles_class(self):
        self.bottle.start()
        pass

    def scan_gpios(self):
        value1 = GPIO.input(self.input_pin1)
        value2 = GPIO.input(self.input_pin2)
        return [value1, value2]

    def scan_gender_status(self):
        md = self.bottle.male_detected
        fd = self.bottle.female_detected
        return [md, fd]
        pass


if __name__ == '__main__':

    screen_id = 0
    is_color = True

    # get the size of the screen
    screen = screeninfo.get_monitors()[screen_id]
    width, height = screen.width, screen.height

    # create image
    if is_color:
        image = np.ones((height, width, 3), dtype=np.float32)
        image[:10, :10] = 0  # black at top-left corner
        image[height - 10:, :10] = [1, 0, 0]  # blue at bottom-left
        image[:10, width - 10:] = [0, 1, 0]  # green at top-right
        image[height - 10:, width - 10:] = [0, 0, 1]  # red at bottom-right
    else:
        image = np.ones((height, width), dtype=np.float32)
        image[0, 0] = 0  # top-left corner
        image[height - 2, 0] = 0  # bottom-left
        image[0, width - 2] = 0  # top-right
        image[height - 2, width - 2] = 0  # bottom-right

    window_name = 'projector'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)

    manImage1 = "/home/misbah/dev/V3/b1m.jpg"
    womanImage1 = "/home/misbah/dev/V3/b1f.jpg"

    manImage2 = "/home/misbah/dev/V3/b2m.jpg"
    womanImage2 = "/home/misbah/dev/V3/b2f.jpg"

    image = cv2.imread(manImage1)
    mainobj = MainCode()

    # check status of all cameras
    status = mainobj.check_bottle_cameras()
    if status:
        print('All bottle Cameras Run Perfectly')
        mainobj.run_bottles_class()

    values = [0, 0]
    mf = [False, False]
    while status:
        values = mainobj.scan_gpios()
        mf = mainobj.scan_gender_status()

        print(mf)
        if mf[0] == True:
            if values[0] == 1 and values[1] == 0:
                image = cv2.imread(manImage1)
            elif values[0] == 0 and values[1] == 1:
                image = cv2.imread(manImage2)
                # image = cv2.resize(image,(width,height))
            pass
        elif mf[1] == True:
            if values[0] == 1 and values[1] == 0:
                image = cv2.imread(womanImage1)
                # image = cv2.resize(image,(width,height))
            elif values[0] == 0 and values[1] == 1:
                image = cv2.imread(womanImage2)
                # image = cv2.resize(image,(width,height))
            pass
        else:
            image = cv2.imread(manImage1)
        cv2.imshow(window_name, image)
        cv2.waitKey(1)
        mainobj.update_shelf_to_cloud()
        #time.sleep(1)
        pass
