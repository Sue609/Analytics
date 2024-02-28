#!/usr/bin/env python3
"""
This module introduces the analyze route.
"""
from flask import render_template, request, redirect, url_for, current_app
from flask.blueprints import Blueprint
import pandas as pd
import os
from werkzeug.utils import secure_filename
from routes.upload import allowed_file


clean_data_app = Blueprint('clean_data_app', __name__, template_folder='templates')

@clean_data_app.route('/clean_data', methods=['GET', 'POST'])
def data_cleaning():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            
            filename = secure_filename('data_cleaning_files.csv')

            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            try:
                df = pd.read_csv(filepath, encoding="latin-1")
                
                # Clean the data
                cleaned_df = clean_data(df)
                
                cleaned_filepath = os.path.join(upload_folder, 'cleaned_data.csv')
                cleaned_df.to_csv(cleaned_filepath, index=False)

                return render_template('data_cleaning.html', cleaned_data=cleaned_df.to_html(), filename=cleaned_filepath)

            except Exception as e:
                return f'Error reading or cleaning CSV file: {e}'

    return render_template('data_cleaning.html')


