import json

from flask import Flask, render_template
from pathlib import Path
from flask_socketio import SocketIO, emit


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

images = []

images.append(Path('static/abc1.png'))
images.append(Path('static/abc2.png'))


@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    try:
        f = open("test.txt", 'r')
        data = f.read()
        idx = int(json.loads(data).get("id")) + int(1)
        data = {"id" : str(idx)}
    except:
        pass
    return render_template('index.html', data=data)

@socketio.on('connect')
def ws_connect():
    try:
        f = open("test.txt", 'r')
        data = f.read()
        idx = int(json.loads(data).get("id")) + int(1)
        data = {"id" : str(idx)}
        emit('connect', data, broadcast=True)

        fw = open("test.txt", 'w', encoding='utf-8')
        fw.write(json.dumps(data))
        fw.close()
    except:
        pass

@socketio.on('disconnect')
def ws_disconnect():
    try:
        f = open("test.txt", 'r')
        data = f.read()
        idx = int(json.loads(data).get("id")) - int(1)
        data = {"id": str(idx)}
        emit('disconnect', data, broadcast=True)

        fw = open("test.txt", 'w', encoding='utf-8')
        fw.write(json.dumps(data))
        fw.close()
    except:
        pass

@socketio.on('message')
def handle_message(data):
    global index, images
    pass

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@socketio.on('my event', namespace='/test')
def handle_my_custom_namespace_event(json):
    print('received json: ' + str(json))

if __name__ == "__main__":
    socketio.run(app)
