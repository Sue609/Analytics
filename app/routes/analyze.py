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

def descriptive_analysis(df, analysis_type, plot_type):
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
    plot_path = None
    summary_statistics = df.describe()

    if analysis_type == 'histogram':
        if plot_type == 'customized_histogram_density':
            # Your existing implementation for customized histogram density plot
            pass
        elif plot_type == 'waterline':
            # Create a figure and axis
            plt.figure(figsize=(12, 8))
            
            # Plotting the waterline histogram
            sns.histplot(df, bins='auto', color='skyblue', edgecolor='black', stat='density')
            sns.kdeplot(df, color='red', linestyle='--')

            plt.title('Waterline Histogram')
            plt.xlabel('X-axis Label')
            plt.ylabel('Density')
            plt.grid(True)
            plt.tight_layout()
            plot_path = 'static/waterline_histogram.png'  # Update the plot path
            plt.savefig(plot_path, dpi=100)
            plt.close()

    return plot_path, summary_statistics  
    '''
    plot_path = None
    summary_statistics = df.describe()
       
    if analysis_type == 'histogram':
        if plot_type == 'customized_histogram_density':
            # Create a figure and axis
            plt.figure(figsize=(12, 8))
            
            sns.histplot(df, kde=True, color='skyblue', edgecolor='black')

            plt.title('Customized Histogram with Density Plot')
            plt.xlabel('X-axis Label')
            plt.ylabel('Density')
            plt.grid(True)
            plt.tight_layout()
            plot_path = 'static/histogram_density.png'
            plt.savefig(plot_path, dpi=100)
            plt.close()
            
            # Compute summary statistics
    return plot_path, summary_statistics
    
    if analysis_type == 'histogram':
        if plot_type == 'customized_histogram_density':
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
                plt.savefig(histogram_path, dpi=100)
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
                plt.savefig(box_plot_path, dpi=100)
                plt.close()
                box_plots.append(box_plot_path)
            
            return histograms, box_plots, summary_statistics
            '''


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
    Calculate the correlation matrix, visualize it as a heatmap,
    and save the heatmap plot.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing numeric columns.

    Returns:
    str: File path to the saved correlation heatmap plot.
    """
    numeric_df = df.select_dtypes(include='number')

    if numeric_df.empty:
        raise ValueError("No numeric columns found for correlation analysis")

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
        try:
            df = pd.read_csv('uploads/file.csv', encoding='latin-1')
            
            # Data cleaning
            if df.isnull().values.any():
                df = df.dropna()

            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                
            if not df.empty:  # Use the .empty attribute to check if the DataFrame is empty
                print("DataFrame is NOT empty")


            analysis_method = request.form.get('analysis_method')

            if analysis_method == 'descriptive':
                plot_type = request.form.get('descriptive_option')  # Corrected variable name

                if plot_type:
                    plot_path, summary_statistics = descriptive_analysis(df, analysis_method, plot_type)
                    return render_template('descriptive_analysis.html', plot_path=plot_path, summary_statistics=summary_statistics)
                else:
                    return render_template('invalid_analysis_option.html')  # Handle case where descriptive option is not selected

            elif analysis_method == 'custom':
                time_series_plot_path, time_series_decomposition_path = custom_analysis(df)
                return render_template('custom_analysis.html', time_series_plot=time_series_plot_path, time_series_decomposition=time_series_decomposition_path)

            elif analysis_method == 'correlation':
                correlation_plot_path = correlation_analysis(df)
                return render_template('correlation_analysis.html', correlation_plot=correlation_plot_path)

            elif analysis_method == 'univariate':
                correlation_plot_path, line_graph_path = univariate_analysis(df)
                return render_template('univariate_analysis.html', correlation_plot=correlation_plot_path, line_graph=line_graph_path)

            else:
                return render_template('invalid_analysis_method.html')  # Handle case where analysis method is not recognized

        except Exception as e:
            # Handle exceptions and return an error page
            return render_template('error.html', error_message=str(e))

    else:
        return "Invalid request method"  # Handle invalid request method
