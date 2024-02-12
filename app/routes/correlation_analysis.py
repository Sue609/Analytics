#!/usr/bin/env python3
"""
This module introduces a correlation analysis.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def correlation_analysis(df):
    """
    Function for calculating the correlation matrix.
    Visualize the correlation matrix as a heatmap.
    Save the heatmap plot.
    """
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.tight_layout()
    
    correlation_plot_path = 'static/images/correlation_heatmap.png'
    plt.savefig(correlation_plot_path)
    plt.close()
    
    return correlation_plot_path
