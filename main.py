from socket import socket
from flask import Blueprint, Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO, emit
from flask_login import login_required, current_user
from auth import auth as auth_blueprint
from profile import player_profile as prof_blueprint
from __init__ import create_app, db
from profile import value_changed


from models import Sheets

values = {'name': 'a', 'value': '0'}

main = Blueprint('main', __name__)

app = create_app()
socketio = SocketIO(app)

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("indexBis.html", **values)


@main.route('/js/<name>.js')
def sendScript(name):
    return send_from_directory("./scripts", name + ".js")


@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})
    print('Client conected')

@socketio.on('data value changed')
def pass_value_changed(message):
    return value_changed(message)


if __name__ == '__main__':
    db.create_all(app=app)
    socketio.run(app, host='0.0.0.0', debug=True)