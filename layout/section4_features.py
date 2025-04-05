from dash import dcc, html
import dash_bootstrap_components as dbc


def section4_feature_analysis():
    """
    Section 3: Model Accuracy - Data Science Metrics
    ------------------------------

    """
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2("4. Feature Importance and Feature Drift", className="mb-3"),
                html.P("This section highlights which features are most important for our model's predictions and monitors if these features are stable over time. Feature drift can indicate changing customer behavior or data quality issues that might affect model performance.", className="mb-4")
            ])
        ]),
        
        # Feature importance chart
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='feature-importance-chart',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'feature_importance_chart'}}
                )
            ], width=12, className="mb-4"),
        ]),
        
        # Feature drift table
        dbc.Row([
            dbc.Col([
                html.H4("Feature Drift Analysis", className="mb-3"),
                html.P("Measured using Characteristic Stability Index (CSI). Lower values indicate more stable features.", className="mb-2"),
                html.Div(id='feature-drift-table')
            ], width=12, className="mb-4"),
        ]),
    ])