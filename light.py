import requests

from constants import hue_username, bridge_ip


class Light:
    def __init__(self):
        pass
    
    
    def open_light(self, mode):
        # TODO connect hue light and open light
        
        res = requests.put("http://{}/api/{}/lights/1/state".format(bridge_ip, hue_username),
                           headers={"content-type": "application/json"},
                           json=mode)
        
        # print(res.text)


light = Light()