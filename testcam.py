import cv2
#import imagezmq
import time
import imutils

print('start')
#rtsp://192.168.1.116:8554/h264?ch=1'
vsc = cv2.VideoCapture('rtsp://admin:@192.168.1.103/Streaming/Channels/600') # face
#vsc = cv2.VideoCapture('rtsp://admin:@192.168.1.43/Streaming/h1080?ch=1')#top  
#vsc = cv2.VideoCapture('rtsp://192.168.1.111:8554/Streaming/Channels/810')#shelf

while True:
    try:
        ret,img = vsc.read()
        scale_percent = 20 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        #frame = imutils.resize(frame, 650)
        #text1 = sender.send_image(image_window_name, frame)
        cv2.imshow("Video",frame)
        cv2.waitKey(10)
    except Exception as error:
        print(error)
        break
