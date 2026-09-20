"""
Statistics Module
Calculates descriptive statistics for demand analysis
"""

import pandas as pd
import numpy as np
from scipy import stats

def calculate_statistics(df, food_item):
    """
    Calculate comprehensive statistics for a specific food item
    
    Parameters:
    df: DataFrame with food data
    food_item: Name of the food item to analyze
    
    Returns:
    dict: Dictionary containing all statistics
    """
    
    # Filter data for the food item
    item_data = df[df['Item'] == food_item]['Actual_Demand'].values
    
    if len(item_data) == 0:
        return None
    
    # Calculate statistics
    stats_dict = {
        'item': food_item,
        'count': len(item_data),
        'mean': np.mean(item_data),
        'median': np.median(item_data),
        'mode': stats.mode(item_data, keepdims=True).mode[0] if len(item_data) > 0 else 0,
        'min': np.min(item_data),
        'max': np.max(item_data),
        'range': np.max(item_data) - np.min(item_data),
        'variance': np.var(item_data),
        'std_dev': np.std(item_data),
        'q1': np.percentile(item_data, 25),
        'q3': np.percentile(item_data, 75),
        'iqr': np.percentile(item_data, 75) - np.percentile(item_data, 25),
        'skewness': stats.skew(item_data),
        'kurtosis': stats.kurtosis(item_data)
    }
    
    return stats_dict

def get_insight_text(stats_dict):
    """
    Generate a natural language insight based on statistics
    
    Parameters:
    stats_dict: Dictionary of statistics
    
    Returns:
    str: Formatted insight text
    """
    
    item = stats_dict['item']
    mean = stats_dict['mean']
    std = stats_dict['std_dev']
    min_val = stats_dict['min']
    max_val = stats_dict['max']
    
    # Interpretation
    if std < mean * 0.1:
        variation = "very stable"
    elif std < mean * 0.2:
        variation = "stable"
    elif std < mean * 0.3:
        variation = "moderate variation"
    else:
        variation = "high variation"
    
    insight = f"""
    **Average {item} demand:** {mean:.0f} units/day
    
    **Stability:** The standard deviation of {std:.1f} indicates {variation} in daily demand.
    
    **Range:** Demand varies from {min_val} to {max_val} units, a range of {max_val - min_val} units.
    
    **Consistency:** With a coefficient of variation of {(std/mean)*100:.1f}%, this item's demand is {'highly predictable' if std/mean < 0.15 else 'moderately predictable' if std/mean < 0.25 else 'difficult to predict'}.
    """
    
    return insight

def get_all_items_summary(df):
    """
    Get summary statistics for all food items
    
    Parameters:
    df: DataFrame with food data
    
    Returns:
    DataFrame: Summary statistics for all items
    """
    
    items = df['Item'].unique()
    summary_data = []
    
    for item in items:
        item_data = df[df['Item'] == item]
        summary_data.append({
            'Food Item': item,
            'Avg Demand': item_data['Actual_Demand'].mean(),
            'Median Demand': item_data['Actual_Demand'].median(),
            'Std Dev': item_data['Actual_Demand'].std(),
            'Avg Waste %': item_data['Waste_Percentage'].mean(),
            'Avg Price': item_data['Price'].mean(),
            'Total Records': len(item_data)
        })
    
    summary_df = pd.DataFrame(summary_data)
    return summary_df.sort_values('Avg Demand', ascending=False)
