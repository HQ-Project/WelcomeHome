import requests
import json

from constants import hue_username, bridge_ip, light_settings_path


class Light:
    def __init__(self):
        pass
    
    def get_light_settings(self, mood):
        with open(light_settings_path, 'r') as f:
            data = json.load(f)
            return data[mood]
    
    def open_light(self, mood):
        light_settings = self.get_light_settings(mood)
        
        try:
            requests.put("http://{}/api/{}/lights/1/state".format(bridge_ip, hue_username),
                           headers={"content-type": "application/json"},
                           json=light_settings,
                           timeout=3)
        except:
            print('Light request failed')


light = Light()