import streamlit as st
import joblib
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Digital Eye Strain Detection",
    page_icon="👁️",
    layout="centered"
)

# ---------- LOAD CSS ----------
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------- LOAD MODEL ----------
model = joblib.load("digital_eye_strain_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# ---------- TITLE ----------
st.markdown("<h1 class='title'>👁️ Digital Eye Strain Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Predict eye strain based on screen usage habits</p>", unsafe_allow_html=True)

# ---------- INPUT FORM ----------
with st.form("eye_form"):
    age = st.slider("Age", 10, 80, 22)
    screen_time = st.slider("Daily screen time (hours)", 1, 15, 5)

    device = st.selectbox("Primary device used", ["Mobile", "Laptop", "Desktop", "Both"])
    brightness = st.selectbox("Screen brightness level", ["Low", "Medium", "High"])
    night_use = st.selectbox("Screen usage after 10 PM?", ["Yes", "No"])
    distance = st.selectbox("Distance from screen", ["Less than 30cm", "30-50 cm", "More than 50cm"])
    breaks = st.selectbox("How often do you take breaks?", [
        "Regularly (every 20-30 minutes)",
        "Sometimes (every 30-60 minutes)",
        "Rarely",
        "Never"
    ])

    submitted = st.form_submit_button("🔍 Predict Eye Strain")

# ---------- PREDICTION ----------
if submitted:
    input_df = pd.DataFrame([{
        "age": age,
        "screen time": screen_time,
        "primary device": device,
        "brightness level": brightness,
        "screen_after_10pm": night_use,
        "screen_distance": distance,
        "break_frequency": breaks
    }])

    prediction = model.predict(input_df)[0]
    result = label_encoder.inverse_transform([prediction])[0]

    if "No" in result:
        st.markdown(f"<div class='result low'>✅ {result}</div>", unsafe_allow_html=True)
    elif "Mild" in result:
        st.markdown(f"<div class='result medium'>⚠️ {result}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='result high'>🚨 {result}</div>", unsafe_allow_html=True)