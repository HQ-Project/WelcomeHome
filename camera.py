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
        self.last_detected = []
        self.wait_response = False
        self.result = -1

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
        
        if len(faces) > 0:
            self.last_detected = img
            return True
        
        return False
    
    def detect_mood(self, deviceCli):
        self.send_frame(self.last_detected, deviceCli)

        self.wait_response = True

        print("begin while")
        #while self.wait_response:
        time.sleep(3)
        print("end while")
        
        return self.result

    def get_frame(self):
        return self.flip_if_needed(self.vs.read())

    def send_frame(self, image_array, deviceCli):
        try:
            image_array = cv2.resize(image_array, (80, 60), interpolation=cv2.INTER_AREA)
            data = {"image": image_array.tolist()}
            deviceCli.publishEvent(event="image", data=data, msgFormat="json")
            print('Sent image')
        except Exception as e:
            print('Mood detection failed:', e)


pi_camera = VideoCamera(flip=True)