# USA House Price Prediction ML App 🏠📈


This real-world project leverages AI/ML to predict house prices across the United States using core property features and contextual state-level data. Designed for deployment on Streamlit and built for testing and production readiness, this project combines model experimentation, API integration, and 2025 market insights to create a highly responsive and realistic real estate price predictor.Test out different house prices and enjoy the model.

---

## 🎯 Project Objective
To build a  machine learning application that predicts housing prices in the U.S. using real-time geolocation data, engineered features, and economic factors like tax rates and market conditions per state.

This tool is designed for potential homebuyers, real estate analysts, and investors to make informed decisions about property valuations.

---

## 🧠 ML Models and Training Process
 Trained and evaluated multiple regression models:

- **Linear Regression**
- **Random Forest Regressor**
- **Decision Tree Regressor**
- **XGBoost Regressor**

### 🔍 Hyperparameter Tuning
- **Tool**: `GridSearchCV`
- **Models Tuned**: Random Forest, Decision Tree


### 📊 Train-Test Split
- 80% training / 20% testing
- Stratified sampling was used to ensure consistency in the target distribution.

---
## 📍 Feature Engineering
Narrowed down the input features to the most impactful predictors:
- Number of Bedrooms
- Number of Bathrooms
- Living Area (in sq ft)
- House Condition Rating
- School Quality in the Area

---

## 🌐 API Integration
 Integrated the **Nominatim API (OpenStreetMap)** to:
- Convert user-entered addresses into precise latitude/longitude coordinates.
- Automatically fetch and display the ZIP code, enabling more location-aware predictions.

---

## 📈 Market-Level Adjustment (2025 Real Estate Trends)
This model uniquely adjusts predicted prices based on:
- **2025 State Tax Rates**
- **Inflation and Market Forecasting Based on 2025**
- **Real Estate Trends** (gathered from housing reports and regional economics)

Each state has its own economic multiplier embedded in the model to reflect real-world price variation with current market conitions.

---
## 📂 Live Demo

- Link to View Complete USA House Price Predictor App : <a href="https://usa-housepricepredictions.streamlit.app/" target="_blank">View USA House Price ML App Here</a>


## 📂 File Structure
```
├── usa-house-price-prediction-ml-app/
│   ├── streamlit_app.py              # Main Streamlit frontend
│   ├── model.pkl                     # Trained ML model 
│   ├── requirements.txt             # Required Python libraries
│   ├── README.md                    # Project documentation
```

---

## 🚀 App Features
- 🧮 Predict house prices based on core property features
- 🗺️ Location-aware predictions using geolocation & ZIP
- 📊 Dynamic 2025-adjusted market prices by state
- 📉 Multiple ML models benchmarked

---

## 🧪 KPIs Tracked
- Time to generate prediction (< 1 second)
-  Latency for API address resolution
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

 


