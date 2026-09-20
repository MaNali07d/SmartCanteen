"""
Correlation Module
Analyzes relationships between variables and demand
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

def calculate_correlation(df, food_item, variable):
    """
    Calculate correlation between a variable and demand
    
    Parameters:
    df: DataFrame with food data
    food_item: Name of the food item
    variable: Name of the variable to correlate (e.g., 'Students_Present', 'Temperature_C', 'Price')
    
    Returns:
    dict: Dictionary with correlation results
    """
    
    # Filter data for the food item
    item_df = df[df['Item'] == food_item].copy()
    
    if len(item_df) < 2:
        return None
    
    # Get the two variables
    x = item_df[variable].values
    y = item_df['Actual_Demand'].values
    
    # Calculate Pearson correlation
    pearson_corr, pearson_pval = pearsonr(x, y)
    
    # Calculate Spearman correlation (rank-based)
    spearman_corr, spearman_pval = spearmanr(x, y)
    
    # Calculate R-squared
    r_squared = pearson_corr ** 2
    
    result = {
        'item': food_item,
        'variable': variable,
        'pearson_r': pearson_corr,
        'pearson_pval': pearson_pval,
        'spearman_r': spearman_corr,
        'spearman_pval': spearman_pval,
        'r_squared': r_squared,
        'correlation_strength': interpret_correlation(pearson_corr),
        'n': len(item_df)
    }
    
    return result

def interpret_correlation(r):
    """
    Interpret correlation coefficient strength
    
    Parameters:
    r: Correlation coefficient value
    
    Returns:
    str: Interpretation of correlation strength
    """
    
    abs_r = abs(r)
    
    if abs_r >= 0.7:
        strength = "Strong"
    elif abs_r >= 0.5:
        strength = "Moderate"
    elif abs_r >= 0.3:
        strength = "Weak"
    else:
        strength = "Very Weak/Negligible"
    
    direction = "Positive" if r > 0 else "Negative" if r < 0 else "Neutral"
    
    return f"{strength} {direction}" if r != 0 else "No Correlation"

def get_correlation_insight(result):
    """
    Generate insight text for correlation result
    
    Parameters:
    result: Dictionary with correlation calculation results
    
    Returns:
    str: Formatted insight text
    """
    
    item = result['item']
    var = result['variable']
    r = result['pearson_r']
    r_sq = result['r_squared']
    strength = result['correlation_strength']
    
    var_labels = {
        'Students_Present': 'Student Attendance',
        'Temperature_C': 'Temperature',
        'Price': 'Price'
    }
    
    var_label = var_labels.get(var, var)
    
    insight = f"""
    **{var_label} vs {item} Demand**
    
    **Correlation Coefficient (Pearson r):** {r:.3f}
    
    **Correlation Strength:** {strength}
    
    **R² Value:** {r_sq:.3f} ({r_sq*100:.1f}%)
    
    **Interpretation:** {r_sq*100:.1f}% of the variation in {item} demand can be explained by changes in {var_label}.
    
    **Important:** Correlation indicates association, not causation. Other factors may influence both variables.
    """
    
    return insight

def get_correlation_matrix(df, food_item=None):
    """
    Get correlation matrix for all relevant variables
    
    Parameters:
    df: DataFrame with food data
    food_item: Optional - specific food item (default: all items)
    
    Returns:
    DataFrame: Correlation matrix
    """
    
    if food_item:
        analysis_df = df[df['Item'] == food_item].copy()
    else:
        analysis_df = df.copy()
    
    # Select numeric columns for correlation
    numeric_cols = ['Students_Present', 'Temperature_C', 'Price', 'Actual_Demand', 'Waste_Percentage']
    
    # Create correlation matrix
    corr_matrix = analysis_df[numeric_cols].corr()
    
    return corr_matrix

def get_all_items_correlations(df):
    """
    Calculate key correlations for all food items
    
    Parameters:
    df: DataFrame with food data
    
    Returns:
    DataFrame: Summary of key correlations
    """
    
    items = df['Item'].unique()
    correlations_data = []
    
    for item in items:
        corr_students = calculate_correlation(df, item, 'Students_Present')
        corr_temp = calculate_correlation(df, item, 'Temperature_C')
        corr_price = calculate_correlation(df, item, 'Price')
        
        correlations_data.append({
            'Food Item': item,
            'Students vs Demand': f"{corr_students['pearson_r']:.3f}",
            'Temperature vs Demand': f"{corr_temp['pearson_r']:.3f}",
            'Price vs Demand': f"{corr_price['pearson_r']:.3f}"
        })
    
    return pd.DataFrame(correlations_data)
