# main.py
from flask import Flask, render_template, redirect, url_for, request
from app.api.Authentication.auth import db, argon2, login_manager, Users, create_user_and_login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"

db.init_app(app)
argon2.init_app(app)
login_manager.init_app(app)



@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        create_user_and_login(username, email, password)

        return redirect(url_for('dashboard'))

    return render_template('signup.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
