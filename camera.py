import cv2
import imutils
import time
import numpy as np
import random
import requests
from imutils.video.pivideostream import PiVideoStream

from constants import detection_duration


class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame
    
    def detect_face(self):
        img = self.get_frame()
        
        # Load the cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        return len(faces) > 0
    
    def detect_mood(self):
        begin_time = time.time()
        
        while True:
            mood = self.send_frame(self.get_frame())
            
            if mood is not None:
                return mood
            
            if time.time() - begin_time > detection_duration:
                return None

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        return frame
        
        '''
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg
        '''
    
    def send_frame(self, image_array):
        try:
            # TODO send request
            res = requests.post('http://{}', format(),
                          json={"data": image_array},
                          timeout=3)
            
            print('detected mood:', res.text)
            return res.text
        except:
            print('Failed mood detection')
            pass
        
        return int(random.random() * 7)


pi_camera = VideoCamera(flip=True)