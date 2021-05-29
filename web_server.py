import json
import pafy
import os
from flask import Flask, render_template, Response, request, redirect, url_for

from constants import server_port, light_settings_path, sounds_path


# TODO delete end points ??
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-custom-light', methods=['post'])
def add_light():
    data = {}
    with open(light_settings_path, "r") as f:
        data = json.load(f)
    data[request.form['light-mood']] = {"bri": request.form["brightness"], "ct": request.form["color-temperature"]}
    
    with open(light_settings_path, "w") as f:
        json.dump(data, f)
    
    return redirect(url_for('index'))


@app.route('/add-custom-sound', methods=['post'])
def add_sound():
    result = pafy.new(request.form['youtube-link'])
    
    min_index = 0
    for i, stream in enumerate(result.audiostreams):
        if stream.get_filesize() < result.audiostreams[min_index].get_filesize():
            min_index = i
    
    path = sounds_path + '/' + request.form['sound-mood'] + '/' + request.form['sound-name'] + '.m4a'
    print('path >>>> ', path)
    
    while True:
        try:
            result.audiostreams[i].download(path)
            print('>>>>>>>>>> downloaded <<<<<<<<<<')
            break
        except:
            pass
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port, debug=True)