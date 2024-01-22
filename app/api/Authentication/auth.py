#!/usr/bin/env python3
"""
This module introduces a class for creating and connecting to the db.
"""
from flask_login import LoginManager, UserMixin, login_user
from flask_argon2 import Argon2
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
argon2 = Argon2()

login_manager = LoginManager()
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


def create_user_and_login(username, email, password):
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
    login_user(new_user)
