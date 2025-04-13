from dash import dcc, html
import dash_bootstrap_components as dbc


def section2_conversion_analysis():
    """
    Section 2: Conversion Analysis
    ------------------------------
    This section provides an overview of the conversion rates for different customer segments.
    It includes scorecards for high, medium, and low probability customers,
    along with charts showing conversion rates over time.
    It helps assess the effectiveness of the model in predicting customer conversions.

    """
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2("2. Actual Conversion Rates for Past Model Scores", className="mb-3"),
                html.P("This section shows how well our model predictions translated to actual customer conversions. We look at data from previous months to see if customers in high probability segments actually converted at higher rates than those in lower segments.", className="mb-4"),
                html.P("Note: This section only includes data up to March 3rd, 2025, as we need time to observe conversions.", className="mb-4 font-italic")
            ])
        ]),
        
        # Conversion rate scorecards
        dbc.Row([
            # High bucket conversion rate
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("High Bucket Conversion Rate", className="card-title"),
                        html.Div([
                            html.H3("7.0%", className="card-text text-center d-inline-block me-2"),
                            html.Span([
                                html.I(className="fas fa-arrow-up text-success"),
                                " +0.5%"
                            ], className="text-success")
                        ], className="text-center my-3")
                    ])
                ], className="mb-4")
            ], width=4),
            
            # Medium bucket conversion rate
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Medium Bucket Conversion Rate", className="card-title"),
                        html.Div([
                            html.H3("4.0%", className="card-text text-center d-inline-block me-2"),
                            html.Span([
                                html.I(className="fas fa-arrow-up text-success"),
                                " +0.3%"
                            ], className="text-success")
                        ], className="text-center my-3")
                    ])
                ], className="mb-4")
            ], width=4),
            
            # Low bucket conversion rate
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Low Bucket Conversion Rate", className="card-title"),
                        html.Div([
                            html.H3("1.5%", className="card-text text-center d-inline-block me-2"),
                            html.Span([
                                html.I(className="fas fa-arrow-down text-danger"),
                                " -0.1%"
                            ], className="text-danger")
                        ], className="text-center my-3")
                    ])
                ], className="mb-4")
            ], width=4),
        ]),
        
        # Charts for Section 2
        
        dbc.Row([
            # Bar and line chart for conversions by decile
            dbc.Col([
                dcc.Graph(
                    id='decile-conversion-chart',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'decile_conversion_chart'}}
                )
            ], width=12, className="mb-4"),
        ]),
        
        dbc.Row([
            # Stacked bar chart for conversions by decile over time
            dbc.Col([
                dcc.Graph(
                    id='stacked-decile-conversion-chart',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'stacked_decile_conversion_chart'}}
                )
            ], width=12, className="mb-4"),
        ]),
        
        dbc.Row([
            # Total conversions over time
            dbc.Col([
                dcc.Graph(
                    id='total-conversions-chart',
                    config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'total_conversions_chart'}}
                )
            ], width=12, className="mb-4"),
        ]),
    ])