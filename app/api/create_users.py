#!/usr/bin/python3
from models.database.users import Users, db
from app.api.main import argon2, app
from flask import request, render_template, redirect, url_for
from flask_argon2 import check_password_hash, generate_password_hash
from flask_login import login_user


def create_user(username, email, password):
    """
    Function to create a new user.
    Hashing the password using Argon2
    Input:
        username: The username of the individual to register
        password: The password.
    Store the new user in the database.
    """
    print("hey sue")
    hashed_pwd = argon2.generate_password_hash(password)
    new_user = Users(username=username, email=email, password=hashed_pwd)
    db.session.add(new_user)
    db.session.commit()

   
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Defining a route that allows a user to login to their accounts.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = Users.query.filter_by(email=email).first()
        
        #if user is None:
            #raise IncorrectEmailError('Incorrect email!')

        if user is not None and argon2.check_password_hash(user.password, password):
            # if password is correct, log the user in
            login_user(user)
            return redirect(url_for('dashboard'))
        
        # incorrect name and password
        #except IncorrectEmailError as e:
            #return render_template("login.html", error="Incorrect email")
         
    return render_template('index.html')
            