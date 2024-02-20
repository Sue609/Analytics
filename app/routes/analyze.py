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

def descriptive_analysis(df):
    """
    Perform descriptive analysis methods on the input DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data for analysis.

    Returns:
        tuple: A tuple containing the following elements:
            - list: A list of file paths to the generated histogram plots.
            - list: A list of file paths to the generated box plot plots.
            - pandas.DataFrame: Summary statistics of the input DataFrame.
    """
    histograms = []
    box_plots = []
    summary_statistics = df.describe()

    for column in df.select_dtypes(include='number').columns:
        plt.figure(figsize=(12, 8))
        plt.hist(df[column], bins=10)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.tight_layout()
        histogram_path = f'static/histogram_{column}.png'
        plt.savefig(histogram_path, dpi=300)
        plt.close()
        histograms.append(histogram_path)
    
    for column in df.select_dtypes(include='number').columns:
        plt.figure(figsize=(12, 8))
        sns.boxplot(x=df[column])
        plt.title(f'Box Plot of {column}')
        plt.xlabel(column)
        plt.grid(True)
        plt.tight_layout()
        box_plot_path = f'static/box_plot_{column}.png'
        plt.savefig(box_plot_path, dpi=300)
        plt.close()
        box_plots.append(box_plot_path)
    
    return histograms, box_plots, summary_statistics


def custom_analysis(df):
    """
    Perform custom analysis methods on the input DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data for analysis.

    Returns:
        tuple: A tuple containing the file paths of the generated images.
    """
    if 'Date' not in df.columns:
        raise ValueError("Column 'Date' not found in the DataFrame.")

    result = {}

    time_series_data = df.set_index('Date')
    time_series_data.index = pd.to_datetime(time_series_data.index)  # Convert index to datetime

    plt.figure(figsize=(12, 8))
    time_series_data['Value'].plot()
    plt.title('Time Series Data')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.grid(True)
    plt.tight_layout()
    time_series_plot_path = 'static/time_series_plot.png'
    plt.savefig(time_series_plot_path, dpi=300)
    plt.close()

    decomposition = sm.tsa.seasonal_decompose(time_series_data['Value'], model='additive')
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    plt.figure(figsize=(14, 10), dpi=100)
    plt.subplot(411)
    plt.plot(time_series_data['Value'], label='Original')
    plt.legend(loc='best')
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(413)
    plt.plot(seasonal, label='Seasonal')
    plt.legend(loc='best')
    plt.subplot(414)
    plt.plot(residual, label='Residual')
    plt.legend(loc='best')
    plt.tight_layout()
    time_series_decomposition_path = 'static/time_series_decomposition.png'
    plt.savefig(time_series_decomposition_path, dpi=300)
    plt.close()

    return time_series_plot_path, time_series_decomposition_path


def correlation_analysis(df):
    """
    Function for calculating the correlation matrix.
    Visualize the correlation matrix as a heatmap.
    Save the heatmap plot.
    """
    numeric_df = df.select_dtypes(include='number')

    corr_matrix = numeric_df.corr()

    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.tight_layout()

    correlation_plot_path = 'static/correlation_heatmap.png'
    plt.savefig(correlation_plot_path)
    plt.close()
    
    return correlation_plot_path


def univariate_analysis(df):
    """
    Function for calculating the correlation matrix and visualizing it as a heatmap,
    and also creating a line graph to visualize the relationship between two specific variables.
    Save the heatmap plot and line graph.
    """
    numeric_df = df.select_dtypes(include='number')

    corr_matrix = numeric_df.corr()

    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.tight_layout()

    correlation_plot_path = 'static/correlation_heatmap.png'
    plt.savefig(correlation_plot_path)
    plt.close()

    variable1 = 'Age'
    variable2 = 'Income'

    plt.figure()
    plt.plot(df[variable1], df[variable2], marker='o', linestyle='-')
    plt.title(f'Line Graph of {variable1} vs {variable2}')
    plt.xlabel(variable1)
    plt.ylabel(variable2)
    plt.tight_layout()

    line_graph_path = 'static/line_graph.png'
    plt.savefig(line_graph_path)
    plt.close()

    return correlation_plot_path, line_graph_path


@analyze_app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    """
    Function for loading the DataFrame from a CSV file,
    performing data validation and cleaning, and then performing analysis.
    """
    if request.method == 'POST':
        df = pd.read_csv('uploads/file.csv', encoding='latin-1')

        if df.isnull().values.any():
            df = df.dropna()

        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])

        analysis_method = request.form.get('analysis_method')

        if analysis_method == 'descriptive':
            histograms, box_plots, summary_statistics = descriptive_analysis(df)
            return render_template('descriptive_analysis.html', histograms=histograms, box_plots=box_plots, summary_statistics=summary_statistics)
        
        elif analysis_method == 'custom':
            try:
                time_series_plot_path, time_series_decomposition_path = custom_analysis(df)
                return render_template('custom_analysis.html', time_series_plot=time_series_plot_path, time_series_decomposition=time_series_decomposition_path)
            except ValueError as e:
                return render_template('custom_analysis_error.html', error_message=str(e))

        elif analysis_method == 'correlation':
            correlation_plot_path = correlation_analysis(df)
            return render_template('correlation_analysis.html', correlation_plot=correlation_plot_path)
        
        elif analysis_method == 'univariate':
            correlation_plot_path, line_graph_path = univariate_analysis(df)
            return render_template('univariate_analysis.html', correlation_plot=correlation_plot_path, line_graph=line_graph_path)

        else:
            return render_template('invalid_analysis_method.html')
    
    else:
        return "Invalid request method"