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
@auth.route('/login', methods=['GET', 'POST']) # define login page path
def login():
        if request.method == 'GET':
                return render_template('login.html')
        else:
                email = request.form.get('email')
                password = request.form.get('password')
                remember = True if request.form.get('remember') else False
                user = User.query.filter_by(email=email).first()
                
                if not user:
                        flash('Please sign up before !')
                        return redirect(url_for('auth.signup'))
                elif not check_password_hash(user.password, password):
                        flash('Wrong password')
                        return redirect(url_for('auth.login'))
                
                else:
                        login_user(user, remember=remember)
                        return redirect(url_for('main.profile'))

####################################################################
@auth.route('/signup', methods=['GET', 'POST'])# we define the sign up path
def signup(): # define the sign up function
        if request.method == 'GET':
                return render_template('signup.html')
        #if the request if POST, we check email
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
@login_required
def logout(): #define the logout function
        logout_user()
        return render_template('logout.html')