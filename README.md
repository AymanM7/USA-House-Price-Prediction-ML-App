# USA-House-Price-Prediction-ML-App
This application uses machine learning techniques to predict house prices across the United States based on various property features. By analyzing historical real estate data such as living area, number of bedrooms, bathrooms, condition, location, and nearby schools, the app generates price estimates for residential properties.


# 🏠 USA House Price Prediction ML App

## Project Objective  
This project delivers a production-grade machine learning application to predict house prices in the United States using real-time, geolocated features and economic factors relevant to 2025. It is designed for real estate analysts, home buyers, and tech-savvy investors to get accurate home price predictions based on minimal but highly influential features.

The model incorporates Random Forest and Linear Regression, hyperparameter optimization, location-based API integration, and state-specific tax adjustments. The app is deployed using Streamlit and allows user interactivity through geospatial visualizations and real-time predictions.

---

## 📂 Dataset  

- **Source**: U.S. housing market datasets + custom augmentation  
- **Volume**: 100,000+ rows  
- **Final Features Used**:
  - 🛏 Bedrooms
  - 🛁 Bathrooms
  - 📏 Living Area (sq ft)
  - 🧱 House Condition (1–5 scale)
  - 🏫 Nearby School Rating
  - 🌎 ZIP Code (converted to lat/long)
  - 🧾 State Tax Adjustment for 2025

---

## ❓ Key Questions / KPIs

1. What is the predicted house price based on 5 key attributes?
2. How do 2025 tax policies affect pricing across different states?
3. What’s the MAE and R² score for each ML model tested?
4. Do homes near better schools consistently have higher price predictions?
5. Can minimal features still provide high accuracy in regression modeling?
6. Which state shows the highest average predicted price in 2025?
7. Does home condition affect price more than school quality?

---

## ⚙️ ML Models Used  

| Model               | MAE     | R² Score | Notes                          |
|--------------------|---------|----------|-------------------------------|
| Linear Regression  | $27,300 | 0.71     | Simple, interpretable         |
| Decision Tree      | $21,500 | 0.82     | Sensitive to outliers         |
| Random Forest (🏆) | $18,700 | 0.89     | Best after tuning             |

- 🧠 Final model trained with `GridSearchCV`
- 🧾 Serialized with `joblib` → `model.pkl`

---

## 🔧 Process  

1. **Data Engineering**
   - Removed outliers, nulls, and inconsistent entries
   - Augmented data with ZIP→Lat/Long via Nominatim API
   - Applied 2025 state-level tax adjustment multipliers

2. **Feature Selection**
   - Selected top 5 features based on correlation and SHAP values
   - Avoided overfitting through minimal dimensionality

3. **Modeling & Evaluation**
   - Split data 80/20
   - Trained models and optimized Random Forest using GridSearchCV
   - Evaluated using MAE, R² Score, and Residual Analysis

4. **App Development**
   - Built UI using Streamlit
   - Integrated interactive map with Folium
   - Allowed user to input features to generate live predictions

---

## 🗺️ API & Libraries  

- 📍 **Nominatim API (OpenStreetMap)** – convert ZIP to geolocation  
- 🐍 **Python Libraries**:
  - `pandas`, `numpy`, `scikit-learn`
  - `geopy`, `joblib`, `folium`, `streamlit`, `matplotlib`

---

## 🖥 How to Use / Run Locally  

```bash
# Step 1: Clone the repo
git clone https://github.com/<your-username>/usa-house-price-prediction-ml-app.git  
cd usa-house-price-prediction-ml-app  

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run the Streamlit app
streamlit run streamlit_app.py


