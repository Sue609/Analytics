#!/usr/bin/env python3
"""
This module introduces the analyze route.
"""
from flask import Blueprint, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import plotly.graph_objects as go


analyze_app = Blueprint('analyze', __name__, template_folder='templates')

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


def create_boxplot_with_watermark(df, columns_data, column_names):
    """
    Function to create box plots with watermark for specified columns in a DataFrame.

    Parameters:
    df (DataFrame): The input DataFrame.
    columns_data (list): List of numpy arrays containing the data for each column to visualize.
    column_names (list): List of column names to be used for labeling.

    Returns:
    None
    """
    num_columns = len(columns_data)

    for i in range(num_columns):
        plt.figure(figsize=(10, 6))
        plt.boxplot(columns_data[i], vert=False)
        plt.title(f'Box Plot of {column_names[i]}')
        plt.xlabel(column_names[i])
        plt.grid(True)
        plt.text(0.9, 0.15, 'Watermark Text', fontsize=12, color='red', ha='right', va='bottom', alpha=0.7)
        plt.savefig(f'static/boxplot_with_watermark_{column_names[i]}.png')
        plt.close()


def create_histogram_with_watermark(year_data, column_data, column_name):
    """
    Function to create a histogram with watermark for a specified column in a DataFrame.

    Parameters:
    year_data (numpy.ndarray): The data for the 'Year' column.
    column_data (numpy.ndarray): The data for the column to visualize.
    column_name (str): The name of the column to visualize.

    Returns:
    None
    """
    plt.figure(figsize=(10, 6))
    plt.hist2d(year_data, column_data, bins=(20, 20), cmap='Blues')
    plt.title(f'Histogram of Year vs {column_name}')
    plt.xlabel('Year')
    plt.ylabel(column_name)
    plt.colorbar(label='Frequency')
    plt.grid(True)
    plt.text(0.9, 0.15, 'Watermark Text', fontsize=12, color='red', ha='right', va='bottom', alpha=0.7)
    plt.savefig(f'static/histogram_with_watermark_{column_name}.png')
    plt.close()


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

            analysis_method = request.form.get('analysis_method')

            if analysis_method == 'descriptive':
                descriptive_option = request.form.get('descriptive_option')
                summary_option = request.form.get('summary_statistics_option')

                if descriptive_option == 'summary_statistics':
                    summary_stats = summary_statistics(df, summary_option)
                    return render_template('summary_statistics.html', summary_stats=summary_stats)
                
                elif descriptive_option == 'data_visualization':
                    visualization_option = request.form.get('data_visualization_option')
                    if visualization_option == 'histograms':
                        columns_to_visualize = ['MMLU avg', 'Training computation (petaFLOP)', 'Training dataset size']
                        for column in columns_to_visualize:
                            if column not in df.columns:
                                return render_template('error.html', error_message=f"Invalid column name: {column}")
                        
                        year_data = df['Year'].values  # Convert Series to NumPy array
                        column_data = df[columns_to_visualize].values.T  # Transpose to get each column as a row
                        for data, column_name in zip(column_data, columns_to_visualize):
                            create_histogram_with_watermark(year_data, data, column_name)

                        return render_template('watermark_histogram.html')
                    
                    elif visualization_option == 'box_plots':
                        columns_to_visualize = ['MMLU avg', 'Training computation (petaFLOP)', 'Training dataset size']
                        for column in columns_to_visualize:
                            if column not in df.columns:
                                return render_template('error.html', error_message=f"Invalid column name: {column}")
                        
                        column_data = df[columns_to_visualize].values.T  # Transpose to get each column as a row
                        create_boxplot_with_watermark(df, column_data, columns_to_visualize)

                        return render_template('watermark_boxplots.html')


            else:
                return render_template('invalid_analysis_method.html')

        except Exception as e:
            return render_template('error.html', error_message=str(e))

    elif request.method == 'GET':
        return render_template('form.html')

    else:
        return "Invalid request method"