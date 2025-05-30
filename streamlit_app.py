import streamlit as st
import joblib
import numpy as np
import pandas as pd


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

=

    




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
