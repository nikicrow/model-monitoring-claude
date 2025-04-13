from dash.dependencies import Input, Output
from utils.filters import filter_by_month
import plotly.express as px

def register_callbacks_section3(app, roc_data, prc_data, cum_metrics_df):
    @app.callback(
        [Output('roc-curve', 'figure'),
         Output('prc-curve', 'figure'),
         Output('cumulative-recall-chart', 'figure'),
         Output('cumulative-precision-chart', 'figure')],
        [Input('month-selector', 'value')]
    )
    def update_model_metrics(selected_month):
        # ROC curve
        roc_fig = px.line(roc_data,
                         x='FPR',
                         y='TPR',
                         title='ROC Curve')
        
        # PRC curve
        prc_fig = px.line(prc_data,
                         x='Recall',
                         y='Precision',
                         title='Precision-Recall Curve')
        
        # Cumulative metrics
        cum_recall = px.line(cum_metrics_df,
                            x='Decile',
                            y='Cumulative Recall',
                            title='Cumulative Recall by Decile')
        
        cum_prec = px.line(cum_metrics_df,
                          x='Decile',
                          y='Cumulative Precision',
                          title='Cumulative Precision by Decile')
        
        return roc_fig, prc_fig, cum_recall, cum_prec
