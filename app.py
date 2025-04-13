import pandas as pd
import numpy as np
import plotly.express as px

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from data.mock_data import create_mock_data, create_mock_feature_data
from layout.section1_stability import section1_stability_analysis
from layout.section2_conversions import section2_conversion_analysis
from layout.section3_offline import section3_offline_metrics
from layout.section4_features import section4_feature_analysis
from callbacks.section1_callbacks import register_callbacks_section1
from callbacks.section2_callbacks import register_callbacks_section2
from callbacks.section3_callbacks import register_callbacks_section3
from callbacks.section4_callbacks import register_callbacks_section4
from components.month_selector import create_month_selector

# Set random seed for reproducibility
np.random.seed(42)

# Generate mock data
df, roc_data, prc_data, cum_metrics_df = create_mock_data()
feature_importance, feature_drift = create_mock_feature_data()

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
    
    # Navigation
    dbc.Row([
        dbc.Col([
            html.H4("Jump to Section:", className="text-center mb-3"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("Model Scoring Pipeline Stability", href="#section1", external_link=True),
                    dbc.ListGroupItem("Actual Conversion Rates", href="#section2", external_link=True),
                    dbc.ListGroupItem("Model Accuracy", href="#section3", external_link=True),
                    dbc.ListGroupItem("Feature Importance and Drift", href="#section4", external_link=True),
                ],
                horizontal=True,
                className="justify-content-center mb-4"
            )
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
    html.Div(section1_stability_analysis(), id="section1"),

    # Section 2: Actual Conversion Rates
    html.Div(section2_conversion_analysis(), id="section2"),

    # Section 3: Model Accuracy
    html.Div(section3_offline_metrics(), id="section3"),

    # Section 4: Feature Importance and Drift
    html.Div(section4_feature_analysis(), id="section4"),
    
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