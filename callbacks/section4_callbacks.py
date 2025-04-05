from dash.dependencies import Input, Output
import plotly.express as px
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

def register_callbacks_section4(app, feature_importance, feature_drift):
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