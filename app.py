import streamlit as st
import joblib
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded
import re

# Define colors and styles at the top
bg_gradient = "linear-gradient(-45deg, #1a1a1a, #2e2e2e, #3d3d3d, #4a4a4a)"  # Dark gradient to maintain black theme
text_color = "#ffffff"
card_color = "#4a4a4a"  # Fully grey to match input fields
input_field_color = "#4a4a4a"  # Grey for all input fields
button_color = "#005fa3"
plus_color = "#00cc00"  # Explicit green for plus sign


# Initialize session state for prediction history and last ZIP code
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_zip' not in st.session_state:
    st.session_state.last_zip = None
if 'last_location_data' not in st.session_state:
    st.session_state.last_location_data = None


# Load model
model = joblib.load("model.pkl")


# Cache geocoding results
@st.cache_data(ttl=3600)  # Cache for 1 hour
def geocode_zip(zip_code):
    try:
        geolocator = Nominatim(user_agent="house_price_app")
        location = geolocator.geocode(f"{zip_code}, USA", timeout=10)
        if location:
            return location.latitude, location.longitude
        return None
    except (GeocoderTimedOut, GeocoderQuotaExceeded) as e:
        return None


@st.cache_data(ttl=3600)  # Cache for 1 hour
def reverse_geocode(lat, lon):
    try:
        geolocator = Nominatim(user_agent="house_price_app")
        address = geolocator.reverse((lat, lon), language='en', timeout=10).raw['address']
        return address.get('state', 'Unknown')
    except (GeocoderTimedOut, GeocoderQuotaExceeded) as e:
        return 'Unknown'


# ------------------- App Styling -----------------------
# Disable sidebar to remove potential white rectangle
st.set_page_config(page_title="USA House Price Prediction App", layout="centered", initial_sidebar_state="collapsed")


