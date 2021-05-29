import random
import os

from constants import sounds_path


class SoundSystem:
    def __init__(self):
        pass
    
    def play_music(self, mood):
        sounds = os.listdir(sounds_path + '/' + mood)
        sound = sounds[int(random.random() * len(sounds))]
        path = sounds_path + '/' + mood + '/' + sound
        
        os.system('mocp -l {}'.format(path))


sound_system = SoundSystem()