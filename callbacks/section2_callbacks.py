from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from utils.filters import filter_by_month

def register_callbacks_section2(app, df):
    
    @app.callback(
        Output('decile-conversion-chart', 'figure'),
        [Input('month-selector', 'value')]
    )
    def update_decile_conversion(selected_month):
        filtered_df = filter_by_month(df, selected_month)
        
        # Group by decile
        decile_conversion = filtered_df.groupby('decile').agg(
            customers=('customers', 'sum'),
            conversions=('conversions', 'sum')
        ).reset_index()
        
        decile_conversion['conversion_rate'] = (decile_conversion['conversions'] / 
                                              decile_conversion['customers'] * 100)
        
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
            title_text=f'Conversions and Conversion Rate by Decile ({selected_month})',
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
