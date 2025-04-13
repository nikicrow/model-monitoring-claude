import pandas as pd
import numpy as np
import plotly.express as px

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from data.mock_data import create_mock_data
from layout.section1_stability import section1_stability_analysis
from layout.section2_conversions import section2_conversion_analysis
from layout.section3_offline import section3_offline_metrics
from layout.section4_features import section4_feature_analysis
from callbacks.section1_callbacks import register_callbacks_section1
from callbacks.section2_callbacks import register_callbacks_section2
from callbacks.section3_callbacks import register_callbacks_section3
from callbacks.section4_callbacks import register_callbacks_section4
from utils.filters import get_latest_month, get_all_months

# Set random seed for reproducibility
np.random.seed(42)

# Generate mock data
df, feature_importance, feature_drift, roc_data, prc_data, cum_metrics_df = create_mock_data()

# Add month selector component
def create_month_selector(df):
    months = get_all_months(df)
    return dcc.Dropdown(
        id='month-selector',
        options=[{'label': m, 'value': m} for m in months],
        value=get_latest_month(df),
        clearable=False
    )

# Create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Propensity Model Monitoring Dashboard", className="text-center my-4"),
            html.P("This dashboard provides insights into the performance and stability of our customer propensity model. Designed for business users, it offers a comprehensive view of model performance, stability, and accuracy.", className="lead text-center mb-5")
        ])
    ]),
    
    # Month Selector
    dbc.Row([
        dbc.Col([
            create_month_selector(df),
            html.P("Choose the month above that you would like to look at.", className="lead text-center mb-5")
        ])
    ]),

    # Section 1: Model Scoring Pipeline Stability
    section1_stability_analysis(),

    # Section 2: Actual Conversion Rates
    section2_conversion_analysis(),

    # Section 3: Model Accuracy
    section3_offline_metrics(),

    # Section 4: Feature Importance and Drift
    section4_feature_analysis(),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("Propensity Model Monitoring Dashboard • Data as of April 4, 2025", className="text-center text-muted"),
        ])
    ]),
], fluid=True)

# Register callbacks - pass month selector as a parameter
register_callbacks_section1(app, df)
register_callbacks_section2(app, df)
register_callbacks_section3(app, roc_data, prc_data, cum_metrics_df)
register_callbacks_section4(app, feature_importance, feature_drift)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)