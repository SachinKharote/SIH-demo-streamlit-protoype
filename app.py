# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from weather import get_weather
from auth import create_user, login_user, is_valid_email
from deep_translator import GoogleTranslator
import hashlib  # for password hashing
from email_utils import send_registration_email
from auth import create_user, login_user, is_valid_email
import re
import sqlite3
from db_setup import init_db
from fertilizer import recommend_fertilizers, get_crop_season
from market_trends import show_market_trends
from phase4_extras import chatbot_interface, image_upload_interface



init_db()  # ensure the database is ready


# -------------------------
# Load trained ML model
# -------------------------
clf = joblib.load("crop_model.pkl")
le = joblib.load("label_encoder.pkl")

# -------------------------
# Multilingual support
# -------------------------
lang_dict = {"English": "en", "Hindi": "hi", "Marathi": "mr"}
lang = st.sidebar.selectbox("Language", list(lang_dict.keys()))
lang_code = lang_dict[lang]

def translate(text, lang_code):
    if lang_code == "en":
        return text
    try:
        return GoogleTranslator(source='en', target=lang_code).translate(text)
    except Exception:
        return text  # fallback to English if translation fails

# -------------------------
# Streamlit layout
# -------------------------
st.set_page_config(page_title="Smart Crop Planner", layout="wide")

# -------------------------
# User Authentication
# -------------------------
st.sidebar.title(translate("Account", lang_code))
auth_page = st.sidebar.radio(translate("Authentication", lang_code), ["Login", "Register"])

# Initialize session state for user
if "user" not in st.session_state:
    st.session_state.user = None

if auth_page == "Register":
    st.header(translate("Register", lang_code))
    name = st.text_input(translate("Name", lang_code), key="reg_name")
    email = st.text_input(translate("Email", lang_code), key="reg_email")
    password = st.text_input(translate("Password", lang_code), type="password", key="reg_password")
    
    if st.button(translate("Register", lang_code), key="reg_btn"):
        if not create_user.__globals__['is_valid_email'](email):
            st.error(translate("Please enter a valid email address.", lang_code))
        else:
            success, message = create_user(name, email, password)
            if success:
                # Send confirmation email
                email_sent = send_registration_email(email, name)
                if email_sent:
                    st.success(translate("Registration successful! Confirmation email sent. Please login.", lang_code))
                else:
                    st.warning(translate("Registration successful! But email could not be sent.", lang_code))
            else:
                st.error(translate(message, lang_code))

elif auth_page == "Login":
    st.header(translate("Login", lang_code))
    email = st.text_input(translate("Email", lang_code), key="login_email")
    password = st.text_input(translate("Password", lang_code), type="password", key="login_password")
    if st.button(translate("Login", lang_code), key="login_btn"):
        success, message = login_user(email, password)
        if success:
            # Fetch the user details to store in session state
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = c.fetchone()
            conn.close()

            st.session_state.user = user
            st.success(translate(f"Welcome back, {user[1]}!", lang_code))
        else:
            st.error(translate(message, lang_code))



