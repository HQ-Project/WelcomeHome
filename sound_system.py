import random
import os

from constants import sounds_path


class SoundSystem:
    def __init__(self):
        pass
    
    def play_music(self, mood):
        sounds = os.listdir(sounds_path + '/' + mood)
        print('sounds', sounds)
        sound = sounds[int(random.random() * len(sounds))]
        print('sound', sound)
        path = sounds_path + '/' + mood + '/' + sound
        print('path', path)
        
        os.system('mocp -l {}'.format(path))


sound_system = SoundSystem()