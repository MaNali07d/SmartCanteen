"""
SmartCanteen Dataset Generator
Generates realistic simulated canteen data with meaningful correlations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

def generate_smartcanteen_data(days=365):
    """
    Generate realistic canteen data with meaningful relationships
    
    Parameters:
    days: Number of days to generate (default 365 for 1 year)
    """
    
    # Food items and their base properties
    food_items = ['Samosa', 'Vada Pav', 'Sandwich', 'Tea', 'Coffee', 
                  'Cold Drink', 'Veg Puff', 'Maggi']
    
    # Base demand for each food item (average)
    base_demand = {
        'Samosa': 120,
        'Vada Pav': 95,
        'Sandwich': 85,
        'Tea': 150,
        'Coffee': 110,
        'Cold Drink': 90,
        'Veg Puff': 75,
        'Maggi': 65
    }
    
    # Price of each item
    prices = {
        'Samosa': 12,
        'Vada Pav': 15,
        'Sandwich': 40,
        'Tea': 8,
        'Coffee': 15,
        'Cold Drink': 20,
        'Veg Puff': 18,
        'Maggi': 30
    }
    
    # Temperature patterns (realistic for Mumbai)
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    data = []
    
    for date in dates:
        day_of_week = date.weekday()  # 0=Monday, 6=Sunday
        month = date.month
        day_name = date.strftime('%A')
        
        # Determine if it's weekend
        is_weekend = day_of_week >= 5  # Saturday, Sunday
        
        # Simplified holiday detection (basic approach)
        is_holiday = False
        if (month == 1 and date.day in [26]):  # Republic Day
            is_holiday = True
        if (month == 8 and date.day in [15]):  # Independence Day
            is_holiday = True
        if (month == 10 and date.day in [2]):  # Gandhi Jayanti
            is_holiday = True
        
        # Determine if it's exam week (simplified)
        is_exam_week = (month in [4, 5, 11, 12])  # Rough exam periods
        
        # Generate student attendance
        base_students = 1000
        
        if is_weekend:
            students = np.random.normal(500, 50, 1)[0]
        elif is_holiday:
            students = np.random.normal(200, 30, 1)[0]
        elif is_exam_week:
            students = np.random.normal(800, 100, 1)[0]
        else:
            students = np.random.normal(900, 150, 1)[0]
        
        students = max(0, int(students))
        
        # Temperature pattern (Mumbai climate)
        # Winter: Jan-Feb (22-28°C), Summer: Mar-May (30-38°C)
        # Monsoon: Jun-Sep (25-30°C), Post-monsoon: Oct-Nov (25-32°C)
        if month in [12, 1, 2]:
            temperature = np.random.normal(25, 2)
        elif month in [3, 4, 5]:
            temperature = np.random.normal(34, 3)
        elif month in [6, 7, 8, 9]:
            temperature = np.random.normal(28, 2)
        else:
            temperature = np.random.normal(29, 2)
        
        temperature = np.clip(temperature, 18, 42)
        
        # Generate demand for each food item
        for item in food_items:
            base = base_demand[item]
            
            # Factor 1: Student count effect
            attendance_factor = (students / 900) if students > 0 else 0.2
            
            # Factor 2: Temperature effect
            if item in ['Cold Drink']:
                temp_factor = 1 + (temperature - 25) * 0.05  # High temp increases cold drink demand
            elif item in ['Tea', 'Coffee']:
                temp_factor = 1 + (25 - temperature) * 0.03  # Low temp increases tea/coffee
            else:
                temp_factor = 1
            
            # Factor 3: Day of week effect
            if is_weekend:
                dow_factor = 0.7
            elif is_exam_week:
                dow_factor = 0.85
            else:
                dow_factor = 1.0
            
            # Factor 4: Holiday effect
            if is_holiday:
                dow_factor *= 0.3
            
            # Calculate actual demand with random noise
            demand = base * attendance_factor * temp_factor * dow_factor
            demand = demand + np.random.normal(0, base * 0.1)  # Add noise
            demand = max(1, int(demand))
            
            # Prepare amount (often imperfect)
            # Good canteens prepare ~110% of expected, poor ones might over/under prepare
            prepared_factor = np.random.normal(1.15, 0.15)  # 115% average
            prepared = max(int(demand * prepared_factor), 1)
            
            # Sold amount (less than or equal to prepared)
            sold = min(prepared, demand + np.random.normal(0, max(1, demand * 0.05)))
            sold = max(0, int(sold))
            
            # Waste
            waste = prepared - sold
            waste_percentage = (waste / prepared * 100) if prepared > 0 else 0
            
            data.append({
                'Date': date,
                'Day': day_name,
                'Weekend': is_weekend,
                'Holiday': is_holiday,
                'Exam_Week': is_exam_week,
                'Students_Present': students,
                'Temperature_C': round(temperature, 1),
                'Item': item,
                'Actual_Demand': demand,
                'Prepared': prepared,
                'Sold': sold,
                'Waste': waste,
                'Waste_Percentage': round(waste_percentage, 2),
                'Price': prices[item]
            })
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("🍽️ Generating SmartCanteen Dataset...")
    
    # Generate dataset
    df = generate_smartcanteen_data(days=365)
    
    # Save to CSV
    df.to_csv('smartcanteen_dataset.csv', index=False)
    
    print(f"✓ Dataset generated successfully!")
    print(f"📊 Total records: {len(df)}")
    print(f"🍱 Food items: {df['Item'].nunique()}")
    print(f"📅 Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"\n📁 Saved as: smartcanteen_dataset.csv")
    print(f"\nDataset preview:\n{df.head()}")
    print(f"\nDataset info:\n{df.info()}")