# -------------------------
# Only show app content if user is logged in
# -------------------------
if st.session_state.user:
    user = st.session_state.user  # get persisted user

    # -------------------------
    # Weather Data
    # -------------------------
    city = st.text_input(translate("Enter your city to fetch live weather data:", lang_code), key="city_input")

    if st.button(translate("Get Weather", lang_code), key="weather_btn"):
        weather = get_weather(city)
        if "error" in weather:
            st.error(weather["error"])
        else:
            st.success(f"Weather in {city}: {weather['description'].capitalize()}")
            st.write(f"🌡️ Temperature: {weather['temperature']} °C")
            st.write(f"💧 Humidity: {weather['humidity']} %")
            st.write(f"🌧️ Rainfall: {weather['rainfall']} mm")

    # -------------------------
    # Sidebar Navigation
    # -------------------------
    st.sidebar.title(translate("Navigation", lang_code))
    page = st.sidebar.radio(translate("Go to", lang_code), 
                            ["Home", "Crop Recommendation", "Companion Crop Planner", "Market Insights", "AI Assistant"])

    # -------------------------
    # Home Page
    # -------------------------
    if page == "Home":
        st.title(translate("Smart Crop Planner", lang_code))
        st.subheader(translate("Grow Smart, Earn More", lang_code))
        st.write(translate("This platform helps farmers choose the best crops, companion crops, and see market insights.", lang_code))

    # -------------------------
    # Crop Recommendation
    # -------------------------
    elif page == "Crop Recommendation":
        st.header(translate("Crop Recommendation", lang_code))
        st.write(translate("Enter your farm details below:", lang_code))

        nitrogen = st.slider(translate("Nitrogen (N)", lang_code), 0, 140, 50, key="N_slider")
        phosphorus = st.slider(translate("Phosphorus (P)", lang_code), 5, 145, 50, key="P_slider")
        potassium = st.slider(translate("Potassium (K)", lang_code), 5, 205, 50, key="K_slider")
        temperature = st.number_input(translate("Temperature (°C)", lang_code), -10, 50, 25, key="temp_input")
        humidity = st.slider(translate("Humidity (%)", lang_code), 10, 100, 80, key="hum_slider")
        ph = st.slider(translate("pH Level", lang_code), 0.0, 14.0, 6.5, 0.1, key="ph_slider")

        if st.button(translate("Get Recommendation", lang_code), key="crop_recommend_button"):
            input_df = pd.DataFrame({
                'N': [nitrogen],
                'P': [phosphorus],
                'K': [potassium],
                'temperature': [temperature],
                'humidity': [humidity],
                'ph': [ph]
            })

            # Get prediction probabilities
            pred_probs = clf.predict_proba(input_df)[0]

            # Map encoded labels to crop names
            crop_names = le.inverse_transform(range(len(pred_probs)))

            # Sort top 3 crops
            top3_idx = pred_probs.argsort()[-3:][::-1]
            top3_crops = [(crop_names[i], round(pred_probs[i]*100, 2)) for i in top3_idx]

            # Display
            st.success(translate("Top 3 Recommended Crops:", lang_code))
            for crop, prob in top3_crops:
                st.write(f"{crop}: {prob}%")
                
            # Inside your top 3 crops loop:
            fertilizers = recommend_fertilizers(crop, nitrogen, phosphorus, potassium)
            seasons = get_crop_season(crop)

            if fertilizers:
                st.info(f"Fertilizer Recommendation: {', '.join(fertilizers)}")
            else:
                st.info("No additional fertilizer required")

            st.info(f"Sowing Season: {seasons['sowing']}, Harvesting Season: {seasons['harvesting']}")
            
            # Sort top 3 crops
            top3_idx = pred_probs.argsort()[-3:][::-1]
            top3_crops = [(crop_names[i], round(pred_probs[i]*100, 2)) for i in top3_idx]

            # Store just the crop names in session_state
            st.session_state.top3_crops = [crop for crop, prob in top3_crops]

            # Display Top 3 crops
            st.success(translate("Top 3 Recommended Crops:", lang_code))
            for crop, prob in top3_crops:
                st.write(f"{crop}: {prob}%")
    
        # Fertilizer and season info
        fertilizers = recommend_fertilizers(crop, nitrogen, phosphorus, potassium)
        seasons = get_crop_season(crop)

        if fertilizers:
            st.info(f"Fertilizer Recommendation: {', '.join(fertilizers)}")
        else:
            st.info("No additional fertilizer required")

        st.info(f"Sowing Season: {seasons['sowing']}, Harvesting Season: {seasons['harvesting']}")

 
           # Soil Inputs (Phase 1)
        nitrogen = st.slider(translate("Nitrogen (N)", lang_code), 0, 140, 50, key="N_slider_crop")
        phosphorus = st.slider(translate("Phosphorus (P)", lang_code), 5, 145, 50, key="P_slider_crop")
        potassium = st.slider(translate("Potassium (K)", lang_code), 5, 205, 50, key="K_slider_crop")
        temperature = st.number_input(translate("Temperature (°C)", lang_code), -10, 50, 25, key="temp_input_crop")
        humidity = st.slider(translate("Humidity (%)", lang_code), 10, 100, 80, key="hum_slider_crop")
        rainfall = st.number_input(translate("Rainfall (mm)", lang_code), 0, 500, 100, key="rain_input_crop")
        ph = st.slider(translate("pH Level", lang_code), 0.0, 14.0, 6.5, 0.1, key="ph_slider_crop")
        soil_type = st.selectbox(
            translate("Soil Type", lang_code),
            ["Sandy", "Loamy", "Clayey", "Silty", "Peaty", "Chalky"],
            key="soil_type_select_crop"
)



    # -------------------------
    # Companion Crop Planner
    # -------------------------
    elif page == "Companion Crop Planner":
        st.header(translate("Companion Crop Planner", lang_code))
        st.write(translate("Choose your main crop:", lang_code))
        
        main_crop = st.selectbox(translate("Main Crop", lang_code), ["Banana", "Wheat", "Maize", "Groundnut", "Cowpea"], key="main_crop_select")
        
        if st.button(translate("Get Companion Crops", lang_code), key="companion_button"):
            companion_dict = {
                "Banana": ["Cowpea", "Groundnut", "Maize"],
                "Wheat": ["Mustard", "Lentil", "Chickpea"],
                "Maize": ["Beans", "Sunflower", "Soybean"],
                "Groundnut": ["Maize", "Cowpea"],
                "Cowpea": ["Maize", "Groundnut"]
            }
            companions = companion_dict.get(main_crop, [])
            st.success(translate(f"Recommended Companion Crops for {main_crop}:", lang_code) + " " + ", ".join(companions))

    # -------------------------
    # Market Insights
    # -------------------------
    elif page == "Market Insights":
        st.header(translate("Market Insights", lang_code))
        st.write(translate("Market price trends for your top recommended crops:", lang_code))

    # Get top crops from session_state
        top_crops = st.session_state.get("top3_crops", ["Wheat", "Maize", "Banana"])

    # Call the market trends module
        show_market_trends(top_crops, csv_path=r"F:\SIH demo streamlit\commodity_price.csv")


# -------------------------
# Phase 4 – AI Assistant
# -------------------------
    elif page == "AI Assistant":
        chatbot_interface()
        st.markdown("---")
        image_upload_interface()
        st.header(translate("AI Assistant", lang_code))
        st.write(
            translate(
                "Ask any farming-related question or upload an image for diagnosis.", lang_code
        )
    )

    # Create two columns: left for chatbot, right for image upload
    col1, col2 = st.columns(2)

    # Left column: Chatbot
    with col1:
        st.subheader(translate("Chatbot", lang_code))
        chatbot_interface()

    # Right column: Image Upload
    with col2:
        st.subheader(translate("Plant/Soil Diagnosis", lang_code))
        image_upload_interface()

