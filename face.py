import cv2

from HumanTracker.FaceDetector import FaceDetector

faceDetector = FaceDetector(min_area = 1500)

camera = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = camera.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    number_of_faces, faces = faceDetector.detect(
        frame)
    print("Number of  Faces: " + str(number_of_faces) )
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break
    
camera.release()
cv2.destroyAllWindows()