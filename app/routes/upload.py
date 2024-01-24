#!/usr/bin/env python3
"""
This module introduces the upload route for uploading files and CSVs
"""
from flask import Flask, Blueprint, render_template, request
import pandas as pd


upload_app = Blueprint('upload', __name__, template_folder='templates')


@upload_app('/upload', method=['POST'])
def upload():
    """
    Function for checking if the post request has the file.
    """
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    # Check if the file has a CSV extension
    if file.filename.endswith('.csv'):
        df = df.read_csv(file)