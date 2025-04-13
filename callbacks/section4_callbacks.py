from dash.dependencies import Input, Output
from utils.filters import filter_by_month
import plotly.express as px
from dash import html
import pandas as pd

def register_callbacks_section4(app, feature_importance, feature_drift):
    @app.callback(
        [Output('feature-importance-chart', 'figure'),
         Output('feature-drift-table', 'data')],
        [Input('month-selector', 'value')]
    )
    def update_feature_analysis(selected_month):
        print(selected_month)
        # Filter data for selected month
        monthly_feature_importance = filter_by_month(feature_importance, selected_month)
        monthly_feature_drift = filter_by_month(feature_drift, selected_month)
        print(monthly_feature_importance)
        # Generate feature importance visualization
        importance_fig = px.bar(
            monthly_feature_importance.sort_values('Importance', ascending=True),
            y='Feature',
            x='Importance',
            orientation='h',
            title='Feature Importance'
        )
        
        # Prepare drift table data
        drift_table_data = monthly_feature_drift.sort_values('CSI', ascending=False).to_dict('records')
        
        return importance_fig, drift_table_data