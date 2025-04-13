from dash.dependencies import Input, Output
from utils.filters import filter_by_month
import plotly.express as px
import pandas as pd

def register_callbacks_section1(app, df):
    # Total customers over time
    @app.callback(
        Output('total-customers-chart', 'figure'),
        Input('total-customers-chart', 'id')
    )
    def update_total_customers_chart(_):
        # Convert the 'month' column to datetime format
        df['month'] = pd.to_datetime(df['month'], format='%b %Y') # Adjust format if necessary
    
        monthly_totals = df.groupby('month')['customers'].sum().reset_index().sort_values('month')
        
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
        [Input('month-selector', 'value')]
    )
    def update_decile_distribution(selected_month):
        filtered_df = filter_by_month(df, selected_month)
        fig = px.bar(filtered_df, 
                    x='decile', 
                    y='customers',
                    color='bucket',
                    title='Customer Distribution by Decile')
        return fig
