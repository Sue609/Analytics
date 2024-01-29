#!/usr/bin/env python3
"""
This module introduces the analyze route.
"""
from flask import Blueprint, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


analyze_app = Blueprint('analyze', __name__, template_folder='templates')

def custom_analysis(df, parameters):
    """
    Function to implement the custom analysis logic
    """
    group_by_column = parameters.get('group_by_column')
    
    if group_by_column:
        result = df.groupby(group_by_column).agg({'value': 'sum'})
        
        # Generate visualization
        plt.figure(figsize=(10, 6))
        sns.barplot(x=result.index, y='value', data=result)
        plt.title('Custom Analysis Result')
        plt.xlabel(group_by_column)
        plt.ylabel('Sum of Values')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig('static/custom_analysis_plot.png')
        # Close plot to free resources
        plt.close()
        
        return result
    else:
        return "Group by column not specified" 

@analyze_app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    # Load the DataFrame from a CSV file
    df = pd.read_csv('uploads/file.csv')
    
    analysis_method = request.form.get('analysis_method')
    
    if analysis_method == 'describe':
        result = df.describe()
        
        # Generate visualization
        plt.figure(figsize=(10, 6))
        df.hist()
        plt.suptitle('Histogram of data')
        plt.tight_layout()
        plt.savefig('static/describe_analysis_plot.png')
        plt.close()
        
    elif analysis_method == 'custom':
        # Implement custom analysis based on user input
        # You can retrieve additional parameters from the form
        result = custom_analysis(df, request.form)
    else:
        result = "Invalid analysis method"

    return render_template('result.html', result=result)
