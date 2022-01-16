# Import packages
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db

# We define our blueprint for authentification
auth = Blueprint('auth', __name__)

# For logging in
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        name = request.form.get('name')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = Users.query.filter_by(name=name).first()
                
        if not user:
                flash('Please sign up before !')
                return redirect(url_for('auth.signup'))

        elif not check_password_hash(user.password, password):
                flash('Wrong password')
                return redirect(url_for('auth.login'))
        
        else:
                login_user(user, remember=remember)
                return redirect(url_for('player_profile.profile'))


# For singing up
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    else:
        name = request.form.get('name')
        password = request.form.get('password')
        isAdmin = False
        user = Users.query.filter_by(name=name).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        password=generate_password_hash(password, method='sha256')
        new_user = Users(name=name, password=password, isAdmin=isAdmin)

        db.session.add(new_user)
        db.session.commit()



        return redirect(url_for('auth.login'))


# For logging out
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template(url_for('main.index'))