#!/usr/bin/env python3
"""
This module introduces a correlation analysis.
"""
from flask import Blueprint, request, render_template
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

correlation_app = Blueprint('analyze', __name__, template_folder='templates')

