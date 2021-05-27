import random

class Mood:
    def __init__(self):
        # TODO get them from website/application
        self.mood_lights = {
            'happy': 'happy_light',
            'sad': 'sad_light',
            'neutral': 'neutral_light',
            'angry': 'angry_light'
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