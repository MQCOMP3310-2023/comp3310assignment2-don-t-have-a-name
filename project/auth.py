from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user
from sqlalchemy import text
from .models import User
from . import db, limiter
from werkzeug.security import generate_password_hash, check_password_hash
import re
from validate_email_address import validate_email



auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login_post():
    if request.form['email']:
        inEmail = request.form['email']
         #  Check to ensure valid gmail account syntax'
        if not re.match("^[a-zA-Z .@']+@gmail.com$", inEmail):  
            flash('valid email only include letters, numbers, . and @ .')
            login()
        email = inEmail
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    
    # check if the user actually exists
    # take the user-supplied password and compare it with the stored password
    if not user or (user.is_password_correct(password) == False):
        flash('Please check your login details and try again.')
        current_app.logger.warning("User login failed")
        if user is None:
            return redirect(url_for('auth.login')) # if the user doesn't exist reload the page
        elif user.passwordAttempts >= 8:
            
            flash('Too many incorrect password attempts, try again later')
            return redirect(url_for('auth.login'), code=429)
        else:
            user.passwordAttempts = user.passwordAttempts + 1
            db.session.commit()
        return redirect(url_for('auth.login')) 
    # if the above check passes, then we know the user has the right credentials

    elif user.passwordAttempts >= 8:

            flash('Too many incorrect password attempts, try again later')
            return redirect(url_for('auth.login'), code=429)
    else:
        login_user(user, remember=remember)
        return redirect(url_for('main.showRestaurants'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
@limiter.limit("5 per minute")
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Check if the email address is a valid Gmail address
    if not re.match("^[a-zA-Z0-9._%+-]+@gmail.com$", email):
        flash('Please enter a valid Gmail address.')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')  # 'flash' function stores a message accessible in the template code.
        current_app.logger.debug("User email already exists")
        return redirect(url_for('auth.signup'))
    
    if verify_email_exists(email):
        # create a new user with the form data.
        new_user = User(email=email, name=name)
        new_user.set_password(password)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
    
    if not verify_email_exists(email):
        flash('This Email address is not valid')

    return redirect(url_for('auth.login'))

def verify_email_exists(email):
    return validate_email(email, verify=True)

@auth.route('/logout')
@login_required
def logout():
    logout_user();
    return redirect(url_for('main.showRestaurants'))

# See https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login for more information
