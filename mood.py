import random

class Mood:
    def __init__(self):
        # TODO get them from website/application
        self.mood_lights = {
            'happy': {"bri":254, "ct":153},
            'sad': {"bri":110, "ct":153},
            'neutral': {"bri":110, "ct":300},
            'angry': {"bri":254, "ct":500}
        }
        
        # TODO get them from website/application
        self.mood_musics = {
            'happy': ['happy_music_link1', 'happy_music_link2', 'happy_music_link3'],
            'sad': ['sad_music_link_1'],
            'neutral': ['neutral_music_link_1'],
            'angry': ['angry_music_link_1']
        }
    
    def get_mood_light(self, mood):
        return self.mood_lights[mood]
    
    def get_mood_music(self, mood):
        musics = self.mood_musics[mood]
        index = int(random.random() * len(musics))
        
        return musics[index]
    
    def set_mood_lights(self, lights):
        self.mood_lights = lights
    
    def set_mood_musics(self, musics):
        self.mood_musics = musics

mood_handler = Mood()