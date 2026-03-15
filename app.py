import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
import subprocess

# --- CONFIG ---
st.set_page_config(
    page_title="MindBalance | AI Digital Wellness",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- THEME & STYLING ---
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        * { font-family: 'Outfit', sans-serif; }
        .main { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); color: #ffffff; }
        [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-right: 1px solid rgba(255, 255, 255, 0.1); }
        .stButton>button { background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%); color: white; border-radius: 30px; border: none; padding: 10px 25px; font-weight: 600; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(106, 17, 203, 0.4); }
        .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(106, 17, 203, 0.6); color: white; }
        .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border-radius: 20px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
        h1, h2, h3 { color: #ffffff; font-weight: 700; }
        .highlight-text { background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; }
        .stSlider { color: #2575fc; }
        [data-testid="stMetricValue"] { font-size: 40px; font-weight: 700; color: #00d2ff; }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- HELPER FUNCTIONS ---
def load_model():
    try:
        with open('best_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('features.pkl', 'rb') as f:
            features = pickle.load(f)
        return model, features
    except:
        return None, None

def get_bsmas_result(score):
    if score <= 12:
        return "Balanced User", "green", "Healthy usage pattern detected.", [
            "Maintain current digital boundaries.",
            "Schedule 'Phone-Free' weekends.",
            "Continue focused deep work."
        ]
    elif score <= 18:
        return "Mild Risk (Habitual)", "orange", "Showing signs of habitual dependency.", [
            "Enable App Timers for social media.",
            "Delete apps during exam weeks.",
            "Physical hobby replacement for 30m/day."
        ]
    elif score <= 24:
        return "High Risk Dependency", "red", "Digital habits are impacting mental health.", [
            "Digital Detox for 48 hours.",
            "Use grayscale mode to reduce stimulation.",
            "Uninstall high-attachment apps instantly."
        ]
    else:
        return "Severe Addiction Risk", "darkred", "Urgent digital intervention suggested.", [
            "Consult a therapist for behavioral patterns.",
            "Transition to essential-only apps.",
            "30-day complete social media break."
        ]

# --- NAVIGATION ---
if 'menu' not in st.session_state:
    st.session_state.menu = "Home"

with st.sidebar:
    st.markdown("### MindBalance AI")
    menu = st.radio(
        "Go to", 
        ["Home", "Psychological Assessment", "Dataset Insights", "Screen Time Controller"],
        index=["Home", "Psychological Assessment", "Dataset Insights", "Screen Time Controller"].index(st.session_state.menu),
        key="navigation_radio"
    )
    st.session_state.menu = menu

# --- HOME PAGE ---
if menu == "Home":
    st.markdown("<h1>Decode Your <span class='highlight-text'>Digital Life</span></h1>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("<div class='glass-card'><h3>Real-World Addiction Analysis</h3><p>Move beyond simple tracking. Understand the psychological impact of digital consumption on your sleep, focus, and relationships.</p></div>", unsafe_allow_html=True)
        def start_now(): st.session_state.navigation_radio = "Psychological Assessment"
        st.button("Start Assessment Now", on_click=start_now)
    with c2:
        st.image("website_design.png")

# --- ASSESSMENT ---
elif menu == "Psychological Assessment":
    st.markdown("<h1>Clinical <span class='highlight-text'>Assessment</span></h1>", unsafe_allow_html=True)
    with st.form("assessment"):
        c1, c2, c3 = st.columns(3)
        with c1: age = st.number_input("Age", 16, 25, 20)
        with c2: gender = st.selectbox("Gender", ["Male", "Female"])
        with c3: level = st.selectbox("Academic Level", ["High School", "Undergraduate", "Graduate"])
        
        c4, c5 = st.columns(2)
        with c4: country = st.selectbox("Country", ["India", "USA", "UK", "Other"])
        with c5: platform = st.selectbox("Top Platform", ["Instagram", "Threads", "Snapchat", "YouTube", "LinkedIn", "WhatsApp"])
        
        st.markdown("### BSMAS Survey (1: Rarely - 5: Always)")
        q1 = st.slider("Thinking about it constantly?", 1, 5, 3)
        q2 = st.slider("Urge to use it more?", 1, 5, 3)
        q3 = st.slider("Using to escape problems?", 1, 5, 3)
        q4 = st.slider("Failed to cut down?", 1, 5, 3)
        q5 = st.slider("Restless if prohibited?", 1, 5, 3)
        q6 = st.slider("Negative impact on studies?", 1, 5, 3)
        
        st.markdown("### Daily Metrics")
        usage = st.slider("Daily Usage (Hours)", 0.0, 15.0, 4.0)
        sleep = st.slider("Sleep (Hours)", 3.0, 10.0, 7.0)
        conflicts = st.number_input("Social Conflicts / Week", 0, 20, 1)
        
        submit = st.form_submit_button("Generate AI Report")

    if submit:
        total = q1+q2+q3+q4+q5+q6
        label, color, advice, cures = get_bsmas_result(total)
        st.markdown(f"<h2>Result: <span style='color:{color}'>{label}</span></h2>", unsafe_allow_html=True)
        
        model, _ = load_model()
        if model:
            # Predict
            feat = pd.DataFrame([{
                'Age': age, 'Gender': gender, 'Academic_Level': level, 'Country': country,
                'Avg_Daily_Usage_Hours': usage, 'Most_Used_Platform': platform,
                'Affects_Academic_Performance': "Yes" if q6 >= 4 else "No",
                'Sleep_Hours_Per_Night': sleep, 'Mental_Health_Score': 11-(total//3),
                'Relationship_Status': "Single", 'Conflicts_Over_Social_Media': conflicts
            }])
            prob = model.predict_proba(feat)[0][1]
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Clinical Risk Index", f"{int(prob*100)}%")
                st.write(f"**Advice:** {advice}")
                st.markdown("### 🪴 The Cure")
                for c in cures: st.write(f"✅ {c}")
            with c2:
                fig = go.Figure(go.Indicator(mode="gauge+number", value=prob*100, gauge={'axis':{'range':[0,100]}, 'bar':{'color':color}}))
                st.plotly_chart(fig, use_container_width=True)

# --- INSIGHTS ---
elif menu == "Dataset Insights":
    st.markdown("<h1>Real-Time <span class='highlight-text'>Behavior Analysis</span></h1>", unsafe_allow_html=True)
    try:
        df = pd.read_csv('social_media_addiction_data.csv')
        st.markdown("### Screen Time vs Mental Health Resilience")
        fig = px.scatter(df, x="Avg_Daily_Usage_Hours", y="Mental_Health_Score", color="Status", trendline="ols", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 Data shows a sharp decline in mental resilience after 5 hours of daily usage.")
    except Exception as e:
        st.error(f"Error loading insights: {e}")

# --- SCREEN TIME ---
elif menu == "Screen Time Controller":
    st.markdown("<h1>Active <span class='highlight-text'>Smart Controller</span></h1>", unsafe_allow_html=True)
    
    CONFIG_PATH = 'screen_config.json'
    
    # Load or init config
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    else:
        config = {"limit": 4.0, "status": "active", "start_time": datetime.now().timestamp()}

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("### 🛡️ Automatic Guard Configuration")
    new_limit = st.number_input("Set Your Strict Daily Limit (Hours)", 0.5, 12.0, float(config["limit"]))
    
    if st.button("Activate Real-Time Guard"):
        config["limit"] = new_limit
        config["status"] = "active"
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f)
        
        # Start background process if not running
        subprocess.Popen(["python", "background_monitor.py"], 
                         creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        st.success("Your AI Guard is now running in the background. It will alert your desktop automatically!")

    st.markdown("</div>", unsafe_allow_html=True)
    
    # Live Status
    elapsed = (datetime.now().timestamp() - config["start_time"]) / 3600
    progress_pct = min(1.0, elapsed / new_limit) if new_limit > 0 else 1.0
    
    st.markdown("### 📈 Usage Progress")
    
    # Visual Progress Bar
    bar_color = "green" if progress_pct < 0.7 else "orange" if progress_pct < 1.0 else "red"
    st.progress(progress_pct, text=f"{int(progress_pct * 100)}% of limit consumed")
    
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.metric("Live Session Tracker", f"{elapsed:.2f} Hours", 
                  delta=f"{new_limit - elapsed:.2f}h Left" if elapsed < new_limit else "OVER LIMIT", 
                  delta_color="normal" if elapsed < new_limit else "inverse")
    
    with c_m2:
        # Mini Gauge for Progress
        fig_progress = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = progress_pct * 100,
            number = {'suffix': "%"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': bar_color},
                'steps': [
                    {'range': [0, 70], 'color': "rgba(0, 255, 0, 0.1)"},
                    {'range': [70, 100], 'color': "rgba(255, 165, 0, 0.1)"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 100
                }
            }
        ))
        fig_progress.update_layout(height=200, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig_progress, use_container_width=True)

    if elapsed > new_limit:
        st.error(f"🚨 ALERT: You have exceeded your {new_limit}h limit! The Background Guard is active.")
    
    st.info("💡 Once activated, the Guard works outside the browser. You don't need to keep this website open.")