#!/usr/bin/env python3
"""
This module introduces the upload route for uploading files and CSVs
"""
from flask import Flask, Blueprint, render_template, request, redirect, current_app
import pandas as pd
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}


upload_app = Blueprint('upload', __name__, template_folder='templates')


def allowed_file(filename):
    """
    Function for checking if a particular file is a csv or not.
    """
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_app.route('/upload', methods=['POST'])
def upload():
    """
    Function for checking if the post request has the file.
    """
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    # Check if the file has a CSV extension
    if file and allowed_file(file.filename):
        # save the uploaded file
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        filename = secure_filename('file.csv')

        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        try:
            df = pd.read_csv(filepath, encoding="latin-1")
            print(df.head())
            
        except Exception as e:
            return f'Error reading CSV file: {e}'
    
    return 'Invalid file format. Only CSV files are allowed.'
