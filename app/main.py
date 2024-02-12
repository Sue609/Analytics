#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for, request
from routes.auth import db, argon2, login_manager, Users
from flask_login import login_user, current_user, login_required
from dotenv import load_dotenv
import os
from routes.signup import signup_app
from routes.upload import upload_app
from routes.analyze import analyze_app
from routes.correlation_analysis import correlation_app


load_dotenv()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


app.register_blueprint(signup_app)
app.register_blueprint(upload_app)
app.register_blueprint(analyze_app)
app.register_blueprint(correlation_app)


app.config['SECRET_KEY'] = 'data_analytic'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
argon2.init_app(app)
login_manager.init_app(app)


@app.route('/')
def home():
    """
    Route for the home page.
    """
    return render_template('main.html')


@app.route('/dashboard')
@login_required
def dashboard():
    """
    Route for displaying user-specific dashboard information.
    """
    user = current_user
    
    additional_data = {
        'key1': 'value1',
        'key2': 'value2',
    }
    
    return render_template('dashboard.html', user=user, additional_data=additional_data)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
