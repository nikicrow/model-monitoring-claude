import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import datetime

# Set random seed for reproducibility
np.random.seed(42)

# Create mock data
def create_mock_data():
    # Create date range for the last 6 months
    today = datetime.datetime(2025, 4, 5)
    dates = [(today - datetime.timedelta(days=30*i)).replace(day=4) for i in range(6)]
    dates.reverse()  # Oldest to newest
    
    # Total customers per month (around 2.5 million)
    base_customers = 2500000
    customer_counts = [
        base_customers + np.random.randint(-50000, 50000) for _ in range(6)
    ]
    
    # Create distribution across deciles (1-10)
    deciles = list(range(1, 11))
    
    # Monthly data
    monthly_data = []
    
    for month_idx, date in enumerate(dates):
        # Calculate total customers for this month
        total_customers = customer_counts[month_idx]
        
        # Generate decile distribution
        # Deciles have 10% each duh
        decile_weights = np.array([0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10])
        customers_per_decile = np.round(decile_weights * total_customers).astype(int)
        
        # Adjust to match total
        customers_per_decile[-1] += (total_customers - customers_per_decile.sum())
        
        # Conversion rates per decile (higher deciles have higher conversion rates)
        conversion_rates = np.array([0.005, 0.008, 0.012, 0.016, 0.02, 0.025, 0.035, 0.045, 0.07, 0.1])
        
        # Add slight randomness to conversion rates
        if month_idx > 0:  # Keep different for each month except the first
            conversion_rates = conversion_rates * (1 + np.random.uniform(-0.1, 0.1, size=10))
        
        # Calculate conversions per decile
        conversions_per_decile = np.round(customers_per_decile * conversion_rates).astype(int)
        
        # Create bucket mapping (Low: 1-4 and some of 5, Medium: some of 5 and 6-7 and some of 8, High: rest)
        bucket_mapping = {
            1: 'Low', 2: 'Low', 3: 'Low', 4: 'Low',
            5: 'Low',  # Will split this later
            6: 'Medium', 7: 'Medium',
            8: 'Medium',  # Will split this later
            9: 'High', 10: 'High'
        }
        
        # Create month data
        for decile in deciles:
            # Split decile 5 (80% Low, 20% Medium)
            if decile == 5:
                low_count = int(customers_per_decile[decile-1] * 0.8)
                med_count = customers_per_decile[decile-1] - low_count
                
                # Low portion
                monthly_data.append({
                    'date': date,
                    'month': date.strftime('%b %Y'),
                    'decile': decile,
                    'bucket': 'Low',
                    'customers': low_count,
                    'conversions': int(conversions_per_decile[decile-1] * 0.8)
                })
                
                # Medium portion
                monthly_data.append({
                    'date': date,
                    'month': date.strftime('%b %Y'),
                    'decile': decile,
                    'bucket': 'Medium',
                    'customers': med_count,
                    'conversions': int(conversions_per_decile[decile-1] * 0.2)
                })
            
            # Split decile 8 (30% Medium, 70% High)
            elif decile == 8:
                med_count = int(customers_per_decile[decile-1] * 0.3)
                high_count = customers_per_decile[decile-1] - med_count
                
                # Medium portion
                monthly_data.append({
                    'date': date,
                    'month': date.strftime('%b %Y'),
                    'decile': decile,
                    'bucket': 'Medium',
                    'customers': med_count,
                    'conversions': int(conversions_per_decile[decile-1] * 0.3)
                })
                
                # High portion
                monthly_data.append({
                    'date': date,
                    'month': date.strftime('%b %Y'),
                    'decile': decile,
                    'bucket': 'High',
                    'customers': high_count,
                    'conversions': int(conversions_per_decile[decile-1] * 0.7)
                })
            
            else:
                monthly_data.append({
                    'date': date,
                    'month': date.strftime('%b %Y'),
                    'decile': decile,
                    'bucket': bucket_mapping[decile],
                    'customers': customers_per_decile[decile-1],
                    'conversions': conversions_per_decile[decile-1]
                })
    
    # Convert to DataFrame
    df = pd.DataFrame(monthly_data)
    
    # Feature importance and drift data
    features = [
        'Magic Level', 'Horn Toughness', 'Avg Poop Weight', 
        'Number of Legs', 'Sparkle Factor', 'Rainbow Intensity',
        'Mane Length', 'Happiness Index', 'Cupcake Consumption', 
        'Friendship Power'
    ]
    
    importance_values = [0.23, 0.18, 0.15, 0.12, 0.09, 0.08, 0.06, 0.04, 0.03, 0.02]
    
    feature_importance = pd.DataFrame({
        'Feature': features,
        'Importance': importance_values
    })
    
    # Create feature drift data
    feature_drift = pd.DataFrame({
        'Feature': features,
        'CSI': np.random.uniform(0.05, 0.3, size=len(features)),
        'Status': ['Stable'] * len(features)
    })
    
    # Assign warning status for CSI > 0.2
    feature_drift.loc[feature_drift['CSI'] > 0.2, 'Status'] = 'Warning'
    
    # Sort by importance
    feature_drift = feature_drift.sort_values('CSI', ascending=False)
    
    # Create ROC and PRC curve data
    roc_x = np.linspace(0, 1, 100)
    # Curve shape for 0.7 AUROC
    roc_y = np.power(roc_x, 0.3)
    
    prc_x = np.linspace(0, 1, 100)
    # For imbalanced dataset (starting at high precision, low recall)
    prc_y = np.maximum(0.1 * (1 - np.exp(-5 * prc_x)), 0.01)
    
    roc_data = pd.DataFrame({'FPR': roc_x, 'TPR': roc_y})
    prc_data = pd.DataFrame({'Recall': prc_x, 'Precision': prc_y})
    
    # Cumulative recall and precision by decile
    cum_metrics = []
    
    recall_by_decile = [0.3, 0.45, 0.57, 0.67, 0.75, 0.82, 0.88, 0.93, 0.97, 1.0]
    precision_by_decile = [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]
    
    for i, decile in enumerate(range(1, 11)):
        cum_metrics.append({
            'Decile': decile,
            'Cumulative Recall': recall_by_decile[i],
            'Cumulative Precision': precision_by_decile[i]
        })
    
    cum_metrics_df = pd.DataFrame(cum_metrics)
    
    return df, feature_importance, feature_drift, roc_data, prc_data, cum_metrics_df

