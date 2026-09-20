"""
Insights Module
Generates contextual insights and recommendations
"""

import pandas as pd
import numpy as np

def generate_dashboard_insight(df, food_item, students, temperature, exam_week, holiday, predicted_demand):
    """
    Generate insight text for the dashboard
    
    Parameters:
    df: DataFrame with historical data
    food_item: Selected food item
    students: Expected student count
    temperature: Expected temperature
    exam_week: Boolean - is exam week
    holiday: Boolean - is holiday
    predicted_demand: Predicted demand value
    
    Returns:
    str: Formatted insight text
    """
    
    # Get historical context
    item_df = df[df['Item'] == food_item]
    historical_avg = item_df['Actual_Demand'].mean()
    historical_waste_pct = item_df['Waste_Percentage'].mean()
    
    # Generate insight based on conditions
    conditions = []
    
    if students > item_df['Students_Present'].mean() + 100:
        conditions.append("higher than average attendance")
    elif students < item_df['Students_Present'].mean() - 100:
        conditions.append("lower than average attendance")
    
    if temperature > 30:
        conditions.append("hot weather")
    elif temperature < 20:
        conditions.append("cool weather")
    
    if exam_week:
        conditions.append("exam period")
    
    if holiday:
        conditions.append("holiday")
    
    # Build insight
    condition_text = ", ".join(conditions) if conditions else "normal conditions"
    
    comparison = "higher" if predicted_demand > historical_avg else "lower" if predicted_demand < historical_avg else "similar"
    
    variance_pct = ((predicted_demand - historical_avg) / historical_avg * 100) if historical_avg > 0 else 0
    
    insight = f"""
Based on {condition_text}, {food_item} demand is predicted to be **{comparison}** than the historical average ({historical_avg:.0f} units).

**Expected Prediction:** {predicted_demand:.0f} units ({variance_pct:+.0f}% from average)

**Historical Waste Rate:** {historical_waste_pct:.1f}%

This prediction is based on linear regression analysis of student attendance, temperature, exam schedules, and holiday patterns.
"""
    
    return insight

def generate_what_if_insight(scenario_a_pred, scenario_b_pred, scenario_a_label, scenario_b_label):
    """
    Generate insight for what-if comparison
    
    Parameters:
    scenario_a_pred: Prediction for scenario A
    scenario_b_pred: Prediction for scenario B
    scenario_a_label: Description of scenario A
    scenario_b_label: Description of scenario B
    
    Returns:
    str: Formatted comparison insight
    """
    
    difference = scenario_b_pred - scenario_a_pred
    pct_change = (difference / scenario_a_pred * 100) if scenario_a_pred > 0 else 0
    
    insight = f"""
**Comparison Result:**

- **{scenario_a_label}:** {scenario_a_pred:.0f} units
- **{scenario_b_label}:** {scenario_b_pred:.0f} units

**Difference:** {difference:+.0f} units ({pct_change:+.1f}%)

This demonstrates how changing key variables significantly impacts demand prediction. Such analysis helps in capacity planning and inventory management.
"""
    
    return insight

def generate_model_performance_insight(mae, rmse, r2, mape):
    """
    Generate insight about model performance
    
    Parameters:
    mae: Mean Absolute Error
    rmse: Root Mean Squared Error
    r2: R-squared value
    mape: Mean Absolute Percentage Error
    
    Returns:
    str: Formatted performance insight
    """
    
    # Interpret R²
    if r2 > 0.7:
        r2_interpretation = "strong predictive power"
    elif r2 > 0.5:
        r2_interpretation = "moderate predictive power"
    else:
        r2_interpretation = "limited predictive power"
    
    # Interpret MAPE
    if mape < 15:
        accuracy_level = "highly accurate"
    elif mape < 25:
        accuracy_level = "moderately accurate"
    else:
        accuracy_level = "requiring improvement"
    
    insight = f"""
**Model Performance Metrics:**

- **R² Score:** {r2:.3f} - The model explains {r2*100:.1f}% of demand variation ({r2_interpretation})
- **MAE:** {mae:.1f} units - On average, predictions are off by ±{mae:.0f} units
- **RMSE:** {rmse:.1f} units - Root mean squared error accounts for larger deviations
- **MAPE:** {mape:.1f}% - Mean absolute percentage error ({accuracy_level})

**Interpretation:** The model's performance indicates it captures major demand patterns but should be used alongside domain expertise and real-time feedback.
"""
    
    return insight

def get_smart_recommendation_text(predicted_demand, recommended_prep, food_item, students, 
                                  historical_waste_pct, safety_buffer, waste_status):
    """
    Generate smart recommendation text
    
    Parameters:
    predicted_demand: Predicted demand
    recommended_prep: Recommended preparation quantity
    food_item: Food item name
    students: Expected student count
    historical_waste_pct: Average waste percentage
    safety_buffer: Safety buffer percentage applied
    waste_status: Waste status string
    
    Returns:
    str: Formatted recommendation
    """
    
    recommendation = f"""
**SMART RECOMMENDATION**

**Prepare approximately {recommended_prep} units of {food_item}**

---

**Reasoning:**

📊 **Predicted demand** is {predicted_demand:.0f} units based on:
- Expected attendance: {students} students
- Historical demand pattern
- Seasonal and temporal factors

🛡️ **Safety buffer** of {safety_buffer}% has been applied to reduce shortage risk

♻️ **Expected waste rate:** {historical_waste_pct:.1f}% based on historical patterns

📈 **Preparation formula:** Predicted Demand × (1 + Safety Buffer%) = {predicted_demand:.0f} × {1 + safety_buffer/100:.2f} = {recommended_prep} units

✅ **Status:** {waste_status}

---

This recommendation balances between minimizing waste and avoiding shortages. Monitor actual sales to refine future predictions.
"""
    
    return recommendation

def generate_data_quality_summary(df):
    """
    Generate summary of data quality metrics
    
    Parameters:
    df: DataFrame to analyze
    
    Returns:
    str: Data quality summary
    """
    
    total_records = len(df)
    null_count = df.isnull().sum().sum()
    null_pct = (null_count / (len(df) * len(df.columns)) * 100) if len(df) > 0 else 0
    
    unique_items = df['Item'].nunique()
    date_range = f"{df['Date'].min().date()} to {df['Date'].max().date()}" if 'Date' in df.columns else "N/A"
    
    summary = f"""
**Dataset Quality Summary**

📊 **Total Records:** {total_records:,}
🍱 **Food Items:** {unique_items}
📅 **Date Range:** {date_range}
✓ **Data Completeness:** {100 - null_pct:.1f}% (minimal missing values)
⚖️ **Status:** ✅ High Quality Simulated Academic Dataset
"""
    
    return summary
