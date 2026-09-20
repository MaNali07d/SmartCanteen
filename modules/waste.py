"""
Waste Analytics Module
Analyzes food waste patterns and provides recommendations
"""

import pandas as pd
import numpy as np

def calculate_waste_summary(df, food_item=None):
    """
    Calculate comprehensive waste statistics
    
    Parameters:
    df: DataFrame with food data
    food_item: Optional - specific food item (default: all items)
    
    Returns:
    dict: Waste summary statistics
    """
    
    if food_item:
        data = df[df['Item'] == food_item].copy()
    else:
        data = df.copy()
    
    if len(data) == 0:
        return None
    
    total_prepared = data['Prepared'].sum()
    total_sold = data['Sold'].sum()
    total_waste = data['Waste'].sum()
    
    waste_percentage = (total_waste / total_prepared * 100) if total_prepared > 0 else 0
    
    summary = {
        'item': food_item,
        'total_prepared': int(total_prepared),
        'total_sold': int(total_sold),
        'total_waste': int(total_waste),
        'waste_percentage': waste_percentage,
        'avg_daily_waste': data['Waste'].mean(),
        'avg_daily_waste_pct': data['Waste_Percentage'].mean(),
        'max_daily_waste': data['Waste'].max(),
        'min_daily_waste': data['Waste'].min(),
        'waste_std': data['Waste'].std(),
        'financial_loss': (total_waste * data['Price'].mean()) if len(data) > 0 else 0,
        'n_days': data['Date'].nunique() if 'Date' in data.columns else len(data) / 8
    }
    
    return summary

def get_waste_status(waste_percentage):
    """
    Determine waste status based on percentage
    
    Parameters:
    waste_percentage: Waste percentage value
    
    Returns:
    tuple: (status, emoji, color)
    """
    
    if waste_percentage < 15:
        return "LOW WASTE", "🟢", "#2ecc71"
    elif waste_percentage < 25:
        return "MODERATE WASTE", "🟡", "#f39c12"
    else:
        return "HIGH WASTE", "🔴", "#e74c3c"

def get_waste_by_item(df):
    """
    Get waste statistics for all food items
    
    Parameters:
    df: DataFrame with food data
    
    Returns:
    DataFrame: Waste statistics by item
    """
    
    items = df['Item'].unique()
    waste_data = []
    
    for item in items:
        summary = calculate_waste_summary(df, item)
        waste_data.append({
            'Food Item': item,
            'Avg Waste %': f"{summary['avg_daily_waste_pct']:.1f}%",
            'Total Waste': f"{summary['total_waste']} units",
            'Avg Daily Waste': f"{summary['avg_daily_waste']:.0f} units",
            'Financial Loss': f"₹{summary['financial_loss']:.0f}"
        })
    
    return pd.DataFrame(waste_data)

def analyze_waste_by_conditions(df, food_item):
    """
    Analyze waste patterns under different conditions
    
    Parameters:
    df: DataFrame with food data
    food_item: Name of the food item
    
    Returns:
    dict: Waste analysis by different conditions
    """
    
    item_df = df[df['Item'] == food_item].copy()
    
    analysis = {
        'item': food_item,
        'weekdays': {
            'avg_waste': item_df[~item_df['Weekend']]['Waste'].mean(),
            'avg_waste_pct': item_df[~item_df['Weekend']]['Waste_Percentage'].mean()
        },
        'weekends': {
            'avg_waste': item_df[item_df['Weekend']]['Waste'].mean(),
            'avg_waste_pct': item_df[item_df['Weekend']]['Waste_Percentage'].mean()
        },
        'exam_weeks': {
            'avg_waste': item_df[item_df['Exam_Week']]['Waste'].mean(),
            'avg_waste_pct': item_df[item_df['Exam_Week']]['Waste_Percentage'].mean()
        },
        'normal_weeks': {
            'avg_waste': item_df[~item_df['Exam_Week']]['Waste'].mean(),
            'avg_waste_pct': item_df[~item_df['Exam_Week']]['Waste_Percentage'].mean()
        }
    }
    
    return analysis

def get_waste_recommendations(df, food_item):
    """
    Generate waste reduction recommendations
    
    Parameters:
    df: DataFrame with food data
    food_item: Name of the food item
    
    Returns:
    list: List of recommendation strings
    """
    
    item_df = df[df['Item'] == food_item].copy()
    summary = calculate_waste_summary(df, food_item)
    
    recommendations = []
    
    # Recommendation 1: Overall waste level
    if summary['waste_percentage'] > 25:
        recommendations.append(
            f"⚠️ {food_item} shows high waste ({summary['waste_percentage']:.1f}%). "
            f"Consider reducing preparation quantities or improving demand forecasting."
        )
    
    # Recommendation 2: Weekend vs Weekday
    weekend_waste = item_df[item_df['Weekend']]['Waste_Percentage'].mean()
    weekday_waste = item_df[~item_df['Weekend']]['Waste_Percentage'].mean()
    
    if weekend_waste > weekday_waste + 5:
        recommendations.append(
            f"📉 Weekend waste for {food_item} is significantly higher ({weekend_waste:.1f}% vs {weekday_waste:.1f}%). "
            f"Reduce weekend preparation."
        )
    
    # Recommendation 3: High waste days
    high_waste_days = item_df[item_df['Waste_Percentage'] > 35]
    if len(high_waste_days) > 0:
        # Analyze conditions on high waste days
        if high_waste_days['Students_Present'].mean() < item_df['Students_Present'].mean() - 50:
            recommendations.append(
                f"👥 {food_item} wastes more on low-attendance days. "
                f"Implement dynamic preparation based on expected student count."
            )
    
    # Recommendation 4: Consistency
    if summary['waste_std'] > summary['avg_daily_waste'] * 0.5:
        recommendations.append(
            f"📊 {food_item}'s waste is inconsistent (high variation). "
            f"Use safety buffers more intelligently to balance cost and shortages."
        )
    
    # Recommendation 5: Success case
    if summary['waste_percentage'] < 15:
        recommendations.append(
            f"✅ {food_item} has excellent waste management. "
            f"Current preparation strategy is effective."
        )
    
    return recommendations if recommendations else [f"📊 {food_item} waste is within acceptable range."]

def get_waste_vs_attendance_analysis(df, food_item):
    """
    Analyze relationship between attendance and waste
    
    Parameters:
    df: DataFrame with food data
    food_item: Name of the food item
    
    Returns:
    DataFrame: Waste by attendance category
    """
    
    item_df = df[df['Item'] == food_item].copy()
    
    # Create attendance categories
    mean_attendance = item_df['Students_Present'].mean()
    item_df['Attendance_Category'] = pd.cut(
        item_df['Students_Present'],
        bins=[0, mean_attendance * 0.7, mean_attendance, mean_attendance * 1.3, np.inf],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    analysis = item_df.groupby('Attendance_Category').agg({
        'Waste_Percentage': ['mean', 'count'],
        'Prepared': 'mean',
        'Sold': 'mean',
        'Waste': 'mean'
    }).round(1)
    
    return analysis
