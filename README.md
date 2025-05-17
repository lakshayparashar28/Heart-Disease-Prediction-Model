# ❤️ Heart Disease Prediction Web App

A Machine Learning-powered web application that predicts whether a person is likely to have heart disease based on medical inputs. Built using **Python**, **Random Forest Classifier**, and **Streamlit**, this project also stores real-time user data using **MongoDB**. It aims to assist users in understanding their health risks and promote preventive healthcare through AI.

---

## 🔍 Project Overview

The **Heart Disease Prediction Web App** is a major project created as part of my B.Tech in Computer Science at Amity University, Noida. This app takes real-time user health data as input, predicts the presence of heart disease using a trained ML model, and stores all entries in a MongoDB database for future analysis.

---

## 🛠️ Technologies Used

| Component         | Technology                     |
|------------------|--------------------------------|
| Machine Learning | Random Forest, Logistic Regression, Decision Tree |
| Frontend         | Streamlit (Python)             |
| Backend          | Python, Joblib (for model saving) |
| Database         | MongoDB Atlas (Cloud NoSQL DB) |
| Deployment       | Streamlit Cloud + GitHub       |
| IDE              | Jupyter Notebook, VS Code      |

---

## 🧠 ML Model Details

- Dataset: UCI Heart Disease Dataset  
- Features used:
  - `age`, `sex`, `cp` (chest pain type), `trestbps` (resting blood pressure), `chol` (cholesterol), `fbs`, `restecg`, `thalach`, `exang`, `oldpeak`, `slope`, `ca`, `thal`
- Target: `1` → Heart Disease, `0` → No Heart Disease
- Best Model Chosen: **Random Forest Classifier**
- Accuracy Achieved: **~81%**

---

## 🌐 Live App

🔗 [Click here to open the Heart Disease Predictor App](https://yourusername.streamlit.app/)  

---

## 🚀 Features

- ✅ Easy-to-use form for real-time health data input
- ✅ Predicts heart disease risk instantly using ML
- ✅ Stores user submissions to MongoDB database
- ✅ Stylish and modern UI design
- ✅ "Show Data" feature to view stored backend entries

---

## 📦 Installation & Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/heart-disease-predictor.git

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # for Mac/Linux
venv\Scripts\activate     # for Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
