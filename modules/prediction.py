"""
Prediction Module
Implements linear regression for demand forecasting
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import warnings

warnings.filterwarnings('ignore')

class DemandPredictor:
    """
    Linear Regression model for demand prediction
    
    Model: Demand = β0 + β1(Students) + β2(Temperature) + β3(ExamWeek) + β4(Holiday)
    """
    
    def __init__(self, df, food_item):
        """
        Initialize predictor for a specific food item
        
        Parameters:
        df: DataFrame with training data
        food_item: Name of the food item
        """
        
        self.food_item = food_item
        self.model = None
        self.X_train = None
        self.y_train = None
        self.metrics = {}
        self.coefficients = {}
        
        # Train the model
        self._train(df)
    
    def _train(self, df):
        """
        Train the linear regression model
        
        Parameters:
        df: Training DataFrame
        """
        
        # Filter data for the food item
        item_df = df[df['Item'] == self.food_item].copy()
        
        # Features
        feature_cols = ['Students_Present', 'Temperature_C', 'Exam_Week', 'Holiday']
        
        # Convert boolean to int
        item_df['Exam_Week'] = item_df['Exam_Week'].astype(int)
        item_df['Holiday'] = item_df['Holiday'].astype(int)
        
        # Prepare training data
        X = item_df[feature_cols].values
        y = item_df['Actual_Demand'].values
        
        # Train model
        self.model = LinearRegression()
        self.model.fit(X, y)
        
        # Store training data
        self.X_train = X
        self.y_train = y
        
        # Get predictions on training data
        y_pred = self.model.predict(X)
        
        # Calculate metrics
        self.metrics = {
            'mae': mean_absolute_error(y, y_pred),
            'rmse': np.sqrt(mean_squared_error(y, y_pred)),
            'r2': r2_score(y, y_pred),
            'mape': np.mean(np.abs((y - y_pred) / y)) * 100 if np.all(y != 0) else 0
        }
        
        # Store coefficients
        self.coefficients = {
            'intercept': self.model.intercept_,
            'Students_Present': self.model.coef_[0],
            'Temperature_C': self.model.coef_[1],
            'Exam_Week': self.model.coef_[2],
            'Holiday': self.model.coef_[3]
        }
    
    def predict(self, students, temperature, exam_week, holiday):
        """
        Predict demand for given conditions
        
        Parameters:
        students: Number of students present
        temperature: Temperature in Celsius
        exam_week: Boolean (1 for exam week, 0 otherwise)
        holiday: Boolean (1 for holiday, 0 otherwise)
        
        Returns:
        float: Predicted demand
        """
        
        if self.model is None:
            return 0
        
        # Prepare input
        exam_week = int(exam_week)
        holiday = int(holiday)
        
        X = np.array([[students, temperature, exam_week, holiday]])
        
        # Predict
        prediction = self.model.predict(X)[0]
        
        # Ensure non-negative prediction
        prediction = max(0, prediction)
        
        return prediction
    
    def predict_batch(self, df_input):
        """
        Predict demand for multiple records
        
        Parameters:
        df_input: DataFrame with feature columns
        
        Returns:
        array: Array of predictions
        """
        
        if self.model is None:
            return np.array([])
        
        feature_cols = ['Students_Present', 'Temperature_C', 'Exam_Week', 'Holiday']
        
        # Convert boolean to int
        df_temp = df_input.copy()
        df_temp['Exam_Week'] = df_temp['Exam_Week'].astype(int)
        df_temp['Holiday'] = df_temp['Holiday'].astype(int)
        
        X = df_temp[feature_cols].values
        
        predictions = self.model.predict(X)
        predictions = np.maximum(predictions, 0)  # Ensure non-negative
        
        return predictions
    
    def get_model_summary(self):
        """
        Get model summary and coefficients
        
        Returns:
        dict: Model summary information
        """
        
        return {
            'item': self.food_item,
            'n_samples': len(self.y_train),
            'coefficients': self.coefficients,
            'metrics': self.metrics
        }
    
    def get_residuals(self):
        """
        Get residuals (actual - predicted)
        
        Returns:
        array: Array of residuals
        """
        
        if self.model is None:
            return np.array([])
        
        y_pred = self.model.predict(self.X_train)
        residuals = self.y_train - y_pred
        
        return residuals
    
    def get_predictions_comparison(self, df=None):
        """
        Get comparison of actual vs predicted for all training data
        
        Parameters:
        df: Optional DataFrame to filter
        
        Returns:
        DataFrame: Comparison of actual vs predicted
        """
        
        if self.model is None:
            return None
        
        y_pred = self.model.predict(self.X_train)
        
        comparison_df = pd.DataFrame({
            'Actual': self.y_train,
            'Predicted': y_pred.astype(int),
            'Residual': (self.y_train - y_pred).astype(int),
            'Abs_Error': np.abs(self.y_train - y_pred).astype(int)
        })
        
        return comparison_df

def train_predictors(df):
    """
    Train predictors for all food items
    
    Parameters:
    df: DataFrame with training data
    
    Returns:
    dict: Dictionary of predictors keyed by food item
    """
    
    items = df['Item'].unique()
    predictors = {}
    
    for item in items:
        predictors[item] = DemandPredictor(df, item)
    
    return predictors

def get_prediction_recommendation(predicted_demand, safety_buffer):
    """
    Calculate recommended preparation based on prediction
    
    Parameters:
    predicted_demand: Predicted demand (float)
    safety_buffer: Safety buffer percentage (0-20)
    
    Returns:
    int: Recommended preparation quantity
    """
    
    recommended = predicted_demand * (1 + safety_buffer / 100)
    
    return int(recommended)
