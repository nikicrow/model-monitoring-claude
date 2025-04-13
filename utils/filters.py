import pandas as pd

def filter_by_month(df, selected_month):
    """Filter dataframe by selected month."""
    return df[df['month'] == selected_month]

def get_latest_month(df):
    """Get the most recent month from the data."""
    return df['month'].max()

def get_all_months(df):
    """Get sorted list of all months in the data."""
    return sorted(df['month'].unique())
