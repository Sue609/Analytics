#!/usr/bin/python3


def create_user(username, password):
    """
    Function to create a new user.
    Hashing the password using Argon2
    Input:
        username: The username of the individual to register
        password: The password.
    Store the new user in the database.
    """
    hashed_pwd = argon2.generate_password_hash(password)
    new_user = Users(username=username, password=hashed_pwd)
    db.session.add(new_user)
    db.session.commit()