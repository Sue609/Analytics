#!/usr/bin/env python3
"""
This module instroduces a flask application.
"""
from flask import Flask, request, url_for, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['ASQLALCHEMY_DATABASE_URI'] = "sqlite://users.db"


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route("/", )
def home():
    pass

if __name__ == "__main__":
    app.run(debug=True)