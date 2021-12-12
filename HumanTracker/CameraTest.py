import cv2
def list_ports():
    dev_port = 0
    working_ports = []
    available_ports = []
    count = 0
    while count < 10:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            is_working = False
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            cv2.imshow("Camera " + str(dev_port), img)
            cv2.waitKey(0)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
        count +=1
    return available_ports,working_ports

if __name__ == '__main__':
    list_ports()