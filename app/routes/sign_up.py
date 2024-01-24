#!/usr/bin/env python3
"""
This module introduces flask signup route
"""
from flask import Flask, render_template, redirect, url_for, request, Blueprint
from routes.auth import db, argon2, login_manager, Users
from flask_login import login_user, current_user, login_required
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError

signup_app = Blueprint('signup', __name__)

@signup_app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Defining a route that allows users to sign up and create a new account.
    Check if the email is already registered.
    Hash tha password using argon2.
    create new user and add them to the db.
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = Users.query.filter_by(email=email).first()
        if user:
            error_message = "Email already registred. Please use a different email"
            return render_template("index.html", error=error_message)
        
        hashed_pwd = argon2.generate_password_hash(password)
        new_user = Users(username=username, email=email, password=hashed_pwd)
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard'))
        except IntegrityError:
            db.session.rollback()
            error_message = "An error occured while creating the user. Please try again"
            return render_template("index.html", error=error_message)

    return render_template('index.html')
