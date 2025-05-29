# USA-House-Price-Prediction-ML-App
This application uses machine learning techniques to predict house prices across the United States based on various property features. By analyzing historical real estate data such as living area, number of bedrooms, bathrooms, condition, location, and nearby schools, the app generates price estimates for residential properties.


# 🏠 USA House Price Prediction ML App

## Project Objective
This project delivers a professional-grade machine learning application for predicting house prices across the United States. Designed for real estate professionals, analysts, and investors, the solution uses real-world economic data, optimized machine learning models, and geospatial APIs to deliver accurate, interpretable price predictions in 2025 market conditions. 

The app simplifies prediction to five impactful features while incorporating hyperparameter tuning, economic adjustments, and API-enhanced location intelligence. It is built using Python, scikit-learn, Streamlit, and OpenStreetMap's Nominatim API.

---

## 📊 Dataset Summary

- **Source**: U.S. residential property listings, augmented with school ratings, ZIP code mapping, and state tax policies.
- **Size**: Over 100,000 housing records.
- **Target Variable**: House sale price
- **Key Engineered Features**:
  - Bedrooms
  - Bathrooms
  - Living Area (sq ft)
  - House Condition (1–5 scale)
  - Nearby School Quality Rating
  - Geolocation (via ZIP code → Lat/Long)
  - Adjusted for state-specific 2025 tax policies

---

## ❓ Key Business Questions & KPIs

1. Can minimal, high-impact features predict house prices accurately?
2. What effect do school ratings and property condition have on valuations?
3. How do different U.S. states compare in predicted pricing, adjusted for 2025 tax codes?
4. What is the accuracy tradeoff between model complexity and interpretability?
5. Are hyperparameter-optimized models significantly more robust in generalization?

---

## ⚙️ Model Development & Methodology

### 🧹 Data Processing
- Null values, duplicates, and inconsistent entries were removed.
- ZIP codes were geocoded using the Nominatim API to derive latitude/longitude.
- State-level 2025 housing tax rates were applied as price multipliers for realism.
- School scores and condition were normalized to 0–1 scales where applicable.

### 🧪 Train/Test Split
- Stratified sampling ensured representative pricing across regions.
- Dataset split: 80% for training, 20% for testing.
- Cross-validation used during tuning to prevent overfitting.

### 🧠 Models Evaluated
- **Linear Regression** – Baseline for interpretability.
- **Decision Tree Regressor** – Introduced non-linearity, fast fit.
- **Random Forest Regressor** – Final choice due to balance of accuracy and robustness.

### 🔍 Hyperparameter Tuning
Used `GridSearchCV` with 5-fold cross-validation:
---

## 🖥 App Features (Streamlit)
- Real-time prediction based on user input (5 key features)
- Location-aware mapping using Folium + Nominatim
- State-aware pricing with tax-based adjustments
- Input validation and prediction display UI

---

## 🔧 Technologies Used
- Python, scikit-learn, pandas, numpy
- Streamlit (UI framework)
- Geopy + Nominatim API (geolocation)
- Joblib (model serialization)
- Folium (map rendering)


## 🗺️ How to Run Locally
```bash
# Clone the repo
git clone https://github.com/<your-username>/usa-house-price-prediction-ml-app.git
cd usa-house-price-prediction-ml-app

# Install required libraries
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

--
---

## 💡 Project Insights
- States with higher tax rates (e.g., CA, NY) required adjustments to reflect net cost of ownership.
- School rating showed a high correlation with price even when controlling for ZIP and size.
- Random Forest model delivered reliable accuracy without overfitting.
- The 5 selected features yielded high predictive power, validating the "minimal-input" approach.
- SHAP analysis (in future phase) will be added to visualize feature importance for interpretability.



## 🔗 Live Demo
https://usa-housepricepredictions.streamlit.app/
---

---

© 2025 Ayman Mohammad | MIT License




