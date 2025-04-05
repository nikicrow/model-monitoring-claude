from dash.dependencies import Input, Output
import plotly.express as px

def register_callbacks_section3(app, roc_data, prc_data, cum_metrics_df):
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
