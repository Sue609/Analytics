#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for, request
from routes.auth import db, argon2, login_manager, Users, create_user_and_login
from flask_login import login_user
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
argon2.init_app(app)
login_manager.init_app(app)



@app.route('/signup', methods=['GET', 'POST'])
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
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        
        return redirect(url_for('dashboard'))
        
    return render_template('index.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
