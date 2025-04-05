from dash import dcc, html
import dash_bootstrap_components as dbc


def section3_offline_metrics():
    """
    Section 3: Model Accuracy - Data Science Metrics
    ------------------------------

    """
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2("3. Model Accuracy - Data Science Metrics", className="mb-3"),
                html.P("This section provides technical metrics that help assess the model's accuracy and performance. These metrics are standard in the data science community and help us understand how well our model discriminates between customers who will convert and those who won't.", className="mb-4")
            ])
        ]),
        
        # ROC and PRC curves
        dbc.Row([
            # ROC curve
            dbc.Col([
                dcc.Graph(
                    id='roc-curve',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'roc_curve'}}
                )
            ], width=6, className="mb-4"),
            
            # PRC curve
            dbc.Col([
                dcc.Graph(
                    id='prc-curve',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'prc_curve'}}
                )
            ], width=6, className="mb-4"),
        ]),
        
        # Cumulative metrics
        dbc.Row([
            # Cumulative recall by decile
            dbc.Col([
                dcc.Graph(
                    id='cumulative-recall-chart',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'cumulative_recall_chart'}}
                )
            ], width=6, className="mb-4"),
            
            # Cumulative precision by decile
            dbc.Col([
                dcc.Graph(
                    id='cumulative-precision-chart',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'cumulative_precision_chart'}}
                )
            ], width=6, className="mb-4"),
        ]),
        
    ])