# App Title and Header
st.markdown(
    """
    <style>
    .title-container {
        margin-top: 50px; /* Lower the title further */
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="title-container"><h1>🏠 USA House Price Prediction App</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="title-container"><h3>📊 Powered by Machine Learning/AI - Enter House property details below</h3></div>', unsafe_allow_html=True)


# Custom CSS and JavaScript for styling
st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        background: {bg_gradient};
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: {text_color};
    }}


    @keyframes gradient {{
        0% {{background-position: 0% 50%;}}
        50% {{background-position: 100% 50%;}}
        100% {{background-position: 0% 50%;}}
    }}


    .stApp {{
        background-color: rgba(0, 0, 0, 0.9) !important; /* Force black background */
    }}


    .block-container {{
        padding: 0 !important; /* Remove padding to eliminate white space above inputs */
        margin: 0 !important; /* Remove all margins */
        background-color: transparent !important;
        border: none !important;
    }}


    /* Remove any extra containers or cards */
    div[data-testid="stVerticalBlock"] > div:first-child:not(.input-card) {{
        display: none !important; /* Hide any unintended containers above input-card */
    }}


    h1, h2, h3, h4, h5 {{
        color: {text_color};
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }}


    /* Style all input fields consistently */
    .stNumberInput > div > div, .stTextInput > div > div {{
        background-color: {input_field_color} !important; /* Force grey for all inputs */
        border-radius: 12px;
        padding: 10px;
        border: none !important; /* Force remove white borders */
        box-shadow: none !important;
    }}


    /* Ensure number input children inherit the grey */
    .stNumberInput input, .stTextInput input {{
        background-color: {input_field_color} !important; /* Explicitly set input background */
        color: {text_color} !important; /* White text for contrast */
        border: none !important;
    }}


    /* Customize increment/decrement buttons with higher specificity */
    .stNumberInput button[aria-label="Increment"] {{
        color: {plus_color} !important; /* Green for plus */
        font-weight: bold;
        background-color: transparent !important;
        border: none !important; /* Remove white border */
    }}


    .stNumberInput button[aria-label="Decrement"] {{
        color: #ff3333 !important; /* Red for minus */

        font-weight: bold;
        background-color: transparent !important;
        border: none !important; /* Remove white border */
    }}


    .stButton>button {{
        background-color: {button_color};
        color: white;
        font-weight: 600;
        border-radius: 12px;
        padding: 10px 25px;
        margin-top: 0.2rem; /* Keep feedback button up */
        width: 100%;
        border: none;
    }}


    .stButton>button:hover {{
        background-color: #004080;
        color: white;
    }}


    .stSuccess {{
        background-color: #d2f0fc !important;
        border-left: 5px solid #3399ff;
        padding: 20px;
        border-radius: 10px;
        font-size: 1.3em;
        text-align: center;
    }}


    .input-card {{
        padding: 20px;
        margin-bottom: 15px;
        margin-top: 0 !important; /* Remove any top margin */
        background-color: {card_color}; /* Fully grey background */
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: none !important; /* Remove black strip */
    }}


    /* Style the slider for feedback */
    .stSlider > div > div > div > div {{
        background: none !important; /* Remove default dot */
        height: 24px !important;
        width: 24px !important;
        border-radius: 50% !important;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 16px !important;
        color: #00cc00 !important; /* Green emoji */
        content: "⭐" !important; /* Star emoji instead of dot */
    }}


    .stSlider > div > div > div > div::before {{
        content: "⭐"; /* Star emoji as the handle */
        position: absolute;
    }}


    .stSlider > div > div > div {{
        background-color: #333333 !important; /* Dark track */
    }}


    /* Ensure no white sidebar or extra rectangles */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    </style>
    <script>
    function applyIncrementButtonStyles() {{
        const incrementButtons = document.querySelectorAll('.stNumberInput button[aria-label="Increment"]');
        incrementButtons.forEach(button => {{
            button.style.color = '{plus_color}';
            button.style.backgroundColor = 'transparent';
            button.style.border = 'none';
        }});
    }}
    // Run initially
    applyIncrementButtonStyles();
    // Use MutationObserver to handle dynamic rendering
    const observer = new MutationObserver((mutations) => {{
        applyIncrementButtonStyles();
    }});
    observer.observe(document.body, {{ childList: true, subtree: true }});
    </script>
    """,
    unsafe_allow_html=True
)


st.markdown("---")


# ------------------- Input Fields -----------------------
with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    bedrooms = st.number_input("🛏 Bedrooms", min_value=0, value=3, key="bed")
    bathrooms = st.number_input("🛁 Bathrooms", min_value=0, value=2, key="bath")
    livingarea = st.number_input("📐 Living Area (sq ft)", min_value=0, value=1500, key="sqft")
    condition = st.number_input("🏗 Condition/Quality (1-5)", min_value=1, max_value=5, value=3, key="cond")
    numberofschools = st.number_input("🏫 Nearby Schools", min_value=0, value=2, key="schools")
    zip_code = st.text_input("📍 ZIP Code", value="12345", key="zip")
    st.markdown('</div>', unsafe_allow_html=True)


