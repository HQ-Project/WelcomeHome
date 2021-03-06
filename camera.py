import cv2
import imutils
import time
import numpy as np
import random
import json
import requests
from imutils.video.pivideostream import PiVideoStream

from constants import detection_duration, mood_server_ip, users_path


class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        self.last_detected = []
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
    
    def detect_mood(self):
        response = self.send_frame(self.last_detected)
        
        if isinstance(response, int):
            return response

        print(response)
        print(type(response["found"]))
        print(response["found"])
        if response["found"] == False:
            return int(random.random() * 7)

        user_weights = {}
        with open(users_path, "r") as f:
            data = json.load(f)

        for user in data["users"]:
            user_weights[user["name"]] = user["weight"]
        
        # print(user_weights)
        # print(data["users"])
        # print(user_weights["Talha"])

        emotions = np.asarray(response["emotions"], dtype=np.float64)
        # print(emotions)
        names = response["names"]
        # print(response["names"])

        result = np.zeros(7)
        for i, name in enumerate(names):
            # print('>>>>> ', emotions[i], user_weights[name])
            for j in range(emotions.shape[1]):
                prob = float(emotions[i,j])
                result[j] += prob * int(user_weights[name])
        
        # print('resullttttt >>>>><<<<<##### ', result)

        return np.argmax(result)

    def get_frame(self):
        return self.flip_if_needed(self.vs.read())

    def send_frame(self, image_array):
        try:
            res = requests.post('http://{}/detect/{}'.format(mood_server_ip, 2),
                          json={"image": image_array.tolist()},
                          timeout=8).json()
            
            return res
        except Exception as e:
            print('Mood detection failed:', e)
            return int(random.random() * 7)


pi_camera = VideoCamera(flip=True)