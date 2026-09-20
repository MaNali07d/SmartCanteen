# 🚀 SmartCanteen - Quick Start Guide

## ⚡ Get Started in 2 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📚 What to Try First

### 1. Dashboard Page
- Select different food items
- Adjust student attendance
- See real-time predictions
- Modify safety buffer
- Get smart recommendations

### 2. Statistics Page
- Pick any food item
- See mean, median, variance, std dev
- View distribution charts
- Read automatic insights

### 3. Probability Page
- Select a food item
- Set a demand threshold
- See probability of exceeding it
- Understand practical implications

### 4. Prediction Page
- Adjust prediction parameters
- Compare model performance
- See model coefficients
- Understand regression formula

### 5. Waste Analytics
- Analyze waste by item
- See waste trends
- Get recommendations
- Compare across food items

---

## 📊 Dataset Information

✅ **Already Generated:** `smartcanteen_dataset.csv`
- 2,920 records (365 days × 8 food items)
- 8 food items with realistic pricing
- Meaningful relationships between variables
- Simulated academic dataset

To regenerate: `python generate_data.py`

---

## 🎯 Key Features

✨ **Beautiful Dashboard** - Modern SaaS-style interface
📊 **Statistics** - Descriptive analysis with charts
🎲 **Probability** - Empirical probability calculations
🔗 **Correlation** - Multi-variable relationship analysis
🔮 **Prediction** - Linear regression demand forecasting
♻️ **Waste** - Comprehensive waste analytics
🍱 **Comparison** - Cross-item performance analysis
📥 **Data Explorer** - Interactive dataset browser

---

## 🎓 PSDA Concepts Demonstrated

- ✅ Mean, Median, Mode
- ✅ Variance & Standard Deviation
- ✅ Probability Calculations
- ✅ Correlation Analysis
- ✅ Linear Regression
- ✅ Model Evaluation (MAE, R², MAPE)
- ✅ Data Visualization
- ✅ Time Series Analysis

---

## 💡 Example Scenarios

### Scenario 1: Normal Day
- Food: Samosa
- Students: 900
- Temperature: 28°C
- Result: ~121 units (with 5% buffer)

### Scenario 2: Exam Week + Hot
- Food: Cold Drink
- Students: 800
- Temperature: 35°C
- Result: High demand

### Scenario 3: Weekend Holiday
- Food: Any item
- Students: 400 (low attendance)
- Result: Reduced demand

### Scenario 4: What-If Analysis
- Compare 2 scenarios
- See impact on demand
- Make better decisions

---

## 📁 Project Files

```
smartcanteen/
├── app.py                    ← Main application (run this)
├── generate_data.py          ← Dataset generator
├── smartcanteen_dataset.csv  ← Generated data
├── requirements.txt          ← Dependencies
├── README.md                 ← Full documentation
├── QUICKSTART.md            ← This file
└── modules/
    ├── statistics.py         ← Descriptive stats
    ├── probability.py        ← Probability calcs
    ├── correlation.py        ← Correlation analysis
    ├── prediction.py         ← Linear regression
    ├── waste.py              ← Waste analytics
    └── insights.py           ← Insight generation
```

---

## 🔧 Troubleshooting

### App won't start
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check if dataset exists: `smartcanteen_dataset.csv`

### Missing dataset
- Run: `python generate_data.py`
- Check CSV file was created

### Slow performance
- Normal for first load (caching data)
- Subsequent navigation is faster
- Refresh page if stuck

### Import errors
- Reinstall dependencies: `pip install --upgrade -r requirements.txt`
- Use virtual environment: `python -m venv venv && source venv/bin/activate`

---

## 📞 Tips & Tricks

💡 **Use Sidebar:** Easy navigation between pages
💡 **Adjust Inputs:** See predictions update in real-time
💡 **Download Data:** Export filtered dataset as CSV
💡 **Interactive Charts:** Hover for details, zoom, pan
💡 **Try Extremes:** Test with min/max values

---

## 🎓 Learning Outcomes

After exploring SmartCanteen, you'll understand:

✅ How to calculate and interpret statistics
✅ Empirical probability from historical data
✅ Correlation doesn't imply causation
✅ How linear regression models work
✅ Model evaluation metrics explained
✅ Real-world data analysis workflow
✅ Interactive dashboard best practices
✅ Decision-making with data

---

## 📈 Performance Notes

**Model Performance (Samosa example):**
- R² Score: 0.87 (explains 87% of variation)
- MAE: 11 units (average error)
- MAPE: ~9% (percentage accuracy)

Models perform well but should be used with domain expertise.

---

## ✨ UI Highlights

🎨 **Color Scheme:**
- Teal (#0F7C7E) - Primary
- Orange (#E8914C) - Accent
- Cream (#F5F1ED) - Background

📱 **Responsive Design:**
- Works on desktop and tablet
- Mobile-friendly navigation
- Touch-friendly controls

⚡ **Performance:**
- Data cached for speed
- Interactive charts
- Real-time updates

---

## 🚀 Next Steps

1. **Explore:** Try all pages and features
2. **Experiment:** Adjust parameters and observe changes
3. **Analyze:** Read insights and understand patterns
4. **Learn:** Review code and documentation
5. **Customize:** Modify for your needs (optional)

---

## 📚 More Information

- See **README.md** for full documentation
- Check **About page** in the app for concepts
- Review **module files** for implementation details

---

**Ready? Run: `streamlit run app.py`**

🍽️ **SmartCanteen** | Turn Data Into Smarter Meals
