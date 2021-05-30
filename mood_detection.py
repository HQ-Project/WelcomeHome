import time
import os
import numpy as np
import PIL.Image as Image
from camera import VideoCamera
from time import sleep
import ibmiotf.application
import ibmiotf.device

from camera import pi_camera
from sound_system import sound_system
from light import light
from constants import cooldown, moods


def run_mood_detection(deviceCli):
    print('Looking for faces...')
    
    while True:
        if pi_camera.detect_face():
            print('Start mood detection...')
            
            detected_mood = pi_camera.detect_mood(deviceCli)
            print(detected_mood)
            
            if detected_mood != -1:
                print('Detected mood: ', moods[detected_mood])
                light.open_light(moods[detected_mood])
                sound_system.play_music(moods[detected_mood])
                
                sleep(cooldown)
        else:
            sleep(0.5)


def myCommandCallback(cmd):
    print('hhhhh')
    if cmd.command == "image_response":
        print('Command callback')
        
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
          
        pi_camera.result = np.argmax(result)
        pi_camera.wait_response = False


if __name__ == '__main__':
    organization = "7lke3y"
    deviceType = "raspi"
    deviceId = "dca632b2337e"
    authMethod = "token"
    authToken = "z0&s36wdlAL-+A*tUd"

    # Initialize the device client.
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
    deviceCli = ibmiotf.device.Client(deviceOptions)
    
    deviceCli.connect()
    deviceCli.commandCallback = myCommandCallback
    
    run_mood_detection(deviceCli)