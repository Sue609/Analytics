#!/usr/bin/env python3
"""
This file instroduces a class that creates a database
SQLAlchemy:
    - Creating databases
flask_login:
    - Flask class that provides user authentication such as
    form validation, account creation etc
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin


db = SQLAlchemy()


class Users(db.Model, UserMixin):
    """
    Class for storing user passwords and usernames in the database.
    """
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
