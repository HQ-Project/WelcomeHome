import cv2
import imutils
import time
import numpy as np
import random
import json
import requests
from imutils.video.pivideostream import PiVideoStream

from watson import deviceCli
from constants import detection_duration, mood_server_ip


class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        self.last_detected = []
        self.wait_response = False
        self.result = -1

        deviceCli.connect()
        deviceCli.commandCallback = self.myCommandCallback

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

    def myCommandCallback(self, cmd):
      if cmd.command == "image_response":
        response = cmd.data

        if isinstance(response["emotions"], int):
          return response["emotions"]
        
        user_weights = {}
        with open(users_path, "r") as f:
            data = json.load(f)
        
        for user in data["users"]:
            user_weights[user["name"]] = user["weight"]
        
        emotions = np.array(response["emotions"])
        names = response["names"]
        
        result = np.zeros(7)
        for i, name in enumerate(names):
            result += emotions[i] * user_weights[name]
          
        self.result = np.argmax(result)
        self.wait_response = False
    
    def detect_mood(self):
        self.send_frame(self.last_detected)

        self.wait_response = True

        while self.wait_response:
          pass
        
        return self.result

    def get_frame(self):
        return self.flip_if_needed(self.vs.read())

    def send_frame(self, image_array):
        try:
          	data = {"image": image_array.tolist()}
	          deviceCli.publishEvent(event="image", data=data, msgFormat="json")
        except Exception as e:
            print('Mood detection failed:', e)


pi_camera = VideoCamera(flip=True)