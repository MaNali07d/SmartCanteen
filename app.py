"""
SmartCanteen - PSDA Analytics Dashboard
An interactive analytics system for college canteen demand prediction and waste reduction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Import modules
from modules.statistics import calculate_statistics, get_insight_text, get_all_items_summary
from modules.probability import calculate_empirical_probability, get_probability_insight, get_probability_statistics
from modules.correlation import calculate_correlation, get_correlation_insight, get_correlation_matrix, get_all_items_correlations
from modules.prediction import DemandPredictor, train_predictors, get_prediction_recommendation
from modules.waste import calculate_waste_summary, get_waste_status, get_waste_by_item, analyze_waste_by_conditions, get_waste_recommendations, get_waste_vs_attendance_analysis
from modules.insights import (generate_dashboard_insight, generate_what_if_insight, 
                             generate_model_performance_insight, get_smart_recommendation_text,
                             generate_data_quality_summary)

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="SmartCanteen",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM STYLING ====================
st.markdown("""
    <style>
    :root {
        --primary-teal: #0F7C7E;
        --primary-green: #1B5E5E;
        --accent-orange: #E8914C;
        --accent-gold: #D4A574;
        --secondary-sage: #A8B8A8;
        --bg-cream: #F5F1ED;
        --text-dark: #2C3E50;
    }
    
    * {
        margin: 0;
        padding: 0;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-teal);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        color: var(--text-dark);
        font-weight: 600;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f7f5 100%);
        border-left: 4px solid var(--primary-teal);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(15, 124, 126, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(15, 124, 126, 0.15);
    }
    
    .insight-box {
        background: linear-gradient(135deg, #f0f9f9 0%, #f5f1ed 100%);
        border-left: 4px solid var(--accent-orange);
        border-radius: 8px;
        padding: 1.2rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
        color: var(--text-dark);
    }
    
    .kpi-large {
        background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-green) 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(15, 124, 126, 0.2);
        margin: 1rem 0;
    }
    
    .kpi-large h3 {
        font-size: 1.1rem;
        font-weight: 600;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .kpi-large .value {
        font-size: 3rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .kpi-large .description {
        font-size: 0.9rem;
        opacity: 0.85;
        line-height: 1.4;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #f0fff4 0%, #f5f1ed 100%);
        border-left: 5px solid #27ae60;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        font-size: 0.95rem;
        line-height: 1.7;
        color: var(--text-dark);
    }
    
    .comparison-section {
        background: linear-gradient(135deg, #fff9f0 0%, #f5f1ed 100%);
        border: 1px solid rgba(232, 145, 76, 0.2);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-teal);
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-dark);
        margin-top: 0.5rem;
    }
    
    .status-low {
        color: #27ae60;
        font-weight: 600;
    }
    
    .status-moderate {
        color: #f39c12;
        font-weight: 600;
    }
    
    .status-high {
        color: #e74c3c;
        font-weight: 600;
    }
    
    h1 {
        color: var(--primary-teal);
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: var(--primary-teal);
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid var(--accent-orange);
        padding-bottom: 0.5rem;
    }
    
    h3 {
        color: var(--primary-green);
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-teal);
        margin: 1rem 0 0.5rem 0;
    }
    
    .footer-text {
        text-align: center;
        font-size: 0.8rem;
        color: var(--secondary-sage);
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(168, 184, 168, 0.2);
    }
    
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
@st.cache_resource
def load_data():
    """Load and cache the dataset"""
    df = pd.read_csv('smartcanteen_dataset.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

@st.cache_resource
def train_models(df):
    """Train and cache prediction models"""
    return train_predictors(df)

# Load data
df = load_data()
models = train_models(df)

# ==================== SIDEBAR ====================
st.sidebar.markdown("## 🍽️ SMARTCANTEEN")
st.sidebar.markdown("### *Turn Data Into Smarter Meals.*")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio(
    "**Navigation**",
    ["🏠 Dashboard", "📊 Statistics", "🎲 Probability", "🔗 Correlation", 
     "🔮 Prediction", "♻️ Waste Analytics", "🍱 Food Comparison", 
     "📊 Data Explorer", "ℹ️ About"],
    key="page_nav"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### **PSDA Working Model**")
st.sidebar.markdown("*Simulated Academic Dataset*")
st.sidebar.markdown(f"📅 Records: {len(df):,}")
st.sidebar.markdown(f"🍱 Items: {df['Item'].nunique()}")

# ==================== PAGES ====================

# PAGE 1: DASHBOARD
if page == "🏠 Dashboard":
    # Hero Section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("# 🍽️ SmartCanteen")
        st.markdown("### Turn Data Into Smarter Meals.")
        st.markdown("""
An interactive PSDA-based analytics system that helps canteens understand demand, 
predict future requirements and reduce unnecessary food waste.
        """)
    
    st.markdown("---")
    
    # Scenario Controls
    st.markdown("## 🎯 Smart Prediction Scenario")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        food_item = st.selectbox("🍱 Food Item", sorted(df['Item'].unique()), key="dash_food")
    with col2:
        students = st.slider("👥 Expected Students", 100, 1200, 900, step=50, key="dash_students")
    with col3:
        temperature = st.slider("🌡️ Temperature (°C)", 18, 42, 28, step=1, key="dash_temp")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        exam_week = st.checkbox("📚 Exam Week", value=False, key="dash_exam")
    with col2:
        holiday = st.checkbox("🎉 Holiday", value=False, key="dash_holiday")
    with col3:
        safety_buffer = st.slider("🛡️ Safety Buffer %", 0, 20, 5, step=1, key="dash_buffer")
    
    # Predict
    model = models[food_item]
    predicted_demand = model.predict(students, temperature, exam_week, holiday)
    recommended_prep = get_prediction_recommendation(predicted_demand, safety_buffer)
    
    # KPI Cards
    st.markdown("## 📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📈 Predicted Demand",
            f"{predicted_demand:.0f}",
            "units/day",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "🍽️ Recommended Prep",
            f"{recommended_prep}",
            "units",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            "👥 Expected Students",
            f"{students}",
            "students",
            delta_color="off"
        )
    
    with col4:
        item_waste = df[df['Item'] == food_item]['Waste_Percentage'].mean()
        status, emoji, _ = get_waste_status(item_waste)
        st.metric(
            "♻️ Avg Waste",
            f"{item_waste:.1f}%",
            f"{emoji} {status}",
            delta_color="off"
        )
    
    # Recommendation Box
    st.markdown("---")
    st.markdown("## ✅ Smart Recommendation")
    
    waste_summary = calculate_waste_summary(df, food_item)
    waste_status, _, _ = get_waste_status(waste_summary['avg_daily_waste_pct'])
    
    rec_text = get_smart_recommendation_text(
        predicted_demand, recommended_prep, food_item, students,
        waste_summary['avg_daily_waste_pct'], safety_buffer, waste_status
    )
    
    st.markdown(f"""<div class="recommendation-box">{rec_text}</div>""", unsafe_allow_html=True)
    
    # Charts
    st.markdown("---")
    st.markdown("## 📊 Demand Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Demand trend
        item_df = df[df['Item'] == food_item].copy()
        item_df['Date'] = pd.to_datetime(item_df['Date'])
        daily_demand = item_df.groupby('Date')['Actual_Demand'].mean().reset_index()
        
        fig = px.line(daily_demand, x='Date', y='Actual_Demand',
                     title=f"{food_item} - Demand Trend (90 days)",
                     labels={'Actual_Demand': 'Demand (units)', 'Date': 'Date'},
                     color_discrete_sequence=['#0F7C7E'])
        fig.add_hline(y=predicted_demand, line_dash="dash", line_color="#E8914C",
                     annotation_text=f"Predicted: {predicted_demand:.0f}")
        fig.update_layout(hovermode='x unified', height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Prepared vs Sold vs Waste
        item_summary = item_df.groupby(item_df['Date'].dt.date)[['Prepared', 'Sold', 'Waste']].sum()
        item_summary = item_summary.tail(30)
        
        fig = go.Figure(data=[
            go.Bar(x=item_summary.index, y=item_summary['Prepared'], name='Prepared', marker_color='#0F7C7E'),
            go.Bar(x=item_summary.index, y=item_summary['Sold'], name='Sold', marker_color='#27ae60'),
            go.Bar(x=item_summary.index, y=item_summary['Waste'], name='Waste', marker_color='#e74c3c')
        ])
        fig.update_layout(barmode='stack', title=f"{food_item} - Prepared vs Sold vs Waste (Last 30 days)",
                         xaxis_title='Date', yaxis_title='Units', height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    # Dashboard Insight
    insight_text = generate_dashboard_insight(df, food_item, students, temperature, exam_week, holiday, predicted_demand)
    st.markdown(f"""<div class="insight-box">{insight_text}</div>""", unsafe_allow_html=True)

# PAGE 2: STATISTICS
elif page == "📊 Statistics":
    st.markdown("# 📊 Statistical Analysis")
    st.markdown("Comprehensive descriptive statistics for demand analysis")
    
    st.markdown("---")
    
    # Food item selection
    food_item = st.selectbox("Select Food Item:", sorted(df['Item'].unique()), key="stats_food")
    
    # Calculate statistics
    stats = calculate_statistics(df, food_item)
    
    if stats:
        # Statistics Cards
        st.markdown("## 📈 Descriptive Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Mean</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0F7C7E;">{stats['mean']:.0f}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">units/day</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Median</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0F7C7E;">{stats['median']:.0f}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">units/day</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Std Dev</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0F7C7E;">{stats['std_dev']:.1f}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">dispersion</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Range</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0F7C7E;">{stats['range']:.0f}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">max - min</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed Statistics Table
        st.markdown("## 📋 Detailed Metrics")
        
        stats_display = pd.DataFrame({
            'Statistic': ['Mean', 'Median', 'Mode', 'Minimum', 'Maximum', 'Range', 'Variance', 'Standard Deviation', 'Q1 (25th)', 'Q3 (75th)', 'IQR'],
            'Value': [
                f"{stats['mean']:.2f}",
                f"{stats['median']:.2f}",
                f"{stats['mode']:.2f}",
                f"{stats['min']:.2f}",
                f"{stats['max']:.2f}",
                f"{stats['range']:.2f}",
                f"{stats['variance']:.2f}",
                f"{stats['std_dev']:.2f}",
                f"{stats['q1']:.2f}",
                f"{stats['q3']:.2f}",
                f"{stats['iqr']:.2f}"
            ]
        })
        
        st.dataframe(stats_display, use_container_width=True, hide_index=True)
        
        # Charts
        st.markdown("---")
        st.markdown("## 📊 Visualizations")
        
        item_data = df[df['Item'] == food_item]['Actual_Demand'].values
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            fig = px.histogram(x=item_data, nbins=30, title=f"{food_item} - Demand Distribution",
                             labels={'x': 'Demand (units)', 'count': 'Frequency'},
                             color_discrete_sequence=['#0F7C7E'])
            fig.update_layout(height=400, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Box Plot
            fig = go.Figure(data=[
                go.Box(y=item_data, name=food_item, marker_color='#0F7C7E')
            ])
            fig.update_layout(title=f"{food_item} - Demand Distribution (Box Plot)",
                             yaxis_title='Demand (units)', height=400, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        # Daily trend
        item_df = df[df['Item'] == food_item].copy()
        item_df['Date'] = pd.to_datetime(item_df['Date'])
        daily_demand = item_df.groupby('Date')['Actual_Demand'].mean().reset_index()
        
        fig = px.line(daily_demand, x='Date', y='Actual_Demand',
                     title=f"{food_item} - Daily Demand Trend",
                     labels={'Actual_Demand': 'Demand (units)', 'Date': 'Date'},
                     color_discrete_sequence=['#0F7C7E'])
        fig.update_layout(hovermode='x unified', height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
        
        # Insight
        insight_text = get_insight_text(stats)
        st.markdown(f"""<div class="insight-box">{insight_text}</div>""", unsafe_allow_html=True)

# PAGE 3: PROBABILITY
elif page == "🎲 Probability":
    st.markdown("# 🎲 Empirical Probability Analysis")
    st.markdown("Understand the likelihood of different demand levels")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        food_item = st.selectbox("Select Food Item:", sorted(df['Item'].unique()), key="prob_food")
    
    with col2:
        item_data = df[df['Item'] == food_item]['Actual_Demand'].values
        default_threshold = int(np.median(item_data))
        threshold = st.slider("📊 Demand Threshold (units):", 
                             int(np.min(item_data)), int(np.max(item_data)), default_threshold, key="prob_threshold")
    
    # Calculate probability
    prob_result = calculate_empirical_probability(df, food_item, threshold)
    
    if prob_result:
        # KPI
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">P(X > {threshold})</div>
            <div style="font-size: 2.5rem; font-weight: 700; color: #0F7C7E;">{prob_result['probability']:.1f}%</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">probability</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Days Above</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0F7C7E;">{prob_result['above_threshold']}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">observations</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Total Obs</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0F7C7E;">{prob_result['total_observations']}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">records</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Mean Demand</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0F7C7E;">{prob_result['mean']:.0f}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">units/day</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Visualization
        st.markdown("---")
        st.markdown("## 📊 Probability Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart
            categories = [f'≤ {threshold}', f'> {threshold}']
            values = [prob_result['below_equal_threshold'], prob_result['above_threshold']]
            colors = ['#1B5E5E', '#E8914C']
            
            fig = go.Figure(data=[
                go.Bar(x=categories, y=values, marker_color=colors,
                      text=values, textposition='auto')
            ])
            fig.update_layout(title=f"{food_item} - Demand vs Threshold ({threshold} units)",
                             yaxis_title='Number of Days', height=400, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gauge/Progress
            prob_pct = prob_result['probability']
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=prob_pct,
                title={'text': f"Probability of Demand > {threshold}"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#0F7C7E"},
                    'steps': [
                        {'range': [0, 25], 'color': "#f0f0f0"},
                        {'range': [25, 50], 'color': "#f0f0f0"},
                        {'range': [50, 75], 'color': "#f0f0f0"},
                        {'range': [75, 100], 'color': "#f0f0f0"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}}
            ))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Insight
        insight_text = get_probability_insight(prob_result)
        st.markdown(f"""<div class="insight-box">{insight_text}</div>""", unsafe_allow_html=True)
        
        # Probability Table
        st.markdown("---")
        st.markdown("## 📋 Probability Statistics")
        
        prob_table = get_probability_statistics(df, food_item)
        st.dataframe(prob_table, use_container_width=True, hide_index=True)

# PAGE 4: CORRELATION
elif page == "🔗 Correlation":
    st.markdown("# 🔗 Correlation Analysis")
    st.markdown("Analyze relationships between variables and demand")
    st.markdown("**Important:** Correlation indicates association, not causation.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        food_item = st.selectbox("Select Food Item:", sorted(df['Item'].unique()), key="corr_food")
    
    with col2:
        variable = st.selectbox("Select Variable:", 
                               ['Students_Present', 'Temperature_C', 'Price'],
                               format_func=lambda x: {'Students_Present': '👥 Student Attendance',
                                                      'Temperature_C': '🌡️ Temperature',
                                                      'Price': '💰 Price'}[x],
                               key="corr_var")
    
    # Calculate correlation
    corr_result = calculate_correlation(df, food_item, variable)
    
    if corr_result:
        # KPI
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            r_value = corr_result['pearson_r']
            color = '#27ae60' if r_value > 0 else '#e74c3c'
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Correlation (r)</div>
            <div style="font-size: 2.2rem; font-weight: 700; color: {color};">{r_value:+.3f}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">Pearson</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">R² Score</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0F7C7E;">{corr_result['r_squared']:.3f}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">{corr_result['r_squared']*100:.1f}% explained</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Strength</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #0F7C7E;">{corr_result['correlation_strength']}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">relationship</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
            <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">P-value</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #0F7C7E;">{corr_result['pearson_pval']:.4f}</div>
            <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">significance</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts
        st.markdown("---")
        st.markdown("## 📊 Correlation Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot with trendline
            item_df = df[df['Item'] == food_item].copy()
            
            fig = px.scatter(item_df, x=variable, y='Actual_Demand',
                           trendline='ols',
                           labels={variable: variable.replace('_', ' '), 'Actual_Demand': 'Demand (units)'},
                           title=f"{variable.replace('_', ' ')} vs {food_item} Demand",
                           color_discrete_sequence=['#0F7C7E'])
            fig.update_traces(marker=dict(size=6, opacity=0.6))
            fig.update_layout(height=400, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Correlation heatmap for all variables
            corr_matrix = get_correlation_matrix(df, food_item)
            
            fig = px.imshow(corr_matrix,
                           labels=dict(x="Variable", y="Variable", color="Correlation"),
                           x=['Students', 'Temp', 'Price', 'Demand', 'Waste %'],
                           y=['Students', 'Temp', 'Price', 'Demand', 'Waste %'],
                           color_continuous_scale='RdBu_r',
                           text_auto='.2f',
                           aspect='auto',
                           title=f"{food_item} - Correlation Matrix")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Insight
        insight_text = get_correlation_insight(corr_result)
        st.markdown(f"""<div class="insight-box">{insight_text}</div>""", unsafe_allow_html=True)

# PAGE 5: PREDICTION
elif page == "🔮 Prediction":
    st.markdown("# 🔮 Demand Prediction Engine")
    st.markdown("Linear Regression Model for Smart Forecasting")
    
    st.markdown("---")
    
    # Input Section
    st.markdown("## 📝 Prediction Inputs")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        food_item = st.selectbox("🍱 Food Item:", sorted(df['Item'].unique()), key="pred_food")
    
    with col2:
        students = st.slider("👥 Expected Students:", 100, 1200, 900, step=50, key="pred_students")
    
    with col3:
        temperature = st.slider("🌡️ Temperature (°C):", 18, 42, 28, step=1, key="pred_temp")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        exam_week = st.checkbox("📚 Exam Week", value=False, key="pred_exam")
    
    with col2:
        holiday = st.checkbox("🎉 Holiday", value=False, key="pred_holiday")
    
    with col3:
        safety_buffer = st.slider("🛡️ Safety Buffer %:", 0, 20, 5, step=1, key="pred_buffer")
    
    # Predict
    model = models[food_item]
    predicted_demand = model.predict(students, temperature, exam_week, holiday)
    recommended_prep = get_prediction_recommendation(predicted_demand, safety_buffer)
    
    # Results
    st.markdown("---")
    st.markdown("## 🎯 Prediction Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-large">
        <h3>Predicted Demand</h3>
        <div class="value">{predicted_demand:.0f}</div>
        <div class="description">units/day</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-large" style="background: linear-gradient(135deg, #1B5E5E 0%, #0F7C7E 100%);">
        <h3>Recommended Prep</h3>
        <div class="value">{recommended_prep}</div>
        <div class="description">units (with {safety_buffer}% buffer)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        item_waste = df[df['Item'] == food_item]['Waste_Percentage'].mean()
        st.markdown(f"""
        <div class="kpi-large" style="background: linear-gradient(135deg, #D4A574 0%, #E8914C 100%);">
        <h3>Expected Waste %</h3>
        <div class="value">{item_waste:.1f}%</div>
        <div class="description">historical average</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Model Coefficients
    st.markdown("---")
    st.markdown("## 📊 Model Details")
    
    coeffs = model.coefficients
    summary = model.get_model_summary()
    metrics = summary['metrics']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Linear Regression Coefficients")
        coeff_df = pd.DataFrame({
            'Variable': ['Intercept', 'Students_Present', 'Temperature_C', 'Exam_Week', 'Holiday'],
            'Coefficient': [
                f"{coeffs['intercept']:.4f}",
                f"{coeffs['Students_Present']:.4f}",
                f"{coeffs['Temperature_C']:.4f}",
                f"{coeffs['Exam_Week']:.4f}",
                f"{coeffs['Holiday']:.4f}"
            ]
        })
        st.dataframe(coeff_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Model Equation:**
        ```
        Demand = β₀ + β₁(Students) + β₂(Temperature) + β₃(ExamWeek) + β₄(Holiday)
        ```
        """)
    
    with col2:
        st.markdown("### Model Performance Metrics")
        
        metrics_df = pd.DataFrame({
            'Metric': ['MAE', 'RMSE', 'R² Score', 'MAPE'],
            'Value': [
                f"{metrics['mae']:.2f}",
                f"{metrics['rmse']:.2f}",
                f"{metrics['r2']:.4f}",
                f"{metrics['mape']:.2f}%"
            ]
        })
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
    
    # Comparison Charts
    st.markdown("---")
    st.markdown("## 📈 Model Validation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Actual vs Predicted
        comparison_df = model.get_predictions_comparison()[:100]
        
        fig = px.scatter(comparison_df, x='Actual', y='Predicted',
                        trendline='ols',
                        title=f"{food_item} - Actual vs Predicted Demand",
                        labels={'Actual': 'Actual Demand', 'Predicted': 'Predicted Demand'},
                        color_discrete_sequence=['#0F7C7E'])
        fig.add_shape(type="line", x0=comparison_df['Actual'].min(), y0=comparison_df['Actual'].min(),
                     x1=comparison_df['Actual'].max(), y1=comparison_df['Actual'].max(),
                     line=dict(dash="dash", color="red"), name="Perfect Prediction")
        fig.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Residuals
        residuals = model.get_residuals()
        
        fig = go.Figure(data=[
            go.Histogram(x=residuals, nbinsx=30, name='Residuals',
                        marker_color='#0F7C7E')
        ])
        fig.update_layout(title="Residual Distribution",
                         xaxis_title='Residual (Actual - Predicted)',
                         yaxis_title='Frequency',
                         height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance Insight
    perf_insight = generate_model_performance_insight(metrics['mae'], metrics['rmse'], metrics['r2'], metrics['mape'])
    st.markdown(f"""<div class="insight-box">{perf_insight}</div>""", unsafe_allow_html=True)

# PAGE 6: WASTE ANALYTICS
elif page == "♻️ Waste Analytics":
    st.markdown("# ♻️ Waste Analytics")
    st.markdown("Analyze food waste patterns and optimize preparation")
    
    st.markdown("---")
    
    # Summary Cards
    st.markdown("## 📊 Overall Waste Summary")
    
    total_summary = calculate_waste_summary(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Total Prepared</div>
        <div style="font-size: 2rem; font-weight: 700; color: #0F7C7E;">{total_summary['total_prepared']:,}</div>
        <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">units</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Total Sold</div>
        <div style="font-size: 2rem; font-weight: 700; color: #27ae60;">{total_summary['total_sold']:,}</div>
        <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">units</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Total Waste</div>
        <div style="font-size: 2rem; font-weight: 700; color: #e74c3c;">{total_summary['total_waste']:,}</div>
        <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">units</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        waste_status, emoji, _ = get_waste_status(total_summary['waste_percentage'])
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size: 0.9rem; color: #2C3E50; margin-bottom: 0.5rem;">Waste %</div>
        <div style="font-size: 2rem; font-weight: 700; color: #e74c3c;">{total_summary['waste_percentage']:.1f}%</div>
        <div style="font-size: 0.8rem; color: #A8B8A8; margin-top: 0.5rem;">{emoji} {waste_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Item Analysis
    st.markdown("---")
    st.markdown("## 🍱 Waste by Food Item")
    
    food_item = st.selectbox("Select Food Item:", sorted(df['Item'].unique()), key="waste_food")
    
    item_summary = calculate_waste_summary(df, food_item)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Daily Waste", f"{item_summary['avg_daily_waste']:.1f} units", "per day")
    
    with col2:
        st.metric("Waste %", f"{item_summary['avg_daily_waste_pct']:.1f}%", "of prepared")
    
    with col3:
        st.metric("Total Waste", f"{item_summary['total_waste']} units", "all time")
    
    with col4:
        st.metric("Financial Loss", f"₹{item_summary['financial_loss']:.0f}", "estimated")
    
    # Charts
    st.markdown("---")
    st.markdown("## 📈 Waste Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Waste trend
        item_df = df[df['Item'] == food_item].copy()
        item_df['Date'] = pd.to_datetime(item_df['Date'])
        daily_waste = item_df.groupby('Date')[['Prepared', 'Sold', 'Waste']].sum().reset_index()
        
        fig = go.Figure(data=[
            go.Bar(x=daily_waste['Date'], y=daily_waste['Waste'], name='Waste', marker_color='#e74c3c'),
            go.Scatter(x=daily_waste['Date'], y=daily_waste['Waste'].rolling(7).mean(), 
                      name='7-day MA', line=dict(color='#0F7C7E', dash='dash'))
        ])
        fig.update_layout(title=f"{food_item} - Daily Waste Trend",
                         xaxis_title='Date', yaxis_title='Waste (units)',
                         height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Waste by day of week
        item_df['DayOfWeek'] = item_df['Date'].dt.day_name()
        waste_by_day = item_df.groupby('DayOfWeek')['Waste_Percentage'].mean().reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        
        fig = px.bar(x=waste_by_day.index, y=waste_by_day.values,
                    title=f"{food_item} - Waste % by Day of Week",
                    labels={'x': 'Day', 'y': 'Waste %'},
                    color_discrete_sequence=['#E8914C'])
        fig.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    # Waste Comparison Table
    st.markdown("---")
    st.markdown("## 📊 Waste by Food Item")
    
    waste_table = get_waste_by_item(df)
    st.dataframe(waste_table, use_container_width=True, hide_index=True)
    
    # Recommendations
    st.markdown("---")
    st.markdown("## 💡 Recommendations")
    
    recommendations = get_waste_recommendations(df, food_item)
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"""
        <div class="insight-box">
        {rec}
        </div>
        """, unsafe_allow_html=True)

# PAGE 7: FOOD COMPARISON
elif page == "🍱 Food Comparison":
    st.markdown("# 🍱 Food Item Comparison")
    st.markdown("Compare all food items across key metrics")
    
    st.markdown("---")
    
    # Summary Table
    st.markdown("## 📊 Food Item Summary")
    
    summary_table = get_all_items_summary(df)
    st.dataframe(summary_table, use_container_width=True, hide_index=True)
    
    # Charts
    st.markdown("---")
    st.markdown("## 📈 Comparative Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Demand comparison
        demand_by_item = df.groupby('Item')['Actual_Demand'].mean().sort_values(ascending=False)
        
        fig = px.bar(x=demand_by_item.index, y=demand_by_item.values,
                    title="🔥 Average Demand by Item",
                    labels={'x': 'Food Item', 'y': 'Avg Demand (units)'},
                    color_discrete_sequence=['#0F7C7E'])
        fig.update_layout(height=400, template='plotly_white', xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Waste comparison
        waste_by_item = df.groupby('Item')['Waste_Percentage'].mean().sort_values(ascending=False)
        
        fig = px.bar(x=waste_by_item.index, y=waste_by_item.values,
                    title="♻️ Average Waste % by Item",
                    labels={'x': 'Food Item', 'y': 'Waste %'},
                    color_discrete_sequence=['#e74c3c'])
        fig.update_layout(height=400, template='plotly_white', xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # More Comparisons
    col1, col2 = st.columns(2)
    
    with col1:
        # Demand Variability
        std_by_item = df.groupby('Item')['Actual_Demand'].std().sort_values(ascending=False)
        
        fig = px.bar(x=std_by_item.index, y=std_by_item.values,
                    title="📊 Demand Variability (Std Dev)",
                    labels={'x': 'Food Item', 'y': 'Standard Deviation'},
                    color_discrete_sequence=['#1B5E5E'])
        fig.update_layout(height=400, template='plotly_white', xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Price vs Demand
        price_demand = df.groupby('Item').agg({
            'Price': 'mean',
            'Actual_Demand': 'mean'
        }).sort_values('Actual_Demand', ascending=False)
        
        fig = px.scatter(price_demand, x='Price', y='Actual_Demand',
                        text=price_demand.index,
                        title="💰 Price vs Demand",
                        labels={'Price': 'Price (₹)', 'Actual_Demand': 'Avg Demand (units)'},
                        color_discrete_sequence=['#E8914C'])
        fig.update_traces(textposition='top center', marker=dict(size=15))
        fig.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

# PAGE 8: DATA EXPLORER
elif page == "📊 Data Explorer":
    st.markdown("# 📊 Data Explorer")
    st.markdown("Explore and download the simulated dataset")
    
    st.markdown("---")
    st.markdown("⚠️ **Simulated Academic Dataset**")
    
    # Filters
    st.markdown("## 🔍 Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_items = st.multiselect(
            "Food Items:",
            sorted(df['Item'].unique()),
            default=sorted(df['Item'].unique())
        )
    
    with col2:
        date_range = st.date_input(
            "Date Range:",
            value=(df['Date'].min().date(), df['Date'].max().date()),
            min_value=df['Date'].min().date(),
            max_value=df['Date'].max().date()
        )
    
    with col3:
        show_columns = st.multiselect(
            "Columns to Show:",
            df.columns.tolist(),
            default=['Date', 'Item', 'Students_Present', 'Actual_Demand', 'Prepared', 'Sold', 'Waste', 'Waste_Percentage']
        )
    
    # Filter data
    filtered_df = df[
        (df['Item'].isin(selected_items)) &
        (df['Date'].dt.date >= date_range[0]) &
        (df['Date'].dt.date <= date_range[1])
    ][show_columns]
    
    # Display
    st.markdown(f"### 📋 Dataset Preview ({len(filtered_df)} records)")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download
    st.markdown("---")
    st.markdown("## 📥 Download")
    
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"smartcanteen_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Statistics
    st.markdown("---")
    st.markdown("## 📊 Dataset Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(filtered_df):,}")
    
    with col2:
        st.metric("Unique Dates", f"{filtered_df['Date'].nunique()}")
    
    with col3:
        st.metric("Food Items", f"{filtered_df['Item'].nunique()}")
    
    with col4:
        st.metric("Date Range", f"{(filtered_df['Date'].max() - filtered_df['Date'].min()).days} days")

# PAGE 9: ABOUT
elif page == "ℹ️ About":
    st.markdown("# ℹ️ About SmartCanteen")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📋 Project Information
        
        **Project Name:** SmartCanteen
        
        **Subject:** Probability, Statistics and Data Analysis (PSDA)
        
        **Purpose:** 
        Demand prediction and food waste reduction system for college canteens
        
        **Type:** Academic Working Model
        """)
    
    with col2:
        st.markdown("""
        ### 💻 Technology Stack
        
        - **Language:** Python
        - **Framework:** Streamlit
        - **Data:** Pandas, NumPy
        - **Visualization:** Plotly
        - **ML:** Scikit-learn
        - **Statistics:** SciPy
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎓 PSDA Concepts Demonstrated
    
    **Descriptive Statistics:**
    - Mean, Median, Mode
    - Variance and Standard Deviation
    - Quartiles and Interquartile Range
    - Data Distribution Analysis
    
    **Probability:**
    - Empirical Probability Calculation
    - Probability Distributions
    - Threshold Analysis
    
    **Correlation Analysis:**
    - Pearson Correlation Coefficient
    - Correlation Strength Interpretation
    - Causation vs Correlation
    
    **Regression & Prediction:**
    - Linear Regression Model
    - Model Coefficients
    - Residual Analysis
    
    **Model Evaluation:**
    - Mean Absolute Error (MAE)
    - Root Mean Squared Error (RMSE)
    - R² Score
    - Mean Absolute Percentage Error (MAPE)
    
    **Data Visualization:**
    - Histograms and Box Plots
    - Scatter Plots with Trendlines
    - Time Series Analysis
    - Heatmaps and Correlation Matrices
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📊 Dataset Information
    
    **Dataset Type:** Simulated Academic Dataset
    
    **Records:** 2,920 observations
    
    **Duration:** 365 days (1 year)
    
    **Food Items:** 8 varieties
    - Samosa, Vada Pav, Sandwich
    - Tea, Coffee, Cold Drink
    - Veg Puff, Maggi
    
    **Features:**
    - Date, Day, Weekend Flag
    - Holiday Flag, Exam Week Flag
    - Student Attendance
    - Temperature (°C)
    - Actual Demand, Prepared, Sold
    - Waste, Waste Percentage
    - Price
    
    **Meaningful Relationships:**
    - Student count affects demand
    - Temperature influences hot/cold item demand
    - Exam periods change consumption patterns
    - Holidays reduce attendance
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 Features
    
    1. **Dashboard:** Real-time prediction and KPI overview
    2. **Statistics:** Comprehensive descriptive analysis
    3. **Probability:** Empirical probability calculations
    4. **Correlation:** Relationship analysis between variables
    5. **Prediction:** Linear regression demand forecasting
    6. **Waste Analytics:** Comprehensive waste analysis
    7. **Food Comparison:** Cross-item comparison
    8. **Data Explorer:** Interactive dataset exploration
    9. **Smart Recommendations:** AI-powered suggestions
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### ⚠️ Important Notes
    
    **Dataset Disclaimer:**
    The dataset included with this project is **simulated for academic demonstration purposes only**. 
    It does not represent actual canteen data.
    
    **Predictions:**
    This system is designed to support better demand planning and potentially reduce unnecessary food preparation. 
    Actual results may vary based on real-world conditions.
    
    **Use Case:**
    This is an academic working model demonstrating PSDA concepts. For production use, 
    consider real historical data and additional factors.
    """)
    
    st.markdown("---")
    
    data_quality_summary = generate_data_quality_summary(df)
    st.markdown(data_quality_summary)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div class="footer-text">
🍽️ <b>SmartCanteen</b> | PSDA Academic Project | Simulated Dataset | 
<i>Turn Data Into Smarter Meals</i>
</div>
""", unsafe_allow_html=True)
