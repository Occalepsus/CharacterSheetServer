from flask import Blueprint, Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO, emit
from flask_login import login_required, current_user
from __init__ import create_app, db
#from flask.ext.sqlalchemy import SQLAlchemy

values = {'name': 'a', 'value': '0'}

main = Blueprint('main', __name__)

app=create_app()
socketio = SocketIO(app)

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("indexBis.html", **values)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/js/test.js')
def sendScript():
    return send_from_directory("./scripts", "test.js")


@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})
    print('Client conected')


@socketio.on('data value changed')
def value_changed(message):
    values[message['who']] = message['data']
    print('Message recieved : ' + message['who'] + ', ' + message['data'])
    emit('update', message, broadcast=True)


if __name__ == '__main__':
    db.create_all(app=create_app())
    socketio.run(app, host='0.0.0.0', debug=True)