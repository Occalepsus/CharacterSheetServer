from enum import unique
from flask_login import UserMixin
from __init__ import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean)


class Sheets(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(1000), unique=True)
    user = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
