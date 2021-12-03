import cv2
import time
import threading
from PIL import Image
import face_recognition

cap = cv2.VideoCapture(5)
while True:
    # time.sleep(0.1
    ret, frame = cap.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)#frame[:, :, ::-1]
   
    # Load a sample picture and learn how to recognize it.
    try:
        temp_image = face_recognition.load_image_file("11.jpg")
        temp_image_encoding = face_recognition.face_encodings(temp_image)[0]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        results = face_recognition.compare_faces(temp_image_encoding, face_encodings)
        if len(results):
            print(results)
            if results[0]:
                print("same image")
                pass
            else:
                im_pil = Image.fromarray(rgb_frame)
                im_pil.save("11.jpg", format='JPEG')
        pass
    except Exception as error:
        print("saving new image",error)
        im_pil = Image.fromarray(rgb_frame)
        im_pil.save("11.jpg", format='JPEG')
        pass

    
    
    pass # main loop