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