# ------------------- Location-Based Feature -----------------------
st.subheader("🗺 Location Context")
try:
    # Validate ZIP code format (5 digits) and restrict to USA
    if not re.match(r"^\d{5}$", zip_code):
        raise ValueError("ZIP code must be a 5-digit number")
    # Check if ZIP is within valid US range (e.g., 00501-99950, excluding non-US)
    zip_int = int(zip_code)
    if zip_int < 501 or zip_int > 99950 or zip_int in [340, 962, 963, 964, 965, 966, 967, 968, 969]:  # Exclude non-US ZIP ranges
        raise ValueError("ZIP code must be a valid US ZIP code")


    # Check if ZIP code changed or no cached data
    if zip_code != st.session_state.last_zip or st.session_state.last_location_data is None:
        location_data = geocode_zip(zip_code)
        if location_data:
            lat, lon = location_data
            state = reverse_geocode(lat, lon)
            st.session_state.last_location_data = (lat, lon, state)
            st.session_state.last_zip = zip_code
        else:
            raise ValueError("Invalid ZIP code or geocoding failed")
    else:
        lat, lon, state = st.session_state.last_location_data


    
    #State-specific price adjustments
    state_adjustments = {    
   'Alabama': (1.03, "+3% (Moderate growth, low property taxes at 0.38%)"),  # Low taxes, affordable market[](https://www.propertyshark.com/info/property-taxes-by-state/)
    'Alaska': (1.02, "+2% (Stable, remote market with high costs)"),  # Stable but high living costs
    'Arizona': (0.98, "-2% (Oversupply, high risk of price decline)"),  # High risk of price drops[](https://www.cotality.com/insights/articles/us-home-price-insights-march-2025)
    'Arkansas': (1.03, "+3% (Moderate growth, low-cost Midwest)"),  # Affordable, stable growth
    'California': (1.03, "+3% (High demand, affordability issues, 7% mortgage rates)"),  # High costs, locked-in homeowners[](https://lao.ca.gov/LAOEconTax/Article/Detail/793)
    'Colorado': (1.03, "+3% (Stable, tech-driven, moderating prices)"),  # Cooling after boom[](https://worldpopulationreview.com/state-rankings/median-home-price-by-state)
    'Connecticut': (1.06, "+6% (Northeast strength, high property taxes at 1.81%)"),  # Strong market, high taxes[](https://taxfoundation.org/data/all/state/property-taxes-by-state-county/)
    'Delaware': (1.05, "+5% (Moderate growth, urban proximity)"),  # Steady demand
    'Florida': (0.99, "-1% (Oversupply in some markets, high insurance costs)"),  # Risk of price decline[](https://www.cotality.com/insights/articles/us-home-price-insights-march-2025)
    'Georgia': (1.05, "+5% (Sunbelt growth, strong job market)"),  # Hot market, population growth[](https://raleighrealty.com/blog/least-and-most-affordable-states)
    'Hawaii': (0.97, "-3% (Price decline, high home values at $843,723)"),  # Declining prices, high taxes[](https://www.fool.com/money/research/average-house-price-state/)
    'Idaho': (1.02, "+2% (Cooling after boom, high prices at $466,435)"),  # Post-boom correction[](https://worldpopulationreview.com/state-rankings/median-home-price-by-state)
    'Illinois': (1.04, "+4% (Moderate growth, high property taxes at 2.11%)"),  # Urban-driven, high taxes[](https://taxfoundation.org/data/all/state/property-taxes-by-state-county/)
    'Indiana': (1.05, "+5% (Midwest growth, affordable homes)"),  # Strong appreciation potential[](https://realwealth.com/learn/housing-market-predictions/)
    'Iowa': (1.03, "+3% (Stable, low-cost market)"),  # Steady, affordable
    'Kansas': (1.03, "+3% (Stable, agricultural market)"),  # Moderate growth
    'Kentucky': (1.04, "+4% (Moderate growth, affordable housing)"),  # Stable, low-cost
    'Louisiana': (1.02, "+2% (Slower growth, hurricane risks)"),  # Slower market, natural disaster impacts
    'Maine': (1.06, "+6% (Northeast strength, high demand)"),  # Strong regional market
    'Maryland': (1.05, "+5% (High home values at $634,548, urban proximity)"),  # Expensive but stable[](https://www.fool.com/money/research/average-house-price-state/)
    'Massachusetts': (1.06, "+6% (High home values at $247,917, strong market)"),  # Costly, low affordability[](https://www.fool.com/money/research/average-house-price-state/)
    'Michigan': (1.05, "+5% (Affordable homes at $337,608, Detroit growth)"),  # Strong Midwest market[](https://www.fool.com/money/research/average-house-price-state/)
    'Minnesota': (1.04, "+4% (Stable, good income-to-home-value ratio)"),  # Balanced market[](https://www.fool.com/money/research/average-house-price-state/)
    'Mississippi': (1.02, "+2% (Slower growth, low-cost housing)"),  # Affordable, slow market
    'Missouri': (1.03, "+3% (Moderate growth, affordable Midwest)"),  # Stable, low-cost
    'Montana': (1.02, "+2% (Cooling after boom, rural market)"),  # Post-boom stabilization
    'Nebraska': (1.04, "+4% (Stable, strong ROI potential)"),  # Affordable, investment-friendly[](https://raleighrealty.com/blog/least-and-most-affordable-states)
    'Nevada': (1.05, "+5% (Sunbelt, Vegas-driven growth)"),  # Strong demand, urban centers
    'New Hampshire': (1.06, "+6% (Northeast strength, high property taxes)"),  # Strong market, high taxes[](https://taxfoundation.org/data/all/state/property-taxes-by-state-county/)
    'New Jersey': (1.07, "+7% (High demand, highest property taxes at 2.23%)"),  # Expensive, urban-driven[](https://www.propertyshark.com/info/property-taxes-by-state/)
    'New Mexico': (1.02, "+2% (Moderate growth, high risk of price decline)"),  # Cooling market[](https://www.cotality.com/insights/articles/us-home-price-insights-february-2025)
    'New York': (1.05, "+5% (Strong urban markets, high taxes)"),  # Variable but strong[](https://worldpopulationreview.com/state-rankings/median-home-price-by-state)
    'North Carolina': (1.06, "+6% (Hot market, Raleigh growth, strong ROI)"),  # High demand, population growth[](https://raleighrealty.com/blog/least-and-most-affordable-states)
    'North Dakota': (1.02, "+2% (Slower growth, stable economy)"),  # Slow but steady
    'Ohio': (1.05, "+5% (Midwest growth, affordable markets)"),  # Strong appreciation potential[](https://realwealth.com/learn/housing-market-predictions/)
    'Oklahoma': (1.03, "+3% (Moderate growth, low-cost housing)"),  # Affordable, stable
    'Oregon': (1.02, "+2% (Cooling, high prices at $502,215)"),  # Affordability constraints[](https://worldpopulationreview.com/state-rankings/median-home-price-by-state)
    'Pennsylvania': (1.05, "+5% (Moderate urban growth, stable market)"),  # Steady demand
    'Rhode Island': (1.08, "+8% (High price appreciation, small inventory)"),  # Strong Northeast market
    'South Carolina': (1.06, "+6% (Sunbelt, Charleston-driven growth)"),  # Hot market, coastal demand
    'South Dakota': (1.03, "+3% (Stable, rural market)"),  # Moderate growth
    'Tennessee': (1.05, "+5% (Sunbelt, Nashville growth, strong ROI)"),  # High demand, investment-friendly[](https://realwealth.com/learn/housing-market-predictions/)
    'Texas': (0.99, "+1% (Oversupply, price fluctations expected)"),  # High inventory, price drops[](https://www.newsweek.com/texas-faces-major-housing-market-correction-prices-drop-across-state-2070190)
    'Utah': (1.02, "+2% (Cooling after boom, high prices at $544,868)"),  # Post-boom correction[](https://worldpopulationreview.com/state-rankings/median-home-price-by-state)
    'Vermont': (1.08, "+8% (High price appreciation, low inventory)"),  # Strong Northeast market
    'Virginia': (1.05, "+5% (Stable, urban proximity, strong job market)"),  # Steady demand
    'Washington': (1.03, "+3% (Stable, tech-driven, high prices at $595,723)"),  # Cooling, high costs[](https://worldpopulationreview.com/state-rankings/median-home-price-by-state)
    'West Virginia': (1.07, "+7% (High appreciation, lowest prices at $146,578)"),  # Affordable, high growth[](https://raleighrealty.com/blog/least-and-most-affordable-states)
    'Wisconsin': (1.05, "+5% (Midwest growth, stable market)"),  # Strong, affordable
    'Wyoming': (1.02, "+2% (Slower growth, rural market)"),  # Stable, low demand
    'District of Columbia': (0.97, "-3% (Price decline, high costs at $701,895)"),  # Declining prices, low homeownership[](https://worldpopulationreview.com/state-rankings/median-home-price-by-state)
}


    if state in state_adjustments:
        location_multiplier, adjustment_text = state_adjustments[state]
    else:
        location_multiplier = 1.03  # Default for unknown states
        adjustment_text = "+3% (General market)"
   
    # Render map
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], popup=f"ZIP: {zip_code}", tooltip="Estimated Location").add_to(m)
    folium_static(m, width=700, height=300)
   
    # Display adjustment
    st.write(f"Location adjustment for ZIP {zip_code}: {adjustment_text}")
   
    # OpenStreetMap attribution
    st.markdown("Map data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors", unsafe_allow_html=True)


