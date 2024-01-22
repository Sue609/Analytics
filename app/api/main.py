#!/usr/bin/env python3
"""
This module introduces a Flask application.
"""
from flask import Flask, request, redirect, url_for, render_template
from flask_login import LoginManager, UserMixin, login_user
from flask_argon2 import Argon2
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
argon2 = Argon2(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class Users(db.Model, UserMixin):
    """
    Class for storing user passwords and usernames in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def create_user(username, email, password):
    """
    Function to create a new user.
    Hashing the password using Argon2
    Input:
        username: The username of the individual to register
        password: The password.
    Store the new user in the database.
    """
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
        
        if user is not None and argon2.check_password_hash(user.password, password):
            # if password is correct, log the user in
            login_user(user)
            return redirect(url_for('dashboard'))
        
        error_message = "Invalid email or password. Please try again."
        return render_template("index.html", error=error_message)
        
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   
    app.run(debug=True)
