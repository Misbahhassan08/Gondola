# print("Updating Hardware Please Wait... ")
# while True:
#	pass
import install

try:
    import cv2
    import time
    from tagsClass import HW
    from classAI import AI

    import requests
    import numpy as np
    from threading import Thread
    import json

except Exception as error:
    print('Installing libs now ..')
    install.install_dep()

import os
import getpass


class MainCode:
    def __init__(self):

        self.camera_gender = 0
        self.shelf = [1, 2, 3, 4, 5]

        self.gender_camera = False
        self.bottle_camera = False
        self.loop = True

        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        self.ID = getpass.getuser()  # machine ID should be the unique

        self.bottle = AI(self.ROOT_DIR, cam_number=self.shelf, gender_cam=self.camera_gender, threshold=0.01)

        self.arduino = HW()

        self.url = "http://35.222.60.164"

        self.screenshoot = '{}/screen.jpg'.format(self.ROOT_DIR)

        self.thread = Thread(target=self.update_to_cloud, args=())
        self.thread.start()

    def update_to_cloud(self):

        try:
            stat = self.check_bottle_cameras()
            if stat:
                print('All bottle Cameras Run Perfectly')
                self.run_tagsCalss()
                self.run_bottles_class()

        except Exception as error:
            print("ERROR : ", error)
            pass
        while True:
            print("**************************************************&&&&&&&&***********************")
            self.update_shelf_to_cloud()
            time.sleep(5)
            pass
        pass

    def update_shelf_to_cloud(self):
        #scan new configs
        try:
            _endpoint_config = "{}/api/checkconfig".format(self.url)
            payload = {'Check_Config': True}
            payload = json.dumps(payload)
            print(payload)
            print(_endpoint_config)
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", _endpoint_config, headers=headers, data=payload)
            print("------ RESPONSE ----------------------------->", response)

            # if reponse is true then check updated updations , color configs, card configs


        except Exception as error:
            pass

        # update screenshot
        try:
            _id = self.ID
            _endpoint = "{}/api/screenshoots".format(self.url)
            files = {
                'media': open(self.screenshoot, 'rb'),
                'payload': _id
            }
            r = requests.post(_endpoint, files=files)
            print(r)
        except Exception as error:
            pass

        # update logs
        try:
            bt = self.bottle.get_cameras_status()
            log = {'Data':bt, 'Hardware': self. arduino.getfails()}
            endpoint = "{}/api/stand_status".format(self.url)
            payload = {'Stand': self.ID, 'Logs': log}
            payload = json.dumps(payload)
            print(payload)
            print(endpoint)
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", endpoint, headers=headers, data=payload)
            print("------ RESPONSE ----------------------------->", response)
        except Exception as error:
            pass

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

    def run_tagsCalss(self):
        self.arduino.start()
        pass


if __name__ == '__main__':
    status = False
    mainobj = MainCode()