except ValueError as ve:
    # Handle invalid ZIP format or non-US ZIP codes
    lat, lon = 39.8283, -98.5795
    location_multiplier = 1.0
    st.error(f"Error: {str(ve)}. Using default US center location.")
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], popup="Default Location", tooltip="US Center").add_to(m)
    folium_static(m, width=700, height=300)
    st.markdown("Map data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors", unsafe_allow_html=True)
except GeocoderTimedOut:
    # Handle API timeout
    lat, lon = 39.8283, -98.5795
    location_multiplier = 1.0
    st.error("Geocoding timed out. Please try again later. Using default US center location.")
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], popup="Default Location", tooltip="US Center").add_to(m)
    folium_static(m, width=700, height=300)
    st.markdown("Map data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors", unsafe_allow_html=True)
except GeocoderQuotaExceeded:
    # Handle API rate limit
    lat, lon = 39.8283, -98.5795
    location_multiplier = 1.0
    st.error("API rate limit exceeded. Please wait a moment and try again. Using default US center location.")
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], popup="Default Location", tooltip="US Center").add_to(m)
    folium_static(m, width=700, height=300)
    st.markdown("Map data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors", unsafe_allow_html=True)
except Exception as e:
    # Handle other errors
    lat, lon = 39.8283, -98.5795
    location_multiplier = 1.0
    st.error(f"Map rendering or geocoding failed: {str(e)}. Using default US center location.")
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], popup="Default Location", tooltip="US Center").add_to(m)
    folium_static(m, width=700, height=300)
    st.markdown("Map data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors", unsafe_allow_html=True)


