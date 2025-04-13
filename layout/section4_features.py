from dash import dcc, html, dash_table
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
                dash_table.DataTable(
                    id='feature-drift-table',
                    columns=[
                        {'name': 'Feature', 'id': 'Feature'},
                        {'name': 'CSI', 'id': 'CSI'},
                        {'name': 'Status', 'id': 'Status'}
                    ],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left'},
                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{Status} = "Warning"'},
                            'backgroundColor': '#ffeb9c',
                            'color': '#9c6500'
                        }
                    ]
                )
            ], width=12, className="mb-4"),
        ]),
    ])