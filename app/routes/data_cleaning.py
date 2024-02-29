from routes.upload import allowed_file
from flask import render_template, request, redirect, url_for, Blueprint, current_app
import pandas as pd
import os
from werkzeug.utils import secure_filename

clean_data_app = Blueprint('clean_data_app', __name__)


def clean_data(df):
    # Add your data cleaning logic here
    cleaned_df = df  # Placeholder for actual data cleaning logic
    return cleaned_df


@clean_data_app.route('/clean_data', methods=['GET', 'POST'])
def handle_clean_data():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save the uploaded file
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            
            filename = secure_filename('data_cleaning_files.csv')
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            try:
                df = pd.read_csv(filepath, encoding="latin-1")
                
                # Clean the data
                cleaned_df = clean_data(df)
                
                # Save the cleaned data to a new CSV file
                cleaned_filepath = os.path.join(upload_folder, 'cleaned_data.csv')
                cleaned_df.to_csv(cleaned_filepath, index=False)
    
                # Render the clean_data.html template with the uploaded and cleaned data
                return render_template('data_cleaning.html', cleaned_data=cleaned_df.to_html(), filename=cleaned_filepath)

            except Exception as e:
                return f'Error reading or cleaning CSV file: {e}'

    return render_template('data_cleaning.html')
