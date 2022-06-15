from flask import Blueprint, render_template, redirect, send_from_directory, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
import json
import os
from flask_socketio import emit
from numpy import broadcast
from sqlalchemy import false
from models import Sheets, Users

player_profile = Blueprint('player_profile', __name__)
root = os.path.dirname(os.path.abspath(__file__))

def create_new_profile(name:str):
    os.mkdir(root + '/users/' + name)    


@player_profile.route('/profile')
@login_required
def profile():
    user = Users.query.filter(Users.name==current_user.name).first()
    if not user.isAdmin:
        rows = Sheets.query.filter(Sheets.user==current_user.name).all()
    else:
        rows = Sheets.query.all()

    return render_template('profile.html', name=current_user.name, rows=rows)




@player_profile.route('/<username>/sheet<id>')
@login_required
def send_sheet(id, username):
    status = canUserLoad(id, username)
    if status == 404:
        return '404, not found'
    elif status == 403:
        return '403, unauthorized'
    elif status == 200:
        return render_template('sheet.html', pageId=id)
    else:
        return None



#Called on socket 'data value changed'
def value_changed(message):
    print('Message recieved')
    id = message['id']
    status = canUserLoad(id, username=current_user.name)
    if status == 404:
        print('404 error')
        emit('exception', {"errorMessage" :"404 not found"})
    elif status == 403:
        print('403 error')
        emit('exception', {"errorMessage": "403 not authorised"})
    elif status == 200:
        if not canUserChange(message['field']):
            emit('exception', {"error": "403 not authorized"})
            return
        else:
            emit('update', message, room='room' + id)

            path = current_user.name + '/sheet' + id + '.json'
            data = readJsonFile(path)
            data[message['field']] = message['value']
            writeJsonFile(data, path)



def readJsonFile(path:str):
    with open(root + '/users/' + path) as jsonFile:
        return json.load(jsonFile)


def writeJsonFile(data, path:str):
    with open(root + '/users/' + path, 'w', encoding='utf_8') as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False, indent=4)


def canUserLoad(id, username):
    sheet = Sheets.query.filter(Sheets.id==id).first()
    if not sheet:
        return 404 #Not found status
    user = Users.query.filter(Users.name==current_user.name).first()
    if not user.isAdmin:
        availableSheet = Sheets.query.filter(Sheets.id==id, Sheets.user==current_user.name).first()
        if not availableSheet:
            return 403 #Unauthorized status
    return 200 #Ok status


userAccessibleList = ["name", "age", "type"]
userModifiableList = ["age", "type"]

def canUserChange(field):
    user = Users.query.filter(Users.name==current_user.name).first()
    if not user.isAdmin:
        if field in userModifiableList:
            return True
        else:
            return False
    else:
        return True