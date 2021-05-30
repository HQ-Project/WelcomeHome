import cv2
import imutils
import time
import numpy as np
import random
import json
import requests
from imutils.video.pivideostream import PiVideoStream

from constants import detection_duration, mood_server_ip


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
            res = requests.post('http://{}/detect_mood'.format(mood_server_ip),
                          json={"image": image_array.tolist()},
                          timeout=8)
            
            print(res)
            
            print('detected mood:', res.text)
            return res.text['emotion']
        except Exception as e:
            print(e)
            print('Failed mood detection')
            return int(random.random() * 7)


pi_camera = VideoCamera(flip=True)