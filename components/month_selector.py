from dash import dcc
from utils.filters import get_latest_month, get_all_months
import pandas as pd

# Add month selector component
def create_month_selector(df):

    # Convert the 'month' column to datetime format
    df['month'] = pd.to_datetime(df['month'], format='%b %Y') # Adjust format if necessary
    
    months = get_all_months(df)
    return dcc.Dropdown(
        id='month-selector',
        options=[{'label': m, 'value': m} for m in months],
        value=get_latest_month(df),
        clearable=False
    )