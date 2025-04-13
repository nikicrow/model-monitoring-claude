import pandas as pd
import numpy as np
import datetime

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
    
    # Generate time series feature importance and drift data
    feature_importance_ts = []
    feature_drift_ts = []
    
    for date in dates:
        # Base importance values with some random variation
        month_importance = [
            max(0.01, v * (1 + np.random.uniform(-0.1, 0.1))) 
            for v in [0.23, 0.18, 0.15, 0.12, 0.09, 0.08, 0.06, 0.04, 0.03, 0.02]
        ]
        # Normalize to sum to 1
        month_importance = np.array(month_importance) / sum(month_importance)
        
        for feat, imp in zip(features, month_importance):
            feature_importance_ts.append({
                'date': date,
                'month': date.strftime('%b %Y'),
                'Feature': feat,
                'Importance': imp
            })
            
            # Generate drift metrics
            csi = np.random.uniform(0.05, 0.3)
            feature_drift_ts.append({
                'date': date,
                'month': date.strftime('%b %Y'),
                'Feature': feat,
                'CSI': csi,
                'Status': 'Warning' if csi > 0.2 else 'Stable'
            })
    
    feature_importance = pd.DataFrame(feature_importance_ts)
    feature_drift = pd.DataFrame(feature_drift_ts)
    
    # Sort latest month by importance
    latest_importance = feature_importance[feature_importance['date'] == dates[-1]]
    feature_importance = feature_importance.sort_values(['date', 'Importance'], ascending=[True, False])
    feature_drift = feature_drift.sort_values(['date', 'CSI'], ascending=[True, False])
    
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
