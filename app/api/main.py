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
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://users.db"
db = SQLAlchemy(app)

# Initialize the database after importing
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.before_first_request
def create_tables():
    """
    Function for creating database tables before the first
    request is handled.
    """
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)