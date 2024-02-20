#!/usr/bin/python3
import pandas as pd
import json


def data_cleaning():
    """
    Function that does data cleaning and transformation using pandas.
    Reading csv file and loading it to a dataframe using pandas.
    """
    data_match = pd.read_csv('../uploads/file.csv')
    
    print(data_match.head())
data_cleaning()