# Generate mock data
df, feature_importance, feature_drift, roc_data, prc_data, cum_metrics_df = create_mock_data()

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
    
    # Section 1: Model Scoring Pipeline Stability
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
    
    # Section 2: Actual Conversion Rates
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
        # Line chart of conversion rates by bucket over time
        dbc.Col([
            dcc.Graph(
                id='conversion-rates-chart',
                config={'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'conversion_rates_chart'}}
            )
        ], width=12, className="mb-4"),
    ]),
    
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
    
    # Section 3: Model Accuracy
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
    
    # Section 4: Feature Importance and Drift
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
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("Propensity Model Monitoring Dashboard • Data as of April 4, 2025", className="text-center text-muted"),
        ])
    ]),
], fluid=True)

# Callbacks to update charts

# Total customers over time
@app.callback(
    Output('total-customers-chart', 'figure'),
    Input('total-customers-chart', 'id')
)
def update_total_customers_chart(_):
    monthly_totals = df.groupby('month')['customers'].sum().reset_index()
    
    fig = px.bar(
        monthly_totals, 
        x='month', 
        y='customers',
        title='Total Customers Scored (Last 6 Months)',
        labels={'month': 'Month', 'customers': 'Number of Customers'},
        text_auto='.2s'
    )
    
    fig.update_traces(
        marker_color='royalblue',
        textposition='outside'
    )
    
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Customers',
        yaxis_tickformat=',',
        plot_bgcolor='white',
        height=500
    )
    
    return fig

