"""
Probability Module
Calculates empirical probabilities from historical data
"""

import pandas as pd
import numpy as np

def calculate_empirical_probability(df, food_item, threshold):
    """
    Calculate empirical probability P(X > threshold)
    
    Parameters:
    df: DataFrame with food data
    food_item: Name of the food item
    threshold: Demand threshold value
    
    Returns:
    dict: Dictionary with probability results
    """
    
    # Filter data
    item_data = df[df['Item'] == food_item]['Actual_Demand'].values
    
    if len(item_data) == 0:
        return None
    
    # Count observations above threshold
    above_threshold = np.sum(item_data > threshold)
    total_observations = len(item_data)
    
    # Calculate probability
    probability = (above_threshold / total_observations) * 100 if total_observations > 0 else 0
    
    # Calculate complementary probability (below or equal)
    below_equal_threshold = total_observations - above_threshold
    
    # Additional statistics
    mean = np.mean(item_data)
    std_dev = np.std(item_data)
    
    # Z-score (for normal approximation)
    z_score = (threshold - mean) / std_dev if std_dev > 0 else 0
    
    result = {
        'item': food_item,
        'threshold': threshold,
        'probability': probability,
        'above_threshold': above_threshold,
        'below_equal_threshold': below_equal_threshold,
        'total_observations': total_observations,
        'mean': mean,
        'std_dev': std_dev,
        'z_score': z_score
    }
    
    return result

def get_probability_insight(result):
    """
    Generate natural language insight for probability result
    
    Parameters:
    result: Dictionary with probability calculation results
    
    Returns:
    str: Formatted insight text
    """
    
    item = result['item']
    threshold = result['threshold']
    prob = result['probability']
    above = result['above_threshold']
    total = result['total_observations']
    days = total / 8 if total > 0 else 0  # Approximate number of unique days
    
    insight = f"""
    **Demand Threshold Analysis for {item}**
    
    **Probability:** Demand exceeded {threshold} units on **{prob:.1f}%** of observed days.
    
    **Occurrences:** Out of {total} observations, demand was above {threshold} units on **{above} days**.
    
    **Interpretation:** On approximately **{prob:.0f}% of days**, the canteen should expect {item} demand to exceed {threshold} units.
    
    **Practical Meaning:** If you prepare only {threshold} units, you'll face potential shortages on roughly {prob:.0f}% of days.
    """
    
    return insight

def get_probability_statistics(df, food_item):
    """
    Get probability statistics for different thresholds
    
    Parameters:
    df: DataFrame with food data
    food_item: Name of the food item
    
    Returns:
    DataFrame: Probabilities for different threshold percentiles
    """
    
    item_data = df[df['Item'] == food_item]['Actual_Demand'].values
    
    if len(item_data) == 0:
        return None
    
    percentiles = [25, 50, 75, 90, 95]
    thresholds = [np.percentile(item_data, p) for p in percentiles]
    
    prob_data = []
    
    for percentile, threshold in zip(percentiles, thresholds):
        prob = calculate_empirical_probability(df, food_item, threshold)
        prob_data.append({
            'Percentile': f'{percentile}th',
            'Threshold': f'{threshold:.0f} units',
            'P(X > threshold)': f'{prob["probability"]:.1f}%',
            'Days Above': f'{prob["above_threshold"]} days'
        })
    
    return pd.DataFrame(prob_data)
