####################################################################
##############          Import packages      #######################
####################################################################
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security \
import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, \
                                     login_required, current_user
from __init__ import db


####################################################################
auth = Blueprint('auth', __name__) # create a Blueprint object that 
                                   # we name 'auth'

####################################################################
@auth.route('/login', methods=['GET']) # define login page path
def login(): # define login page fucntion
        #return 'login'
        return render_template('login.html')
####################################################################
@auth.route('/signup', methods=['GET'])# we define the sign up path
def signup(): # define the sign up function
        if request.method == 'GET':
                return render_template('signup.html')
        else:
                email = request.form.get('email')
                name = request.form.get('name')
                password = request.form.get('password')
                user = User.query.filter_by(email=email).first()
                if user:
                        flash('Email address already exists')
                        return redirect(url_for('auth.signup'))
                password=generate_password_hash(password, method='sha256')
                new_user = User(email=email, name=name, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('auth.login'))

####################################################################
@auth.route('/logout') # define logout path
def logout(): #define the logout function
    return render_template('logout.html')