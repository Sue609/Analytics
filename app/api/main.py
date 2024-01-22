#!/usr/bin/env python3
"""
This module instroduces a flask application.
"""
from flask import Flask, request, url_for, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from models.database.users import Users, db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['ASQLALCHEMY_DATABASE_URI'] = "sqlite://users.db"


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