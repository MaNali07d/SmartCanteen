# 🚀 SmartCanteen - Installation & Verification Guide

## ✅ Complete Setup Instructions

Follow these steps to get SmartCanteen running on your computer.

---

## Prerequisites

### What You Need
- **Python 3.8 or higher** (download from python.org)
- **pip** (comes with Python)
- **Terminal/Command Prompt** access
- **~500 MB** disk space

### Check Your Python
```bash
python --version
```
Should show: `Python 3.8.0` or higher

---

## Installation Steps

### Step 1: Extract Project Files
1. Download/extract all files to a folder
2. Remember the folder path
3. Open Terminal/Command Prompt

### Step 2: Navigate to Project
```bash
cd /path/to/smartcanteen
```

Example on Windows:
```bash
cd C:\Users\YourName\Downloads\smartcanteen
```

Example on Mac/Linux:
```bash
cd ~/Downloads/smartcanteen
```

### Step 3: Create Virtual Environment (Optional but Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- streamlit (web framework)
- pandas (data handling)
- numpy (math)
- plotly (charts)
- scikit-learn (machine learning)
- scipy (statistics)

### Step 5: Verify Installation
```bash
python -c "import streamlit, pandas, numpy, plotly, sklearn; print('✓ All packages installed successfully')"
```

### Step 6: Check Dataset
```bash
ls smartcanteen_dataset.csv
```
Should show: `smartcanteen_dataset.csv` exists (211 KB)

### Step 7: Run Application
```bash
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.
  
  Local URL: http://localhost:8501
```

Browser opens automatically. If not, manually visit: `http://localhost:8501`

---

## ✅ Verification Checklist

### After Running App

**Check 1: Dashboard Page**
- [ ] Page loads without errors
- [ ] Sidebar shows all 9 pages
- [ ] KPI cards display (Predicted Demand, Recommended Prep, etc.)
- [ ] Sliders work (adjust students, temperature)
- [ ] Charts render (Demand Trend, Prepared vs Sold)

**Check 2: Statistics Page**
- [ ] Can select different food items
- [ ] Statistics table shows 11 metrics
- [ ] Histogram, Box Plot, and Trend charts display
- [ ] Insight text is generated

**Check 3: Probability Page**
- [ ] Threshold slider works
- [ ] P(X > threshold) calculated
- [ ] Gauge chart displays
- [ ] Probability statistics table shows

**Check 4: Correlation Page**
- [ ] Can select variable (Students/Temperature/Price)
- [ ] Scatter plot with trendline appears
- [ ] Correlation heatmap displays (5x5)
- [ ] r value and R² shown

**Check 5: Prediction Page**
- [ ] All input controls work (sliders, checkboxes)
- [ ] 3 KPI cards display (Predicted, Recommended, Expected Waste)
- [ ] Model coefficients table appears
- [ ] Model performance metrics shown
- [ ] Actual vs Predicted chart displays
- [ ] Residual histogram shows

**Check 6: Waste Analytics Page**
- [ ] Overall waste summary (4 KPI cards)
- [ ] Can select food item
- [ ] Waste trend chart displays
- [ ] Waste by day-of-week chart displays
- [ ] Waste comparison table shows

**Check 7: Food Comparison Page**
- [ ] Summary table shows all 8 items
- [ ] Demand ranking chart displays
- [ ] Waste % ranking chart displays
- [ ] Variability chart displays
- [ ] Price vs Demand scatter plot displays

**Check 8: Data Explorer Page**
- [ ] Can filter by food items
- [ ] Date range picker works
- [ ] Can select columns to display
- [ ] CSV download button works
- [ ] Filtered data shows in table

**Check 9: About Page**
- [ ] Project information displays
- [ ] Technology stack listed
- [ ] PSDA concepts explained
- [ ] Dataset info shown
- [ ] Data quality summary displayed

---

## 🔍 Troubleshooting

### Issue: Python not found
**Solution:**
```bash
python3 --version  # Try python3 instead
```

### Issue: pip not found
**Solution:**
```bash
python -m pip install -r requirements.txt
```

### Issue: Module not found (streamlit, pandas, etc.)
**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Dataset CSV not found
**Solution:**
```bash
python generate_data.py
```
This regenerates: `smartcanteen_dataset.csv`

### Issue: Charts not displaying
**Solution:**
1. Refresh browser (F5)
2. Clear cache (Ctrl+Shift+Delete)
3. Restart app (press Ctrl+C, then `streamlit run app.py`)

### Issue: App runs very slowly
**Solution:**
1. First load caches data (normal)
2. Subsequent navigation is faster
3. Close other browser tabs
4. Restart app

### Issue: Port 8501 already in use
**Solution:**
```bash
streamlit run app.py --server.port=8502
```

### Issue: Permission denied on Linux/Mac
**Solution:**
```bash
chmod +x app.py
```

---

## 📊 Performance Benchmarks

After proper installation, expect:

| Task | Time |
|------|------|
| App startup | 2-3 seconds |
| Page navigation | <1 second |
| Prediction | <100ms |
| Chart rendering | Smooth, interactive |
| Data loading | Once, then cached |

---

## 🧪 Test Predictions

After app is running, try these:

