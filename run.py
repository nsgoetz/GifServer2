import os
import random
from flask_socketio import SocketIO, emit
from typing import List

from flask import Flask, send_from_directory, render_template, url_for


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

IMAGE_DIR = './img'


def read_all_filenames() -> List[str]:
    file_names = os.listdir(IMAGE_DIR)
    return file_names


@app.route('/')
def run():
    filenames = read_all_filenames()
    filename = random.choice(filenames)
    file_url = url_for('show_image', image_id=filename)

    # file_path = os.path.join(IMAGE_DIR, filename)
    return render_template('serve_gif_sockets.html', first_gif=file_url)


@app.route('/img/<image_id>')
def show_image(image_id):
    return send_from_directory(directory=IMAGE_DIR, path=image_id)

@socketio.on('requestNewImage')
def handle_message():
    print('received message: requestNewImage')
    filenames = read_all_filenames()
    filename = random.choice(filenames)
    file_url = url_for('show_image', image_id=filename)

    emit('imageResponse', file_url)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=4339)