# Stacked bar chart of customers by bucket
@app.callback(
    Output('stacked-customers-chart', 'figure'),
    Input('stacked-customers-chart', 'id')
)
def update_stacked_customers_chart(_):
    bucket_totals = df.groupby(['month', 'bucket'])['customers'].sum().reset_index()
    
    # Define a specific order for the buckets
    bucket_order = ['High', 'Medium', 'Low']
    bucket_totals['bucket'] = pd.Categorical(bucket_totals['bucket'], categories=bucket_order, ordered=True)
    bucket_totals = bucket_totals.sort_values(['month', 'bucket'])
    
    # Define colors for the buckets
    color_map = {'High': '#2ca02c', 'Medium': '#ffbb78', 'Low': '#ff7f0e'}
    
    fig = px.bar(
        bucket_totals, 
        x='month', 
        y='customers',
        color='bucket',
        color_discrete_map=color_map,
        title='Customer Distribution by Probability Bucket (Last 6 Months)',
        labels={'month': 'Month', 'customers': 'Number of Customers', 'bucket': 'Probability Bucket'},
        text_auto='.2s'
    )
    
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Customers',
        yaxis_tickformat=',',
        plot_bgcolor='white',
        legend_title="Probability Bucket",
        height=500
    )
    
    return fig

# Bar chart of customers by decile and bucket
@app.callback(
    Output('decile-distribution-chart', 'figure'),
    Input('decile-distribution-chart', 'id')
)
def update_decile_distribution_chart(_):
    # Get the most recent month's data
    latest_month = df['month'].unique()[-1]
    latest_data = df[df['month'] == latest_month]
    
    # Group by decile and bucket
    decile_bucket = latest_data.groupby(['decile', 'bucket'])['customers'].sum().reset_index()
    
    # Define colors for the buckets
    color_map = {'High': '#2ca02c', 'Medium': '#ffbb78', 'Low': '#ff7f0e'}
    
    fig = px.bar(
        decile_bucket, 
        x='decile', 
        y='customers',
        color='bucket',
        color_discrete_map=color_map,
        title='Current Month Distribution of Customers by Decile and Probability Bucket',
        labels={'decile': 'Decile', 'customers': 'Number of Customers', 'bucket': 'Probability Bucket'},
        text_auto='.2s'
    )
    
    fig.update_layout(
        xaxis_title='Decile (1 = Lowest Propensity, 10 = Highest Propensity)',
        yaxis_title='Number of Customers',
        yaxis_tickformat=',',
        plot_bgcolor='white',
        legend_title="Probability Bucket",
        height=500
    )
    
    # Ensure x-axis shows all deciles
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=list(range(1, 11)))
    
    return fig

# Line chart of conversion rates by bucket over time
@app.callback(
    Output('conversion-rates-chart', 'figure'),
    Input('conversion-rates-chart', 'id')
)
def update_conversion_rates_chart(_):
    # Get data up to the second last month (to simulate having data only up to previous month)
    conversion_data = df[df['month'] != df['month'].unique()[-1]]
    
    # Calculate conversion rates by bucket and month
    bucket_conversion = conversion_data.groupby(['month', 'bucket']).agg(
        customers=('customers', 'sum'),
        conversions=('conversions', 'sum')
    ).reset_index()
    
    bucket_conversion['conversion_rate'] = bucket_conversion['conversions'] / bucket_conversion['customers'] * 100
    
    # Define colors for the buckets
    color_map = {'High': '#2ca02c', 'Medium': '#ffbb78', 'Low': '#ff7f0e'}
    
    fig = px.line(
        bucket_conversion, 
        x='month', 
        y='conversion_rate',
        color='bucket',
        color_discrete_map=color_map,
        title='Conversion Rates by Probability Bucket (Last 5 Months)',
        labels={'month': 'Month', 'conversion_rate': 'Conversion Rate (%)', 'bucket': 'Probability Bucket'},
        markers=True
    )
    
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )
    
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Conversion Rate (%)',
        plot_bgcolor='white',
        legend_title="Probability Bucket",
        height=500
    )
    
    return fig

