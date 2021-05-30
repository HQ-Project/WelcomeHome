import time
import os
import PIL.Image as Image
from camera import VideoCamera
from time import sleep

from camera import pi_camera
from sound_system import sound_system
from light import light
from constants import cooldown, moods


# TODO start mood_detection and web_server module when pi starts
# TODO mocp need to be started as well (just type mocp on terminal)


def run_mood_detection():
    print('Looking for faces...')

    while True:
        if pi_camera.detect_face():
            print('Start mood detection...')
            
            detected_mood = pi_camera.detect_mood()
            print(detected_mood)
            
            if detected_mood != -1:
                print('Detected mood: ', moods[detected_mood])
                light.open_light(moods[detected_mood])
                sound_system.play_music(moods[detected_mood])
                
                sleep(cooldown)
        else:
            sleep(0.5)


if __name__ == '__main__':
    run_mood_detection()