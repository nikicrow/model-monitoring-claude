from dash import dcc, html
import dash_bootstrap_components as dbc


def section1_stability_analysis():
    """
    Section 1: Stability Analysis
    ------------------------------
    This section provides an overview of the stability of the model scoring pipeline.
    It includes the number of customers scored, their distribution across risk categories,
    and the last model run date.
    It also includes charts showing the total number of customers over time,
    the distribution of customers by bucket, and the decile distribution of customers.

    """
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2("1. Model Scoring Pipeline Stability", className="mb-3"),
                html.P("This section shows the stability of our model scoring pipeline, including the number of customers scored and their distribution across risk categories. This helps ensure our model is processing data consistently month over month.", className="mb-4")
            ])
        ]),
        
        # Scorecards
        dbc.Row([
            # Last model run date
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Last Model Run Date", className="card-title"),
                        html.H3("April 4, 2025", className="card-text text-center my-3"),
                    ])
                ], className="mb-4")
            ], width=4),
            
            # Number of customers scored
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Customers Scored", className="card-title"),
                        html.Div([
                            html.H3("2.58M", className="card-text text-center d-inline-block me-2"),
                            html.Span([
                                html.I(className="fas fa-arrow-up text-success"),
                                " +3%"
                            ], className="text-success")
                        ], className="text-center my-3")
                    ])
                ], className="mb-4")
            ], width=4),

        ]),
        
        dbc.Row([
            # High probability customers
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("High Probability Customers", className="card-title"),
                        html.Div([
                            html.H3("25%", className="card-text text-center d-inline-block me-2"),
                            html.Span([
                                html.I(className="fas fa-arrow-up text-success"),
                                " +2%"
                            ], className="text-success")
                        ], className="text-center my-3")
                    ])
                ], className="mb-4")
            ], width=4),
            # Medium probability customers
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Medium Probability Customers", className="card-title"),
                        html.Div([
                            html.H3("35%", className="card-text text-center d-inline-block me-2"),
                            html.Span([
                                html.I(className="fas fa-arrow-down text-danger"),
                                " -1%"
                            ], className="text-danger")
                        ], className="text-center my-3")
                    ])
                ], className="mb-4")
            ], width=4),
            
            # Low probability customers
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Low Probability Customers", className="card-title"),
                        html.Div([
                            html.H3("40%", className="card-text text-center d-inline-block me-2"),
                            html.Span([
                                html.I(className="fas fa-arrow-down text-danger"),
                                " -1%"
                            ], className="text-danger")
                        ], className="text-center my-3")
                    ])
                ], className="mb-4")
            ], width=4),
            
            # Empty column for balance
            dbc.Col(width=4),
        ]),
        
        # Charts for Section 1
        dbc.Row([
            # Total customers over time
            dbc.Col([
                dcc.Graph(
                    id='total-customers-chart',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'total_customers_chart'}}
                )
            ], width=12, className="mb-4"),
        ]),
        
        dbc.Row([
            # Stacked bar chart of customers by bucket
            dbc.Col([
                dcc.Graph(
                    id='stacked-customers-chart',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'stacked_customers_chart'}}
                )
            ], width=12, className="mb-4"),
        ]),
        
        dbc.Row([
            # Bar chart of customers by decile and bucket
            dbc.Col([
                dcc.Graph(
                    id='decile-distribution-chart',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'decile_distribution_chart'}}
                )
            ], width=12, className="mb-4"),
        ]),
    ])