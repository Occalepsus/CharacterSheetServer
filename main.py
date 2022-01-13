from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO, emit

values = {'name': 'a', 'value': '0'}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'tempKey'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")


@app.route('/js/test.js')
def sendScript():
    return send_from_directory("./scripts", "test.js")


@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})


@socketio.on('data value changed')
def value_changed():
    values[message['who']] = message['data']


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')