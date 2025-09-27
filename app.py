# app.py

import streamlit as st
import pandas as pd
import joblib
import sqlite3
from deep_translator import GoogleTranslator
from weather import get_weather
from auth import create_user, login_user, is_valid_email
from email_utils import send_registration_email
from db_setup import init_db
from fertilizer import recommend_fertilizers, get_crop_season
from market_trends import show_market_trends
from phase4_extras import chatbot_interface, image_upload_interface

# -------------------------
# Streamlit config (must be first Streamlit call)
# -------------------------
st.set_page_config(page_title="Smart Crop Planner", layout="wide")

# -------------------------
# Initialize DB
# -------------------------
init_db()

# -------------------------
# Load ML model
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
        return text  # fallback


# -------------------------
# Authentication
# -------------------------
st.sidebar.title(translate("Account", lang_code))
auth_page = st.sidebar.radio(translate("Authentication", lang_code), ["Login", "Register"])

if "user" not in st.session_state:
    st.session_state.user = None

if auth_page == "Register":
    st.header(translate("Register", lang_code))
    name = st.text_input(translate("Name", lang_code), key="reg_name")
    email = st.text_input(translate("Email", lang_code), key="reg_email")
    password = st.text_input(translate("Password", lang_code), type="password", key="reg_password")

    if st.button(translate("Register", lang_code), key="reg_btn"):
        if not is_valid_email(email):
            st.error(translate("Please enter a valid email address.", lang_code))
        else:
            success, message = create_user(name, email, password)
            if success:
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
# App Content (only if logged in)
# -------------------------
if st.session_state.user:
    user = st.session_state.user

    # Weather
    city = st.text_input(translate("Enter your city to fetch live weather data:", lang_code), key="city_input")
    if st.button(translate("Get Weather", lang_code), key="weather_btn"):
        weather = get_weather(city)
        if "error" in weather:
            st.error(weather["error"])
        else:
            st.success(f"Weather in {city}: {weather['description'].capitalize()}")
            st.write(f"🌡️ {weather['temperature']} °C | 💧 {weather['humidity']} % | 🌧️ {weather['rainfall']} mm")

    # Sidebar Nav
    st.sidebar.title(translate("Navigation", lang_code))
    page = st.sidebar.radio(translate("Go to", lang_code),
                            ["Home", "Crop Recommendation", "Companion Crop Planner", "Market Insights", "AI Assistant"])

    # Home
    if page == "Home":
        st.title(translate("🌱 Smart Crop Planner", lang_code))
        st.subheader(translate("Grow Smart, Earn More", lang_code))
        st.write(translate("This platform helps farmers choose crops, companion crops, and see market insights.", lang_code))

    # Crop Recommendation
    elif page == "Crop Recommendation":
        st.header(translate("Crop Recommendation", lang_code))
        st.write(translate("Enter your farm details:", lang_code))

        nitrogen = st.slider(translate("Nitrogen (N)", lang_code), 0, 140, 50)
        phosphorus = st.slider(translate("Phosphorus (P)", lang_code), 5, 145, 50)
        potassium = st.slider(translate("Potassium (K)", lang_code), 5, 205, 50)
        temperature = st.number_input(translate("Temperature (°C)", lang_code), -10, 50, 25)
        humidity = st.slider(translate("Humidity (%)", lang_code), 10, 100, 80)
        ph = st.slider(translate("pH Level", lang_code), 0.0, 14.0, 6.5, 0.1)

        if st.button(translate("Get Recommendation", lang_code)):
            input_df = pd.DataFrame({
                'N': [nitrogen], 'P': [phosphorus], 'K': [potassium],
                'temperature': [temperature], 'humidity': [humidity], 'ph': [ph]
            })

            pred_probs = clf.predict_proba(input_df)[0]
            crop_names = le.inverse_transform(range(len(pred_probs)))

            top3_idx = pred_probs.argsort()[-3:][::-1]
            top3_crops = [(crop_names[i], round(pred_probs[i]*100, 2)) for i in top3_idx]

            st.session_state.top3_crops = [c for c, _ in top3_crops]

            st.success(translate("Top 3 Recommended Crops:", lang_code))
            for crop, prob in top3_crops:
                st.write(f"{crop}: {prob}%")

                # Fertilizer + season info per crop
                ferts = recommend_fertilizers(crop, nitrogen, phosphorus, potassium)
                seasons = get_crop_season(crop)

                if ferts:
                    st.info(f"{crop} → Fertilizers: {', '.join(ferts)}")
                st.info(f"{crop} → Sowing: {seasons['sowing']}, Harvesting: {seasons['harvesting']}")

    # Companion Crop Planner
    elif page == "Companion Crop Planner":
        st.header(translate("Companion Crop Planner", lang_code))
        main_crop = st.selectbox(translate("Main Crop", lang_code), ["Banana", "Wheat", "Maize", "Groundnut", "Cowpea"])
        if st.button(translate("Get Companion Crops", lang_code)):
            companion_dict = {
                "Banana": ["Cowpea", "Groundnut", "Maize"],
                "Wheat": ["Mustard", "Lentil", "Chickpea"],
                "Maize": ["Beans", "Sunflower", "Soybean"],
                "Groundnut": ["Maize", "Cowpea"],
                "Cowpea": ["Maize", "Groundnut"]
            }
            companions = companion_dict.get(main_crop, [])
            st.success(f"{translate('Recommended:', lang_code)} {', '.join(companions)}")

    # Market Insights
    elif page == "Market Insights":
        st.header(translate("Market Insights", lang_code))
        top_crops = st.session_state.get("top3_crops", ["Wheat", "Maize", "Banana"])
        show_market_trends(top_crops, csv_path="commodity_price.csv")  # ✅ relative path

    # AI Assistant
    elif page == "AI Assistant":
        st.header(translate("AI Assistant", lang_code))
        st.write(translate("Ask any farming-related question or upload an image for diagnosis.", lang_code))
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(translate("Chatbot", lang_code))
            chatbot_interface()
        with col2:
            st.subheader(translate("Plant/Soil Diagnosis", lang_code))
            image_upload_interface()