# ------------------- Predict Button -----------------------
predictbutton = st.button("🔍 Predict House Price")


# ------------------- Prediction Output -----------------------
if predictbutton:
    if livingarea <= 0:
        st.error("Please enter a valid living area (greater than 0).")
    else:
        X = np.array([[bedrooms, bathrooms, livingarea, condition, numberofschools]])
        try:
            prediction = model.predict(X)[0][0]
            adjusted_prediction = prediction * location_multiplier  # Apply location adjustment
           
            # Store prediction in history
            st.session_state.history.append({
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Living Area': livingarea,
                'Condition': condition,
                'Schools': numberofschools,
                'ZIP Code': zip_code,
                'Price': f"${adjusted_prediction:,.2f}"
            })
           
            st.balloons()
            st.success(f"🏠 Estimated House Price: **${adjusted_prediction:,.2f}**")
        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
else:
    st.info("👈 Enter values above and click **Predict House Price**.")


# ------------------- Prediction History -----------------------
st.subheader("📜 Prediction History")
if st.session_state.history:
    st.table(pd.DataFrame(st.session_state.history))
else:
    st.write("No predictions yet.")


# ------------------- Feedback Form -----------------------
with st.container():
    st.subheader("💬 Feedback")
    feedback = st.slider(
        "How accurate was this prediction? (1 = Poor, 5 = Excellent)",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        key="feedback_slider",
        help="Slide the star to rate the prediction accuracy from 1 (Poor) to 5 (Excellent)"
    )
    if st.button("Submit Feedback", key="feedback_submit"):
        st.success(f"Thank you for your feedback! Rating: {feedback}/5")