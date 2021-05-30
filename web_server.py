import json
import pafy
import os
import requests
import time
from flask import Flask, render_template, Response, request, redirect, url_for

from constants import server_port, light_settings_path, sounds_path, moods, light_settings_path, mood_server_ip


# TODO delete end points ??
app = Flask(__name__)


def get_sounds():
    ret = {}
    
    for k,v in moods.items():
        sounds = os.listdir(sounds_path + '/' + v)
        ret[v] = sounds
    
    return ret


def get_light_settings():
    with open(light_settings_path, 'r') as f:
        data = json.load(f)
        return data


@app.route('/')
def index():
    return render_template('index.html', feedback="", sounds=get_sounds(), lights=get_light_settings())


@app.route('/add-custom-light', methods=['post'])
def add_light():
    data = {}
    with open(light_settings_path, "r") as f:
        data = json.load(f)
    data[request.form['light-mood']] = {"bri": int(request.form["brightness"]), "ct": int(request.form["color-temperature"])}
    
    with open(light_settings_path, "w") as f:
        json.dump(data, f)
    
    return render_template('index.html', feedback="Successful", sounds=get_sounds(), lights=get_light_settings())


@app.route('/add-custom-sound', methods=['post'])
def add_sound():
    result = pafy.new(request.form['youtube-link'])
    
    min_index = 0
    for i, stream in enumerate(result.audiostreams):
        if stream.get_filesize() < result.audiostreams[min_index].get_filesize():
            min_index = i
    
    path = sounds_path + '/' + request.form['sound-mood'] + '/' + request.form['sound-name'] + '.m4a'
    
    while True:
        try:
            result.audiostreams[i].download(path)
            break
        except:
            pass
    
    return render_template('index.html', feedback="Successful", sounds=get_sounds(), lights=get_light_settings())


@app.route('/stop-music', methods=['get'])
def stop_music():
    os.system('mocp -s')
    return '', 200


@app.route('/image-upload/<username>', methods=['post'])
def image_upload(username):
    file = request.files["file"]
    files = {'imageFile': file.read()}
    
    try:
        res = requests.post('http://{}/register/{}/{}'.format(mood_server_ip, 2, username),
            files=files).json()
        
        print('Image sent', res)
    except Exception as e:
        print('Error:', e)
    
    return '', 200


@app.route('/register-confirm/<username>', methods=['get'])
def register_confirm(username):
    print('to be confirmed', username)
    
    # TODO store user on pi
    
    time.sleep(3)
    
    try:
        res = requests.get('http://{}/register_confirm/{}/{}'.format(mood_server_ip, 2, username)).json()
        print('Confirmed', res)
    except Exception as e:
        print('Error:', e)
    
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port, debug=True)