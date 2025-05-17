import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sqlite3

# Load trained model
model = joblib.load("heart_disease_model.pkl")

# Initialize DB
conn = sqlite3.connect("user_data.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_inputs (
                age INTEGER, sex TEXT, cp INTEGER, trestbps INTEGER, chol INTEGER,
                fbs INTEGER, restecg INTEGER, thalach INTEGER, exang INTEGER,
                oldpeak REAL, slope INTEGER, ca INTEGER, thal INTEGER, prediction TEXT
            )''')
conn.commit()

# ========== DARK THEME CONFIG ==========
st.set_page_config(
    page_title="❤️ Heart Disease Prediction App",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    :root {
        --primary: #ff4b4b;
        --background: #0e1117;
        --secondary-background: #1e1e1e;
        --text: #f0f2f6;
    }
    
    .main {
        background-color: var(--background);
        color: var(--text);
        font-family: 'Segoe UI', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary) !important;
    }
    
    .stNumberInput, .stSelectbox, .stSlider {
        background-color: var(--secondary-background);
    }
    
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        color: var(--text) !important;
        background-color: var(--secondary-background) !important;
    }
    
    .stButton>button {
        background-color: var(--primary) !important;
        color: white !important;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.5em 1em;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        opacity: 0.8;
        transform: scale(1.02);
    }
    
    .stDataFrame {
        background-color: var(--secondary-background) !important;
        color: var(--text) !important;
    }
    
    .stAlert {
        background-color: var(--secondary-background) !important;
    }
    
    .stMarkdown {
        color: var(--text) !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== APP UI ==========
st.title("❤️ Heart Disease Prediction App")
st.markdown("---")

# Input Form
with st.form("prediction_form"):
    st.subheader("📝 Patient Health Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=50)
        sex = st.selectbox("Sex", ["Male", "Female"])
        cp = st.selectbox("Chest Pain Type", 
                         options=[0, 1, 2, 3],
                         format_func=lambda x: ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"][x])
        trestbps = st.number_input("Resting Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)
        chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=100, max_value=600, value=200)
        
    with col2:
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1], format_func=lambda x: ["No", "Yes"][x])
        restecg = st.selectbox("Resting ECG Results", options=[0, 1, 2], format_func=lambda x: ["Normal", "ST-T wave abnormality", "Probable LVH"][x])
        thalach = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=150)
        exang = st.selectbox("Exercise Induced Angina", options=[0, 1], format_func=lambda x: ["No", "Yes"][x])
        oldpeak = st.number_input("ST Depression Induced by Exercise", min_value=0.0, max_value=6.0, value=1.0, step=0.1)
    
    slope = st.selectbox("Slope of Peak Exercise ST Segment", options=[0, 1, 2], format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x])
    ca = st.selectbox("Number of Major Vessels", options=[0, 1, 2, 3, 4])
    thal = st.selectbox("Thalassemia", options=[0, 1, 2, 3], format_func=lambda x: ["Normal", "Fixed defect", "Reversible defect", "Not described"][x])
    
    submit_button = st.form_submit_button("🔮 Predict Heart Disease Risk")

# Prediction Logic
if submit_button:
    try:
        # Create input array with correct variable names
        input_data = np.array([[
            age,
            1 if sex == "Male" else 0,  # Corrected sex conversion
            cp,
            trestbps,
            chol,  # Fixed from 'cholera'
            fbs,
            restecg,  # Fixed from 'restec'
            thalach,
            exang,
            oldpeak,
            slope,
            ca,
            thal
        ]])
        
        prediction = model.predict(input_data)[0]
        pred_text = "High Risk ❌" if prediction == 1 else "Low Risk ✅"
        pred_color = "#ff4b4b" if prediction == 1 else "#2ecc71"
        
        st.markdown(f"""
        <div style="background-color:#1e1e1e;padding:1.5rem;border-radius:12px;margin:1rem 0">
            <h3 style="color:{pred_color};text-align:center">Prediction: {pred_text}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Save to DB
        c.execute("INSERT INTO user_inputs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                  exang, oldpeak, slope, ca, thal, pred_text))
        conn.commit()
        
    except Exception as e:
        st.error(f"Error in prediction: {str(e)}")
        st.error("Please check all inputs are filled correctly")

# Data View Section
st.markdown("---")
st.subheader("📊 Saved Patient Records")

if st.button("🔄 Refresh Data"):
    df = pd.read_sql_query("SELECT * FROM user_inputs", conn)
    if not df.empty:
        st.dataframe(df.style.set_properties(**{
            'background-color': '#1e1e1e',
            'color': 'white',
            'border-color': '#3d3d3d'
        }), use_container_width=True)
    else:
        st.warning("No patient records found in database")

conn.close()