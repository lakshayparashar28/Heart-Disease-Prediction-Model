import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sqlite3

# Load trained model
model = joblib.load("heart_disease_app/heart_disease_model.pkl")

# Initialize DB
conn = sqlite3.connect("user_data.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_inputs (
                age INTEGER, sex TEXT, cp INTEGER, trestbps INTEGER, chol INTEGER,
                fbs INTEGER, restecg INTEGER, thalach INTEGER, exang INTEGER,
                oldpeak REAL, slope INTEGER, ca INTEGER, thal INTEGER, prediction TEXT
            )''')
conn.commit()

# App UI
st.set_page_config(page_title="❤️ Heart Disease Prediction App", layout="centered")
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        padding: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        color: #d6336c;
        text-align: center;
    }
    .stButton button {
        background-color: #d6336c;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.5em 1em;
    }
    </style>
""", unsafe_allow_html=True)

st.title("❤️ Heart Disease Prediction App")
st.subheader("Enter your health details:")

# Input Fields
age = st.number_input("Age", 1, 120)
sex = st.selectbox("Sex", ["Male", "Female"])
cp = st.selectbox("Chest Pain Type (cp)", [0, 1, 2, 3])
trestbps = st.number_input("Resting Blood Pressure (trestbps)", 80, 200)
chol = st.number_input("Cholesterol (chol)", 100, 600)
fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl (fbs)", [0, 1])
restecg = st.selectbox("Resting ECG (restecg)", [0, 1, 2])
thalach = st.number_input("Max Heart Rate Achieved (thalach)", 60, 220)
exang = st.selectbox("Exercise Induced Angina (exang)", [0, 1])
oldpeak = st.number_input("ST Depression (oldpeak)", 0.0, 6.0, step=0.1)
slope = st.selectbox("Slope of ST (slope)", [0, 1, 2])
ca = st.selectbox("Number of Major Vessels (ca)", [0, 1, 2, 3, 4])
thal = st.selectbox("Thalassemia (thal)", [0, 1, 2, 3])

if st.button("Predict"):
    # Preprocess Input
    input_data = np.array([[age, 1 if sex == "Male" else 0, cp, trestbps, chol,
                            fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
    prediction = model.predict(input_data)[0]
    pred_text = "Yes" if prediction == 1 else "No"

    st.success(f"Prediction: {pred_text} - Heart Disease")

    # Save to DB
    c.execute("INSERT INTO user_inputs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (age, sex, cp, trestbps, chol, fbs, restecg, thalach,
               exang, oldpeak, slope, ca, thal, pred_text))
    conn.commit()

st.markdown("---")
st.subheader("📊 View Saved User Data")

if st.button("Show Data"):
    df = pd.read_sql_query("SELECT * FROM user_inputs", conn)
    st.dataframe(df, use_container_width=True)

conn.close()