# Bar and line chart for conversions by decile
@app.callback(
    Output('decile-conversion-chart', 'figure'),
    Input('decile-conversion-chart', 'id')
)
def update_decile_conversion_chart(_):
    # Get data from the second last month
    last_month = df['month'].unique()[-2]
    last_month_data = df[df['month'] == last_month]
    
    # Group by decile
    decile_conversion = last_month_data.groupby('decile').agg(
        customers=('customers', 'sum'),
        conversions=('conversions', 'sum')
    ).reset_index()
    
    decile_conversion['conversion_rate'] = decile_conversion['conversions'] / decile_conversion['customers'] * 100
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add bar chart for number of conversions
    fig.add_trace(
        go.Bar(
            x=decile_conversion['decile'],
            y=decile_conversion['conversions'],
            name='Conversions',
            marker_color='steelblue',
            opacity=0.7
        ),
        secondary_y=False
    )
    
    # Add line chart for conversion rate
    fig.add_trace(
        go.Scatter(
            x=decile_conversion['decile'],
            y=decile_conversion['conversion_rate'],
            name='Conversion Rate',
            marker=dict(size=10, color='darkred'),
            line=dict(width=3, color='darkred')
        ),
        secondary_y=True
    )
    
    # Set titles
    fig.update_layout(
        title_text='Conversions and Conversion Rate by Decile (Last Month)',
        xaxis_title='Decile (1 = Lowest Propensity, 10 = Highest Propensity)',
        plot_bgcolor='white',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Set y-axes titles
    fig.update_yaxes(title_text="Number of Conversions", secondary_y=False)
    fig.update_yaxes(title_text="Conversion Rate (%)", secondary_y=True)
    
    # Ensure x-axis shows all deciles
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=list(range(1, 11)))
    
    return fig

# Stacked bar chart for conversions by decile over time
@app.callback(
    Output('stacked-decile-conversion-chart', 'figure'),
    Input('stacked-decile-conversion-chart', 'id')
)
def update_stacked_decile_conversion_chart(_):
    # Get data up to the second last month
    conversion_data = df[df['month'] != df['month'].unique()[-1]]
    
    # Group by month and decile
    decile_month_conversion = conversion_data.groupby(['month', 'decile'])['conversions'].sum().reset_index()
    
    fig = px.bar(
        decile_month_conversion, 
        x='month', 
        y='conversions',
        color='decile',
        title='Conversions by Decile Over Time (Last 5 Months)',
        labels={'month': 'Month', 'conversions': 'Number of Conversions', 'decile': 'Decile'},
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Conversions',
        plot_bgcolor='white',
        legend_title="Decile",
        height=500
    )
    
    return fig

# Total conversions over time
@app.callback(
    Output('total-conversions-chart', 'figure'),
    Input('total-conversions-chart', 'id')
)
def update_total_conversions_chart(_):
    # Get data up to the second last month
    conversion_data = df[df['month'] != df['month'].unique()[-1]]
    
    # Group by month
    monthly_conversions = conversion_data.groupby('month')['conversions'].sum().reset_index()
    
    fig = px.line(
        monthly_conversions, 
        x='month', 
        y='conversions',
        title='Total Conversions Over Time (Last 5 Months)',
        labels={'month': 'Month', 'conversions': 'Number of Conversions'},
        markers=True
    )
    
    fig.update_traces(
        line=dict(width=3, color='royalblue'),
        marker=dict(size=10, color='royalblue')
    )
    
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Conversions',
        plot_bgcolor='white',
        height=500
    )
    
    return fig

# ROC curve
@app.callback(
    Output('roc-curve', 'figure'),
    Input('roc-curve', 'id')
)
def update_roc_curve(_):
    # Calculate AUC
    auc = 0.7
    
    fig = px.line(
        roc_data, 
        x='FPR', 
        y='TPR',
        title=f'ROC Curve (AUROC = {auc:.2f})',
        labels={'FPR': 'False Positive Rate', 'TPR': 'True Positive Rate'}
    )
    
    # Add diagonal reference line
    fig.add_shape(
        type='line',
        line=dict(dash='dash', color='gray'),
        x0=0, y0=0, x1=1, y1=1
    )
    
    fig.update_traces(
        line=dict(width=3, color='royalblue')
    )
    
    fig.update_layout(
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        xaxis=dict(constrain='domain'),
        yaxis=dict(scaleanchor="x", scaleratio=1),
        plot_bgcolor='white',
        height=500
    )
    
    return fig

# PRC curve
@app.callback(
    Output('prc-curve', 'figure'),
    Input('prc-curve', 'id')
)
def update_prc_curve(_):
    # Calculate area under precision-recall curve
    auprc = 0.25
    
    fig = px.line(
        prc_data, 
        x='Recall', 
        y='Precision',
        title=f'Precision-Recall Curve (AUPRC = {auprc:.2f})',
        labels={'Recall': 'Recall', 'Precision': 'Precision'}
    )
    
    # Add baseline (imbalanced datasets - baseline is the positive class proportion)
    baseline = 0.01  # 1% positive class
    fig.add_shape(
        type='line',
        line=dict(dash='dash', color='gray'),
        x0=0, y0=baseline, x1=1, y1=baseline
    )
    
    fig.update_traces(
        line=dict(width=3, color='darkgreen')
    )
    
    fig.update_layout(
        xaxis_title='Recall',
        yaxis_title='Precision',
        xaxis=dict(constrain='domain'),
        plot_bgcolor='white',
        height=500
    )
    
    return fig

