# Importing packages
###from socket import socket
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import socketio


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# create_app function is used to init our flask application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    global socketio
    socketio = SocketIO(app)

    login_manager = LoginManager() # Create a Login Manager instance
    login_manager.login_view = 'auth.login' # define the redirection path when login required and we attempt to access without being logged in
    login_manager.init_app(app) # configure it for login
    
    from models import Users
    @login_manager.user_loader
    def load_user(user_id): #reload user object from the user ID stored in the session since the user_id is just the primary key of our user table, use it in the query for the user
        return Users.query.get(int(user_id))

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from profile import player_profile as prof_blueprint
    app.register_blueprint(prof_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app