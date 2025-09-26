# phase4_extras.py
import streamlit as st
from PIL import Image
import io
import google.generativeai as genai

# -------------------------
# Configure Gemini API
# -------------------------
GEN_API_KEY = "AIzaSyDQqzTww4lcdMggpQPZrTg-EehKwvs-DZo"  # Replace with your Gemini API key
genai.configure(api_key=GEN_API_KEY)

# -------------------------
# Chatbot Interface
# -------------------------
def chatbot_interface():
    st.subheader("AI Farming Assistant")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask me anything about farming:", key="chat_input")
    
    if st.button("Send", key="send_chat_btn") and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Call Gemini ChatCompletion API
        try:
            response = genai.ChatCompletion.create(
                model="gemini-1.5-t",
                messages=st.session_state.chat_history
            )
            reply = response.choices[0].message["content"]
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error contacting Gemini API: {e}")
            reply = "Sorry, I couldn't get a response."

        st.text_area("AI Response", value=reply, height=150)

    # Display chat history
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**AI:** {msg['content']}")

# -------------------------
# Image Upload & Diagnosis Interface
# -------------------------
def image_upload_interface():
    st.subheader("Upload Plant or Soil Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Convert to bytes for processing if needed
        img_bytes = io.BytesIO()
        image.save(img_bytes, format=image.format)
        img_bytes = img_bytes.getvalue()
        
        st.info("Image received. You can integrate a model here to diagnose plant/soil health.")
