#import imp
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
import json
import os
from flask_socketio import emit
from models import Sheets
from __init__ import db
#from main import socketio

player_profile = Blueprint('player_profile', __name__)
root = os.path.dirname(os.path.abspath(__file__))

def create_new_profile(name:str):
    os.mkdir(root + '/users/' + name)    


@player_profile.route('/profile')
@login_required
def profile():
    rows = Sheets.query.filter(Sheets.user==current_user.name).all()

    return render_template('profile.html', name=current_user.name, rows=rows)


def value_changed(message):
    #values[message['who']] = message['data']
    print('Message recieved : ' + message['who'] + ', ' + message['data'])
    emit('update', message, broadcast=True)
