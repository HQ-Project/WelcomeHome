#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py

from camera import VideoCamera
import time
import threading
import os
import io
import PIL.Image as Image
from time import sleep

from bluetooth_handler import bluetooth_handler
from camera import pi_camera
from mood import mood_handler
from sound_system import sound_system
from light import light


if __name__ == '__main__':
    # TODO get frames periodically and detect face, send the image to the server
    # TODO get mood, play music and open light accordingly
    
    while True:
        #if bluetooth_handler.detect_new_devices(print_devices=True):
        if pi_camera.detect_face():
            print('start mood detection...')
            
            detected_mood = pi_camera.detect_mood()
            print(detected_mood)
            
            if detected_mood is not None:
                light.open_light(mood_handler.get_mood_light(detected_mood))
                sound_system.play_music(mood_handler.get_mood_music(detected_mood))
                
                sleep(4)
                
        sleep(2)

'''
from flask import Flask, render_template, Response, request

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here
    

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frapi-me + b'\r\n\r\n')


# app.run(host='0.0.0.0', debug=False)
'''