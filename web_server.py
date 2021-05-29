from flask import Flask, render_template, Response, request

from constants import server_port


# TODO delete end point ??
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-custom-light')
def add_light():
    pass


@app.route('/add-custom-sound')
def add_sound():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port, debug=True)