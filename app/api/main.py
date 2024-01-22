#!/usr/bin/env python3
"""
This module instroduces a flask application.
"""
from flask import Flask
from flask_login import LoginManager
from models.database.users import db
from flask_argon2 import Argon2
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
argon2 = Argon2(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'


setup_done = False


@app.before_request
def create_tables():
    """
    Function for creating database tables before the first
    request is handled.
    """
    global setup_done
    
    if not setup_done:
        db.create_all()
        setup_done = True


if __name__ == "__main__":
    app.run(debug=True)