### Test 1: Samosa Prediction
- Food Item: **Samosa**
- Students: **900**
- Temperature: **28°C**
- Exam Week: **No**
- Holiday: **No**
- Safety Buffer: **5%**

**Expected Result:** ~121 units recommended

### Test 2: Cold Drink in Summer
- Food Item: **Cold Drink**
- Students: **900**
- Temperature: **35°C** (hot!)
- Safety Buffer: **10%**

**Expected Result:** High demand (temperature effect)

### Test 3: Tea in Winter
- Food Item: **Tea**
- Students: **900**
- Temperature: **20°C** (cold)
- Safety Buffer: **5%**

**Expected Result:** Higher than hot weather

### Test 4: Exam Week
- Food Item: **Any**
- Exam Week: **Yes**

**Expected Result:** Different demand pattern

---

## 🔧 Configuration Options

### Default Settings
| Setting | Value | Range |
|---------|-------|-------|
| Students | 900 | 100-1200 |
| Temperature | 28°C | 18-42°C |
| Safety Buffer | 5% | 0-20% |
| Bins (histogram) | 30 | - |
| Data cache | Always | - |

### To Change Settings
Edit `app.py` and look for:
```python
# Sliders with st.slider()
students = st.slider("👥 Expected Students", 100, 1200, 900, step=50)
# Change 900 to your default value
```

---

## 📁 File Structure After Setup

```
smartcanteen/
├── app.py                          ✓ Main application
├── generate_data.py                ✓ Data generator
├── smartcanteen_dataset.csv        ✓ Generated data
├── requirements.txt                ✓ Dependencies
├── README.md                       ✓ Documentation
├── QUICKSTART.md                   ✓ Quick guide
├── PROJECT_SUMMARY.md              ✓ Technical details
├── FEATURES.txt                    ✓ Feature list
├── INSTALLATION_GUIDE.md           ✓ This file
├── START_HERE.md                   ✓ Quick start
├── modules/                        ✓ Python modules
│   ├── __init__.py
│   ├── statistics.py
│   ├── probability.py
│   ├── correlation.py
│   ├── prediction.py
│   ├── waste.py
│   └── insights.py
└── venv/                          (optional - virtual environment)
```

---

## ✅ Pre-Flight Checklist

Before running the app, verify:

- [ ] Python 3.8+ installed
- [ ] Project files extracted
- [ ] Terminal opened in project folder
- [ ] Virtual environment activated (if using)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Dataset file exists (`smartcanteen_dataset.csv`)
- [ ] All Python files present (app.py, modules/, etc.)
- [ ] Port 8501 available (or use different port)

---

## 🚀 Launch Commands

### First Time Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run app
streamlit run app.py
```

### Subsequent Times
```bash
# Activate environment (if using venv)
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Run app
streamlit run app.py
```

---

## 📞 Getting Help

### Error Messages
1. Read error message carefully
2. Check error is listed in "Troubleshooting" section
3. Follow suggested solution
4. Test again

### Module Import Errors
```bash
pip list  # Check installed packages
pip install --upgrade -r requirements.txt  # Reinstall
```

### Data Issues
```bash
python generate_data.py  # Regenerate dataset
python -c "import pandas as pd; df = pd.read_csv('smartcanteen_dataset.csv'); print(len(df))"
# Should print: 2920
```

---

## 🎓 Environment Variables (Advanced)

Optional, for advanced users:

```bash
# Set Python path (if needed)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Set Streamlit config
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_HEADLESS=true
```

---

## 📈 System Requirements

### Minimum
- CPU: Dual-core processor
- RAM: 4 GB
- Storage: 500 MB
- Python 3.8+

### Recommended
- CPU: Quad-core processor
- RAM: 8 GB
- Storage: 1 GB
- Python 3.10+
- Modern browser (Chrome, Firefox, Edge)

---

## ✨ Optimization Tips

### Faster Startup
1. Use virtual environment (faster imports)
2. Pre-install all dependencies
3. Close other applications

### Better Performance
1. Use Chrome/Firefox (smoother)
2. Disable browser extensions
3. Don't run other memory-intensive apps

### Smooth Charts
1. Use updated GPU drivers
2. Ensure JavaScript enabled in browser
3. Use modern browser version

---

## 🔒 Security Notes

- App runs locally (no data sent anywhere)
- Dataset is simulated (academic purposes only)
- No internet connection required
- All computations done on your machine

---

## 📊 After Installation - Next Steps

1. **Read START_HERE.md** - Quick orientation
2. **Run the app** - `streamlit run app.py`
3. **Explore all pages** - Try each feature
4. **Read README.md** - Detailed documentation
5. **Modify if needed** - Customize for your needs

---

## 🎉 Success!

If you see:
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

**Congratulations! Installation is complete.**

Browser automatically opens. If not, visit: `http://localhost:8501`

---

## 📞 Support Resources

In This Project:
- `START_HERE.md` - Quick guide
- `QUICKSTART.md` - 2-minute setup
- `README.md` - Complete documentation
- `PROJECT_SUMMARY.md` - Technical details
- `FEATURES.txt` - Visual feature breakdown
- Code comments - In Python files

---

**Next: Run `streamlit run app.py` and enjoy SmartCanteen! 🍽️**
