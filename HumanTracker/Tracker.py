import os
import time
import cv2
import argparse
from HumanTracker.human_tracker_onnx import HumanTrackerONNX
from HumanTracker.GenderDetector import GenderDetector
from HumanTracker.FaceDetector import FaceDetector

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

class Tracker:
    def __init__(self, min_face_area= 1500, min_box_area=100000, match_thresh=0.6, track_thresh = 0.4, execution_provider = "CUDAExecutionProvider", model_path="HumanTracker/model/humantracker_nano2.onnx"):

        self.match_thresh = match_thresh
        self.min_box_area = min_box_area
        self.track_thresh = track_thresh
        self.model_path = model_path
        self.args = self.get_args()
        self.cap_device = self.args.device
        self.cap_width = self.args.width
        self.cap_height = self.args.height
        print('Loading HumanTrackerONNX ...')
        self.tracker = HumanTrackerONNX(self.args, execution_provider)
        print('Loaded HumanTrackerONNX')
        self.frame_id = 0
        self.total = 0
        self.male = 0
        self.female = 0
        self.unknown = 0
        self.min_face_area = min_face_area
        self.active_trackers = {}
        # self.detector = FaceAttributeDetector()
        # print('Loaded FaceAttributeDetector')
        self.faceDetector = FaceDetector(min_area = self.min_face_area)
        print('Loaded FaceDetector')
        self.detector = GenderDetector(min_area = self.min_face_area)
        print('Loaded GenderDetector')
        self.min_face_area = min_face_area

    def process(self, frame, faceAttributes=False):
        start_time = time.time()
        self.frame_id += 1
        missed = 0
        # frame = ImageHelper.resize(frame, self.cap_width, self.cap_height)

        _, bboxes, ids, scores = self.tracker.inference(frame)

        # check face
        # print("Detecting Faces...")
        # number_of_faces, faces = self.faceDetector.detect(frame)
        # print("Number of  Faces: " + str(number_of_faces) )

        if ids:
            trackers = list(self.active_trackers.keys())
            for track_id in trackers:
                if track_id not in ids:
                    start_time = self.active_trackers[track_id].get(
                        "start_time")
                    gender = self.active_trackers[track_id].get("gender")
                    area = self.active_trackers[track_id].get("area")
                    print("{} is lost. Duration: {:2f}, Area {}".format(
                        track_id, time.time() - start_time, area))
                    del self.active_trackers[track_id]
                    missed += 1
                    if gender is not None:
                        if gender == "male":
                            self.male += 1
                        elif gender == "female":
                            self.female += 1
                        elif gender == "unknown":
                            self.unknown += 1
                    else:
                        if area > self.min_face_area:
                            self.unknown += 1
                    self.total = self.male + self.female + self.unknown
            trackers = list(self.active_trackers.keys())
            for idx, id in enumerate(ids):
                if id not in trackers:
                    # print(b)
                    self.active_trackers[id] = {
                        "frame": 0,
                        "sample": 0,
                        "area": 0,
                        "start_time": time.time()
                    }

                # increase frame count
                b = [int(arr) for arr in bboxes[idx]]
                tracked_image = frame[b[1]:b[1] + b[3], b[0]:b[0]+b[2]]
                if tracked_image.shape[0] != 0 and tracked_image.shape[1] != 0:
                    # check face

                    number_of_faces, faces = self.faceDetector.detect(
                        tracked_image)
                    # print("Number of  Faces: " + str(number_of_faces) )
                    # face, confidence = self.detector.detectFace(tracked_image)
                    
                    if number_of_faces > 0:
                        self.active_trackers[id]["frame"] += 1
                        face = self.faceDetector.getMaxBox(tracked_image, faces)
                        self.faceDetector.draw(tracked_image, number_of_faces, faces)
                        gender = None
                        gender_confidence = 0
                        if face.area > self.min_face_area:
                            previous_area = self.active_trackers[id]['area'] 
                            self.active_trackers[id]['area'] = (previous_area + face.area) / 2
                            # print("p: {}. average area: {}, frame {}, current {}".format(previous_area, self.active_trackers[id]['area'], self.active_trackers[id]['frame'], maxBox.area))
                            if self.active_trackers[id].get("sample") == 0:
                                try:
                                    # result = self.detector.detect(tracked_image)
                                    # region = result["region"]
                                    # x = region['x'] + b[0]
                                    # y = region['y'] + b[1]
                                    # w = x + region['w']
                                    # h = y + region['h']
                                    # cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
                                    # cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 1)
                                    #print(result)

                                    # self.active_trackers[id]['age'] = result['age']
                                    # self.active_trackers[id]['gender'] = result['gender']

                                    gender, gender_confidence = self.detector.detectGender(tracked_image, face)
                                    if gender is not None:
                                        self.active_trackers[id]['gender'] = gender
                                        # increase sample count
                                        self.active_trackers[id]["sample"] += 1
                                        cv2.imshow("tracked_image", tracked_image)
                                except Exception as e:
                                    print("Gender detect Failed: " + str(e))
                                    pass
                        # self.detector.draw(frame, face= face,  gender=gender, confidence=gender_confidence,start_x=b[0],start_y= b[1]) 

        elapsed_time = time.time() - start_time
        if(bboxes is not None):
            frame = self.draw_tracking_info(
                frame,
                bboxes,
                ids,
                scores,
                self.frame_id,
                elapsed_time,
                self.total
            )
        return missed

    def get_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            '--model',
            type=str,
            default= self.model_path ,
        )
        parser.add_argument('--device', type=int, default=0)
        parser.add_argument("--width", help='cap width', type=int, default=960)
        parser.add_argument("--height", help='cap height',
                            type=int, default=540)
        parser.add_argument(
            '--score_th',
            type=float,
            default=0.3,
        )
        parser.add_argument(
            '--nms_th',
            type=float,
            default=0.2,
        )
        parser.add_argument(
            '--input_shape',
            type=str,
            # default='608,1088',
            # default='320,512',
            default='192,320',
        )
        parser.add_argument(
            '--with_p6',
            action='store_true',
            help='Whether your model uses p6 in FPN/PAN.',
        )

        # tracking args
        parser.add_argument(
            '--track_thresh',
            type=float,
            default=self.track_thresh,
            help='tracking confidence threshold',
        )
        parser.add_argument(
            '--track_buffer',
            type=int,
            default=15,
            help='the frames for keep lost tracks',
        )
        parser.add_argument(
            '--match_thresh',
            type=float,
            default = self.match_thresh,
            help='matching threshold for tracking',
        )
        parser.add_argument(
            '--min_box_area',
            type=float,
            default=self.min_box_area,
            help='filter out tiny boxes',
        )
        parser.add_argument(
            '--mot20',
            dest='mot20',
            default=False,
            action='store_true',
            help='test mot20.',
        )

        args = parser.parse_args()

        return args

    def draw_tracking_info(
        self,
        image,
        tlwhs,
        ids,
        scores,
        frame_id=0,
        elapsed_time=0.0,
        total=0,
    ):
        text_scale = 1.5
        text_thickness = 2
        line_thickness = 2

        # text = 'active: %d ' % (len(tlwhs))
        text = 't: %.0fms ' % (elapsed_time * 1000)
        text += 'f: %d' % (frame_id)
        cv2.putText(
            image,
            text,
            (0, int(15 * text_scale)),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (0, 255, 0),
            thickness=1,
        )

        for index, tlwh in enumerate(tlwhs):
            x1, y1 = int(tlwh[0]), int(tlwh[1])
            x2, y2 = x1 + int(tlwh[2]), y1 + int(tlwh[3])

            color = self.get_id_color(ids[index])
            cv2.rectangle(image, (x1, y1), (x2, y2), color, line_thickness)

            text = str(ids[index])
            cv2.putText(image, text, (x1, y1 - 5), cv2.FONT_HERSHEY_PLAIN,
                        text_scale, (0, 0, 0), text_thickness + 3)
            cv2.putText(image, text, (x1, y1 - 5), cv2.FONT_HERSHEY_PLAIN,
                        text_scale, (255, 255, 255), text_thickness)
        return image

    def get_id_color(self, index):
        temp_index = abs(int(index)) * 3
        color = ((37 * temp_index) % 255, (17 * temp_index) % 255,
                 (29 * temp_index) % 255)
        return color
