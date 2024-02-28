#!/usr/bin/env python3
"""
This module introduces the analyze route.
"""
from flask import Blueprint, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


analyze_app = Blueprint('analyze', __name__, template_folder='templates')
import pandas as pd

def summary_statistics(df, summary_option):
    """
    Function to calculate summary statistics based on the selected option.
    
    Parameters:
    df (DataFrame): The input DataFrame.
    summary_option (str): The selected summary statistics option ('mean_median_mode' or 'standard_deviation').
    
    Returns:
    result: Summary statistics based on the selected option.
    """
    # Convert numeric columns to numeric format
    numeric_cols = ['Year', 'MMLU avg', 'Training computation (petaFLOP)', 'Training dataset size']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    if summary_option == 'mean_median_mode':
        result = df[['Year', 'MMLU avg', 'Training computation (petaFLOP)', 'Training dataset size']].agg(['mean', 'median', lambda x: x.mode().iloc[0]])
    elif summary_option == 'standard_deviation':
        result = df[['Year', 'MMLU avg', 'Training computation (petaFLOP)', 'Training dataset size']].std().to_frame().T
        result.index = ['Standard Deviation']
    else:
        result = pd.DataFrame()
    return result




@analyze_app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    """
    Function for loading the DataFrame from a CSV file,
    performing data validation and cleaning, and then performing analysis.
    """
    if request.method == 'POST':
        try:
            df = pd.read_csv('uploads/file.csv', encoding='latin-1')

            # Check if DataFrame is empty after loading CSV
            if df.empty:
                return render_template('error.html', error_message="Failed to load CSV file or DataFrame is empty")

            print(df.info())  # Print information about DataFrame
            analysis_method = request.form.get('analysis_method')

            if analysis_method == 'descriptive':
                descriptive_option = request.form.get('descriptive_option')
                summary_option = request.form.get('summary_statistics_option')

                if descriptive_option == 'summary_statistics':
                    summary_stats = summary_statistics(df, summary_option)
                    return render_template('summary_statistics.html', summary_stats=summary_stats)

            else:
                return render_template('invalid_analysis_method.html')

        except Exception as e:
            return render_template('error.html', error_message=str(e))

    elif request.method == 'GET':
        return render_template('form.html')

    else:
        return "Invalid request method"