# Cumulative recall by decile
@app.callback(
    Output('cumulative-recall-chart', 'figure'),
    Input('cumulative-recall-chart', 'id')
)
def update_cumulative_recall_chart(_):
    fig = px.line(
        cum_metrics_df, 
        x='Decile', 
        y='Cumulative Recall',
        title='Cumulative Recall by Decile',
        labels={'Decile': 'Decile', 'Cumulative Recall': 'Cumulative Recall'},
        markers=True
    )
    
    fig.update_traces(
        line=dict(width=3, color='darkblue'),
        marker=dict(size=10, color='darkblue')
    )
    
    fig.update_layout(
        xaxis_title='Decile (1 = Highest Propensity, 10 = Lowest Propensity)',
        yaxis_title='Cumulative Recall',
        xaxis=dict(tickmode='linear'),
        plot_bgcolor='white',
        height=500
    )
    
    return fig

# Cumulative precision by decile
@app.callback(
    Output('cumulative-precision-chart', 'figure'),
    Input('cumulative-precision-chart', 'id')
)
def update_cumulative_precision_chart(_):
    fig = px.line(
        cum_metrics_df, 
        x='Decile', 
        y='Cumulative Precision',
        title='Cumulative Precision by Decile',
        labels={'Decile': 'Decile', 'Cumulative Precision': 'Cumulative Precision'},
        markers=True
    )
    
    fig.update_traces(
        line=dict(width=3, color='darkred'),
        marker=dict(size=10, color='darkred')
    )
    
    fig.update_layout(
        xaxis_title='Decile (1 = Highest Propensity, 10 = Lowest Propensity)',
        yaxis_title='Cumulative Precision',
        xaxis=dict(tickmode='linear'),
        plot_bgcolor='white',
        height=500
    )
    
    return fig

# Feature importance chart
@app.callback(
    Output('feature-importance-chart', 'figure'),
    Input('feature-importance-chart', 'id')
)
def update_feature_importance_chart(_):
    # Sort by importance
    sorted_importance = feature_importance.sort_values('Importance', ascending=True)
    
    fig = px.bar(
        sorted_importance,
        y='Feature',
        x='Importance',
        orientation='h',
        title='Feature Importance',
        labels={'Feature': 'Feature', 'Importance': 'Importance (Gain)'}
    )
    
    fig.update_traces(marker_color='royalblue')
    
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis_title='Importance (Gain)',
        yaxis_title='Feature',
        plot_bgcolor='white',
        height=500
    )
    
    return fig

# Feature drift table
@app.callback(
    Output('feature-drift-table', 'children'),
    Input('feature-drift-table', 'id')
)
def update_feature_drift_table(_):
    # Sort by importance
    merged_data = pd.merge(feature_drift, feature_importance, on='Feature')
    sorted_drift = merged_data.sort_values('Importance', ascending=False)
    
    # Create styled table
    table = html.Table([
        html.Thead(
            html.Tr([
                html.Th('Feature', className='p-2'),
                html.Th('Importance', className='p-2 text-center'),
                html.Th('CSI', className='p-2 text-center'),
                html.Th('Status', className='p-2 text-center')
            ], className='border-bottom')
        ),
        html.Tbody([
            html.Tr([
                html.Td(row['Feature'], className='p-2'),
                html.Td(f"{row['Importance']:.3f}", className='p-2 text-center'),
                html.Td(f"{row['CSI']:.3f}", className='p-2 text-center'),
                html.Td(
                    row['Status'], 
                    className=f"p-2 text-center {'text-warning' if row['Status'] == 'Warning' else ''}"
                )
            ], className='border-bottom') for _, row in sorted_drift.iterrows()
        ])
    ], className='table table-hover table-bordered')
    
    return table

# Run the app
if __name__ == '__main__':
    app.run(debug=True)