# USA House Price Prediction ML App 🏠📈


This real-world project leverages AI/ML to predict house prices across the United States using core property features and contextual state-level data. Designed for deployment on Streamlit and built for interpretability and production readiness, this project combines model experimentation, API integration, and 2025 market insights to create a highly responsive and realistic real estate price predictor.

---

## 🎯 Project Objective
To build a robust machine learning application that predicts housing prices in the U.S. using real-time geolocation data, engineered features, and economic factors like tax rates and market conditions per state.

This tool is designed for potential homebuyers, real estate analysts, and investors to make informed decisions about property valuations.

---

## 🧠 ML Models and Training Process
We trained and evaluated multiple regression models:

- **Linear Regression**
- **Random Forest Regressor**
- **Decision Tree Regressor**
- **Support Vector Regressor (SVR)**
- **XGBoost Regressor**

### 🔍 Hyperparameter Tuning
- **Tool**: `GridSearchCV`
- **Models Tuned**: Random Forest, Decision Tree
- **Parameters Tuned**:
  - `max_depth`
  - `n_estimators`
  - `min_samples_split`
  - `min_samples_leaf`

### 📊 Train-Test Split
- 80% training / 20% testing
- Stratified sampling was used to ensure consistency in the target distribution.

---

## 📍 Feature Engineering
We narrowed down the input features to the most impactful predictors:
- Number of Bedrooms
- Number of Bathrooms
- Living Area (in sq ft)
- House Condition Rating
- School Quality in the Area

---

## 🌐 API Integration
We integrated the **Nominatim API (OpenStreetMap)** to:
- Convert user-entered addresses into precise latitude/longitude coordinates.
- Automatically fetch and display the ZIP code, enabling more location-aware predictions.

---

## 📈 Market-Level Adjustment (2025 Real Estate Trends)
This model uniquely adjusts predicted prices based on:
- **2025 State Tax Rates**
- **Inflation and Market Forecasting**
- **Real Estate Trends** (gathered from housing reports and regional economics)

Each state has its own economic multiplier embedded in the model to reflect real-world price variation.

---

## 📂 File Structure
```
├── usa-house-price-prediction-ml-app/
│   ├── streamlit_app.py              # Main Streamlit frontend
│   ├── model.pkl                     # Trained ML model (Random Forest)
│   ├── utils.py                      # Utility functions (e.g., API call, preprocessing)
│   ├── requirements.txt             # Required Python libraries
│   ├── README.md                    # Project documentation
```

---

## 🚀 App Features
- 🧮 Predict house prices based on core property features
- 🗺️ Location-aware predictions using geolocation & ZIP
- 📊 Dynamic 2025-adjusted market prices by state
- 📉 Multiple ML models benchmarked
- 🌐 Hosted on Streamlit Cloud for public access

---

## 🧪 KPIs Tracked
- Time to generate prediction (< 1 second)
- MAE / RMSE during testing (reported in console logs)
- Latency for API address resolution
- Input validation coverage
- Regional accuracy against real market trends

---

## 💻 Installation & Usage
### Clone the Repository
```bash
git clone https://github.com/aymanmohammaddev/usa-house-price-prediction-ml-app.git
cd usa-house-price-prediction-ml-app
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Launch Locally
```bash
streamlit run streamlit_app.py
```

### Deploy to Streamlit Cloud
- Push all code, including `model.pkl` and `requirements.txt`
- Set `streamlit_app.py` as the entry point on the Streamlit dashboard

---

## 🧠 Insights & Strategy
This project reflects months of research and iteration to simulate a realistic, localized housing price model. The use of 2025 tax and trend data ensures predictions stay anchored in future conditions. The integration with real-world APIs and inclusion of model tuning adds a strong engineering foundation for expansion and production-level reliability.

---

## 🤖 Technologies and Libraries Used
- Python
- Streamlit
- Scikit-learn
- Pandas, NumPy
- Seaborn, Matplotlib
- Joblib
- Geopy (Nominatim API)
- GridSearchCV

---

 


