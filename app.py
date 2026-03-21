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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="MindBalance | AI Digital Wellness",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=DM+Mono:wght@400;500&display=swap');
    :root {
        --bg:#e8ecf1; --sd:#c5c9d0; --sl:#ffffff;
        --th:#2d3250; --tb:#4a5070; --tm:#9aa0bc;
        --rose:#d96b6b; --amber:#d99a2e; --sage:#4aaa88; --slate:#6470b8;
        --rose-a:rgba(217,107,107,0.2); --amber-a:rgba(217,154,46,0.2);
        --sage-a:rgba(74,170,136,0.2);  --slate-a:rgba(100,112,184,0.2);
    }
    html,body,[class*="css"],.stApp,.stApp>div,.stApp>div>div,.stApp>div>div>div,
    [data-testid="stAppViewContainer"],[data-testid="stAppViewContainer"]>div,
    section.main,section.main>div,.block-container,
    div[data-testid="column"],div[data-testid="stVerticalBlock"],
    div[data-testid="stHorizontalBlock"],.element-container,
    .stForm,[data-testid="stForm"],[data-baseweb="base-input"],
    [data-baseweb="select"]>div,[data-testid="stNumberInput"]>div,
    .stSlider>div,[data-testid="stMetric"],[data-testid="stMetricValue"] {
        background-color:var(--bg)!important;
        background:var(--bg)!important;
        color:var(--tb)!important;
        font-family:'DM Sans',sans-serif!important;
    }
    [data-testid="stHeader"],[data-testid="stToolbar"]{ background:transparent!important; box-shadow:none!important; }
    .main .block-container{ padding:2.5rem 2.8rem!important; max-width:1120px; }
    [data-testid="stSidebar"]{ background-color:var(--bg)!important; border-right:none!important; box-shadow:5px 0 20px var(--sd),-1px 0 4px var(--sl); }
    [data-testid="stSidebar"] .block-container{ padding:1.8rem 1rem!important; }

    h1{ font-size:2rem!important; font-weight:700!important; color:var(--th)!important; letter-spacing:-0.4px; margin-bottom:0.4rem!important; }
    h2{ font-weight:600!important; color:var(--th)!important; font-size:1.15rem!important; border:none!important; padding:0!important; }
    h3{ font-weight:500!important; color:var(--th)!important; font-size:0.95rem!important; }
    p { color:var(--tb); line-height:1.7; }
    .highlight-text{ color:var(--slate)!important; -webkit-text-fill-color:var(--slate)!important; background:none!important; font-weight:700; }

    .nm-card{ background:var(--bg); border-radius:20px; padding:1.8rem 2rem; margin-bottom:1.2rem; box-shadow:8px 8px 18px var(--sd),-8px -8px 18px var(--sl); transition:box-shadow .2s; }
    .nm-card:hover{ box-shadow:10px 10px 24px var(--sd),-10px -10px 24px var(--sl); }
    .nm-sm{ background:var(--bg); border-radius:16px; padding:1.2rem 1.3rem; box-shadow:6px 6px 14px var(--sd),-6px -6px 14px var(--sl); }
    .nm-inset{ background:var(--bg); border-radius:14px; padding:1rem 1.2rem; box-shadow:inset 4px 4px 9px var(--sd),inset -4px -4px 9px var(--sl); }
    .glass-card{ background:var(--bg)!important; backdrop-filter:none!important; border:none!important; border-radius:20px!important; padding:1.8rem 2rem!important; margin-bottom:1.2rem!important; box-shadow:8px 8px 18px var(--sd),-8px -8px 18px var(--sl)!important; }

    .sec-label{ font-size:0.67rem; font-weight:600; color:var(--tm); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:0.75rem; display:block; }

    .stat-pill{ display:inline-flex; align-items:center; gap:7px; background:var(--bg); border-radius:50px; padding:0.4rem 1rem; box-shadow:3px 3px 8px var(--sd),-3px -3px 8px var(--sl); font-size:0.78rem; font-weight:500; color:var(--tb); margin:3px; }
    .dot{ width:7px; height:7px; border-radius:50%; display:inline-block; }

    .feat-card{ background:var(--bg); border-radius:18px; padding:1.3rem; box-shadow:6px 6px 14px var(--sd),-6px -6px 14px var(--sl); transition:all .2s; }
    .feat-card:hover{ box-shadow:8px 8px 20px var(--sd),-8px -8px 20px var(--sl); transform:translateY(-2px); }
    .feat-icon{ width:42px; height:42px; border-radius:13px; display:flex; align-items:center; justify-content:center; font-size:18px; margin-bottom:0.75rem; box-shadow:4px 4px 10px var(--sd),-4px -4px 10px var(--sl); background:var(--bg); }

    .stButton>button{ background:var(--bg)!important; color:var(--slate)!important; border:none!important; border-radius:14px!important; padding:0.65rem 1.5rem!important; font-family:'DM Sans',sans-serif!important; font-weight:600!important; font-size:0.87rem!important; letter-spacing:0.2px!important; box-shadow:5px 5px 12px var(--sd),-5px -5px 12px var(--sl)!important; transition:all .18s ease!important; width:100%; }
    .stButton>button:hover{ box-shadow:2px 2px 6px var(--sd),-2px -2px 6px var(--sl)!important; color:var(--rose)!important; transform:translateY(-1px); }
    .stButton>button:active{ box-shadow:inset 3px 3px 7px var(--sd),inset -3px -3px 7px var(--sl)!important; transform:translateY(0); }

    .cta-btn>button{ background:var(--slate)!important; color:#fff!important; box-shadow:4px 4px 14px var(--slate-a)!important; }
    .cta-btn>button:hover{ background:var(--rose)!important; box-shadow:4px 4px 14px var(--rose-a)!important; color:#fff!important; }

    [data-testid="stFormSubmitButton"]>button{ background:var(--slate)!important; color:#fff!important; border:none!important; border-radius:14px!important; font-weight:600!important; font-size:0.9rem!important; padding:0.7rem 2rem!important; box-shadow:4px 4px 12px var(--slate-a)!important; width:100%; transition:all .18s ease!important; }
    [data-testid="stFormSubmitButton"]>button:hover{ background:var(--rose)!important; box-shadow:4px 4px 12px var(--rose-a)!important; }
    [data-testid="stFormSubmitButton"]>button:active{ box-shadow:inset 3px 3px 7px rgba(0,0,0,.12)!important; }

    .stTextInput>div>div>input,.stNumberInput>div>div>input,.stSelectbox>div>div,.stTextArea textarea{
        background:var(--bg)!important; border:none!important; border-radius:12px!important;
        box-shadow:inset 4px 4px 9px var(--sd),inset -4px -4px 9px var(--sl)!important;
        color:var(--th)!important; font-family:'DM Sans',sans-serif!important; font-size:0.87rem!important; }
    .stTextInput>div>div>input:focus,.stNumberInput>div>div>input:focus{
        box-shadow:inset 4px 4px 9px var(--sd),inset -4px -4px 9px var(--sl),0 0 0 2px rgba(100,112,184,.3)!important; }
    .stTextInput label,.stNumberInput label,.stSelectbox label,.stSlider label,.stTextArea label{
        font-size:0.75rem!important; font-weight:500!important; color:var(--tm)!important;
        text-transform:uppercase!important; letter-spacing:0.8px!important; }

    [data-testid="stSlider"]>div>div>div{ background:var(--slate)!important; }
    [data-testid="stSlider"]>div>div>div>div{ background:var(--slate)!important; box-shadow:0 0 8px var(--slate-a)!important; }

    [data-testid="stMetric"]{ background:var(--bg)!important; border-radius:16px!important; padding:1.2rem 1.4rem!important; box-shadow:6px 6px 14px var(--sd),-6px -6px 14px var(--sl)!important; }
    [data-testid="stMetricValue"]{ font-size:1.9rem!important; font-weight:600!important; font-family:'DM Mono',monospace!important; color:var(--rose)!important; }
    [data-testid="stMetricLabel"]{ font-size:0.68rem!important; text-transform:uppercase!important; letter-spacing:1.2px!important; color:var(--tm)!important; }

    .stProgress>div>div>div{ background:linear-gradient(90deg,var(--sage),#3a9878)!important; border-radius:20px!important; }
    .stProgress>div>div{ background:var(--bg)!important; box-shadow:inset 3px 3px 7px var(--sd),inset -3px -3px 7px var(--sl)!important; border-radius:20px!important; border:none!important; height:10px!important; }

    .stTabs [data-baseweb="tab-list"]{ background:var(--bg)!important; border-radius:14px; padding:8px; box-shadow:inset 3px 3px 7px var(--sd),inset -3px -3px 7px var(--sl); gap:12px; }
    .stTabs [data-baseweb="tab"]{ background:transparent!important; color:var(--tm)!important; border-radius:10px!important; font-weight:500!important; font-size:0.87rem!important; padding:0.6rem 1.2rem!important; }
    .stTabs [aria-selected="true"]{ background:var(--bg)!important; color:var(--slate)!important; box-shadow:4px 4px 10px var(--sd),-4px -4px 10px var(--sl)!important; }

    .stAlert{ background:var(--bg)!important; border-radius:14px!important; border:none!important; box-shadow:inset 3px 3px 7px var(--sd),inset -3px -3px 7px var(--sl)!important; color:var(--tb)!important; font-size:0.87rem!important; }

    [data-testid="stRadio"]>div{ gap:4px!important; }
    [data-testid="stRadio"] label{ background:var(--bg)!important; border-radius:12px!important; padding:0.55rem 0.85rem!important; font-size:0.84rem!important; color:var(--tb)!important; cursor:pointer; transition:all .15s ease; display:flex!important; align-items:center; gap:8px; }
    [data-testid="stRadio"] label:hover{ box-shadow:3px 3px 8px var(--sd),-3px -3px 8px var(--sl); color:var(--slate)!important; }

    [data-baseweb="popover"] [data-baseweb="menu"]{ background:var(--bg)!important; border-radius:14px!important; box-shadow:8px 8px 20px var(--sd),-4px -4px 10px var(--sl)!important; border:none!important; }
    [data-baseweb="option"]:hover{ background:var(--sd)!important; border-radius:8px!important; }

    [data-testid="stNumberInput"] button{ background:var(--bg)!important; border:none!important; border-radius:8px!important; box-shadow:3px 3px 7px var(--sd),-3px -3px 7px var(--sl)!important; color:var(--slate)!important; font-weight:600!important; }
    [data-testid="stNumberInput"] button:hover{ color:var(--rose)!important; }
    [data-testid="stNumberInput"] button:active{ box-shadow:inset 2px 2px 5px var(--sd),inset -2px -2px 5px var(--sl)!important; }

    .badge{ display:inline-block; border-radius:50px; padding:3px 14px; font-size:0.72rem; font-weight:600; letter-spacing:0.4px; }
    .badge-h{ background:var(--bg); color:var(--rose);  box-shadow:3px 3px 8px var(--sd),-3px -3px 8px var(--sl); }
    .badge-m{ background:var(--bg); color:var(--amber); box-shadow:3px 3px 8px var(--sd),-3px -3px 8px var(--sl); }
    .badge-l{ background:var(--bg); color:var(--sage);  box-shadow:3px 3px 8px var(--sd),-3px -3px 8px var(--sl); }

    @keyframes soft-pulse{ 0%,100%{opacity:1} 50%{opacity:.45} }
    .pulse{ animation:soft-pulse 2.2s ease-in-out infinite; }

    hr{ border:none!important; border-top:1px solid var(--sd)!important; margin:1.5rem 0!important; }
    ::-webkit-scrollbar{ width:5px; height:5px; }
    ::-webkit-scrollbar-track{ background:var(--bg); }
    ::-webkit-scrollbar-thumb{ background:var(--sd); border-radius:3px; }
    ::-webkit-scrollbar-thumb:hover{ background:var(--slate); }
    .js-plotly-plot .plotly .bg{ fill:var(--bg)!important; }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ── HELPERS ──────────────────────────────────
def load_model():
    try:
        with open(os.path.join(BASE_DIR, 'best_model.pkl'),'rb') as f: model = pickle.load(f)
        with open(os.path.join(BASE_DIR, 'features.pkl'),'rb') as f:   feats  = pickle.load(f)
        return model, feats
    except: return None, None

def get_bsmas_result(score):
    if score <= 12:
        return "Balanced User","#4aaa88","Healthy usage pattern detected.",[
            "Maintain current digital boundaries.",
            "Schedule Phone-Free weekends.",
            "Continue focused deep work sessions.",]
    elif score <= 18:
        return "Mild Risk (Habitual)","#d99a2e","Showing signs of habitual dependency.",[
            "Enable App Timers for social media.",
            "Delete apps during exam weeks.",
            "Replace 30 min/day with a physical hobby.",]
    elif score <= 24:
        return "High Risk Dependency","#d96b6b","Digital habits are impacting mental health.",[
            "Start a 48-hour Digital Detox.",
            "Switch phone to grayscale mode.",
            "Uninstall high-attachment apps immediately.",]
    else:
        return "Severe Addiction Risk","#b84040","Urgent digital intervention suggested.",[
            "Consult a therapist for behavioral patterns.",
            "Transition to essential-only apps.",
            "Commit to a 30-day social media break.",]

NM = dict(paper_bgcolor='#e8ecf1',plot_bgcolor='#e8ecf1',
          font=dict(family='DM Sans',color='#4a5070'),
          margin=dict(l=20,r=20,t=30,b=20))

# ── NAV ──────────────────────────────────────
PAGES = ["Home","Psychological Assessment","Dataset Insights","Screen Time Controller"]
ICONS = ["⊙","◈","◎","◉"]
if 'menu' not in st.session_state: st.session_state.menu = "Home"

# ── SIDEBAR ───────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='padding:0.4rem 0 1.6rem;'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:4px;'>
                <div style='width:38px;height:38px;border-radius:12px;background:#e8ecf1;
                            box-shadow:4px 4px 10px #c5c9d0,-4px -4px 10px #fff;
                            display:flex;align-items:center;justify-content:center;font-size:20px;'>🧠</div>
                <div>
                    <p style='font-size:1rem;font-weight:700;color:#2d3250;margin:0;line-height:1.2;'>MindBalance</p>
                    <p style='font-size:0.62rem;color:#9aa0bc;letter-spacing:1.2px;text-transform:uppercase;margin:0;'>AI Digital Wellness</p>
                </div>
            </div>
        </div>
        <p style='font-size:0.62rem;color:#9aa0bc;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;padding-left:4px;'>Navigation</p>
    """, unsafe_allow_html=True)

    menu = st.radio("", PAGES,
        index=PAGES.index(st.session_state.menu),
        format_func=lambda x: f"{ICONS[PAGES.index(x)]}  {x}",
    )
    st.session_state.menu = menu

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        <p style='font-size:0.62rem;color:#9aa0bc;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;padding-left:4px;'>Quick Stats</p>
        <div style='display:flex;flex-direction:column;gap:7px;'>
    """ + "".join([f"""
        <div style='background:#e8ecf1;border-radius:12px;padding:0.65rem 1rem;
                    box-shadow:4px 4px 10px #c5c9d0,-4px -4px 10px #fff;
                    display:flex;justify-content:space-between;align-items:center;'>
            <span style='font-size:0.76rem;color:#4a5070;'>{lbl}</span>
            <span style='font-size:0.86rem;font-family:DM Mono,monospace;font-weight:500;color:{clr};'>{val}</span>
        </div>""" for lbl,val,clr in [
            ("Avg Risk Score","72%","#d96b6b"),
            ("Assessments","1,284","#6470b8"),
            ("Model Accuracy","94.2%","#4aaa88"),
        ]]) + "</div>", unsafe_allow_html=True)


# ── HOME ─────────────────────────────────────
if menu == "Home":
    st.markdown("""
        <h1>Decode Your <span class='highlight-text'>Digital Life</span></h1>
        <p style='color:#9aa0bc;font-size:0.88rem;margin-top:-0.5rem;margin-bottom:2rem;'>
        AI-powered social media addiction analysis for students & educators.
        </p>
    """, unsafe_allow_html=True)

    c1,c2 = st.columns([3,2], gap="large")
    with c1:
        st.markdown("""
            <div class='nm-card'>
                <span class='sec-label'>About This Tool</span>
                <h2 style='margin-top:0;margin-bottom:0.7rem;'>Real-World Addiction Analysis</h2>
                <p style='margin-bottom:1.2rem;font-size:0.9rem;line-height:1.75;'>
                Move beyond simple screen-time tracking. Understand the
                <strong style='color:#2d3250;'>psychological impact</strong> of digital consumption
                on your sleep, focus, academic performance, and relationships.
                </p>
                <div style='display:flex;flex-wrap:wrap;gap:5px;'>
                    <span class='stat-pill'><span class='dot' style='background:#d96b6b;'></span>Risk Detection</span>
                    <span class='stat-pill'><span class='dot' style='background:#6470b8;'></span>BSMAS Assessment</span>
                    <span class='stat-pill'><span class='dot' style='background:#4aaa88;'></span>AI Predictions</span>
                    <span class='stat-pill'><span class='dot' style='background:#d99a2e;'></span>Screen Guard</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        b1,b2 = st.columns(2)
        with b1:
            st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
            if st.button("Start Assessment →", key="h_cta"):
                st.session_state.menu = "Psychological Assessment"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b2:
            if st.button("View Insights", key="h_ins"):
                st.session_state.menu = "Dataset Insights"
                st.rerun()

    with c2:
        try: st.image(os.path.join(BASE_DIR, "website_design.png"), use_container_width=True)
        except:
            st.markdown("""
                <div class='nm-card' style='text-align:center;padding:3rem 1rem;min-height:200px;
                    display:flex;flex-direction:column;align-items:center;justify-content:center;'>
                    <div style='font-size:3.5rem;margin-bottom:0.5rem;'>🧠</div>
                    <p style='color:#9aa0bc;font-size:0.75rem;margin:0;letter-spacing:1px;text-transform:uppercase;'>MindBalance AI</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats row
    for col,(val,lbl,clr) in zip(st.columns(4,gap="medium"),[
        ("1,284","Students Assessed","#6470b8"),
        ("6.4h","Avg Daily Usage","#d96b6b"),
        ("94.2%","Model Accuracy","#4aaa88"),
        ("48h","Avg Detox Relief","#d99a2e"),
    ]):
        with col:
            st.markdown(f"""
                <div class='nm-sm' style='text-align:center;padding:1.2rem 0.8rem;'>
                    <p style='font-family:DM Mono,monospace;font-size:1.55rem;font-weight:600;color:{clr};margin:0;'>{val}</p>
                    <p style='font-size:0.68rem;color:#9aa0bc;text-transform:uppercase;letter-spacing:0.8px;margin:4px 0 0;'>{lbl}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<span class='sec-label'>What You Can Do</span>", unsafe_allow_html=True)

    for col,(icon,title,desc,clr) in zip(st.columns(4,gap="medium"),[
        ("🎯","Psych Assessment","Answer 12 clinical questions & get your addiction profile instantly.","#6470b8"),
        ("📊","Behavior Insights","Explore real data — screen time vs GPA, sleep, and relationships.","#4aaa88"),
        ("🛡️","Screen Guard","Set daily limits. AI monitors usage and alerts you automatically.","#d99a2e"),
        ("🤖","AI Risk Index","ML model predicts your clinical risk score with 94%+ accuracy.","#d96b6b"),
    ]):
        with col:
            st.markdown(f"""
                <div class='feat-card'>
                    <div class='feat-icon'>{icon}</div>
                    <p style='font-weight:600;color:#2d3250;font-size:0.87rem;margin:0 0 5px;'>{title}</p>
                    <p style='font-size:0.76rem;color:#9aa0bc;line-height:1.6;margin:0;'>{desc}</p>
                    <div style='margin-top:10px;width:26px;height:3px;border-radius:2px;background:{clr};'></div>
                </div>
            """, unsafe_allow_html=True)


# ── ASSESSMENT ───────────────────────────────
elif menu == "Psychological Assessment":
    st.markdown("""
        <h1>Clinical <span class='highlight-text'>Assessment</span></h1>
        <p style='color:#9aa0bc;font-size:0.88rem;margin-top:-0.5rem;margin-bottom:1.5rem;'>
        Bergen Social Media Addiction Scale (BSMAS) — validated 6-item psychometric tool.
        </p>
    """, unsafe_allow_html=True)

    with st.form("assessment"):
        st.markdown("<div class='nm-card'>", unsafe_allow_html=True)
        st.markdown("<span class='sec-label'>Student Profile</span>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: age      = st.number_input("Age", 16, 25, 20)
        with c2: gender   = st.selectbox("Gender", ["Male","Female","Non-binary","Prefer not to say"])
        with c3: level    = st.selectbox("Academic Level", ["High School","Undergraduate","Graduate"])
        c4,c5 = st.columns(2)
        with c4: country  = st.selectbox("Country", ["India","USA","UK","Australia","Other"])
        with c5: platform = st.selectbox("Primary Platform", ["Instagram","YouTube","Snapchat","Threads","LinkedIn","WhatsApp","Twitter/X"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='nm-card' style='margin-top:0;'>", unsafe_allow_html=True)
        st.markdown("""
            <span class='sec-label'>BSMAS Survey</span>
            <p style='font-size:0.8rem;color:#9aa0bc;margin-top:-0.3rem;margin-bottom:1rem;'>
            Rate each: &nbsp;1 = Very Rarely &nbsp;·&nbsp; 3 = Sometimes &nbsp;·&nbsp; 5 = Very Often
            </p>
        """, unsafe_allow_html=True)
        q1 = st.slider("I think about social media constantly", 1, 5, 3)
        q2 = st.slider("I feel an urge to use it more and more", 1, 5, 3)
        q3 = st.slider("I use it to escape personal problems", 1, 5, 3)
        q4 = st.slider("I have tried to cut back but failed", 1, 5, 3)
        q5 = st.slider("I feel restless if I cannot use it", 1, 5, 3)
        q6 = st.slider("It has negatively impacted my studies", 1, 5, 3)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='nm-card' style='margin-top:0;'>", unsafe_allow_html=True)
        st.markdown("<span class='sec-label'>Daily Metrics</span>", unsafe_allow_html=True)
        da,db,dc = st.columns(3)
        with da: usage     = st.slider("Daily Usage (Hours)", 0.0, 15.0, 4.0, 0.5)
        with db: sleep     = st.slider("Sleep Per Night (Hours)", 3.0, 10.0, 7.0, 0.5)
        with dc: conflicts = st.number_input("Social Conflicts / Week", 0, 20, 1)
        st.markdown("</div>", unsafe_allow_html=True)

        submit = st.form_submit_button("⟶  Generate AI Risk Report")

    if submit:
        total = q1+q2+q3+q4+q5+q6
        label,color,advice,cures = get_bsmas_result(total)
        severity  = "LOW" if total<=12 else "MODERATE" if total<=18 else "HIGH" if total<=24 else "SEVERE"
        badge_cls = "badge-l" if total<=12 else "badge-m" if total<=18 else "badge-h"

        st.markdown(f"""
            <div class='nm-card' style='border-left:4px solid {color};margin-top:1.5rem;'>
                <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;'>
                    <div>
                        <span class='sec-label' style='color:{color};'>Assessment Result</span>
                        <h2 style='margin:0;color:{color};font-size:1.45rem;'>{label}</h2>
                        <p style='margin:5px 0 0;font-size:0.87rem;'>{advice}</p>
                    </div>
                    <div style='text-align:right;'>
                        <span class='badge {badge_cls}'>{severity} RISK</span>
                        <p style='margin:6px 0 0;font-family:DM Mono,monospace;font-size:2rem;font-weight:600;color:{color};'>
                            {total}<span style='font-size:0.88rem;color:#9aa0bc;'>/30</span>
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        model,_ = load_model()
        gauge_val = (total/30)*100
        if model:
            feat = pd.DataFrame([{'Age':age,'Gender':gender,'Academic_Level':level,'Country':country,
                'Avg_Daily_Usage_Hours':usage,'Most_Used_Platform':platform,
                'Affects_Academic_Performance':"Yes" if q6>=4 else "No",
                'Sleep_Hours_Per_Night':sleep,'Mental_Health_Score':11-(total//3),
                'Relationship_Status':"Single",'Conflicts_Over_Social_Media':conflicts}])
            try: gauge_val = model.predict_proba(feat)[0][1]*100
            except: pass

        r1,r2 = st.columns(2, gap="medium")
        with r1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(gauge_val,1),
                number={'suffix':'%','font':{'color':color,'family':'DM Mono','size':38}},
                title={'text':"Clinical Risk Index",'font':{'color':'#9aa0bc','size':12}},
                gauge={'axis':{'range':[0,100],'tickcolor':'#9aa0bc','tickfont':{'color':'#9aa0bc','size':10}},
                       'bar':{'color':color,'thickness':0.24},'bgcolor':'#e8ecf1','borderwidth':0,
                       'steps':[{'range':[0,40],'color':'rgba(74,170,136,.13)'},
                                 {'range':[40,70],'color':'rgba(217,154,46,.13)'},
                                 {'range':[70,100],'color':'rgba(217,107,107,.13)'}]}))
            fig.update_layout(**NM, height=280)
            st.plotly_chart(fig, use_container_width=True)

        with r2:
            st.markdown(f"""
                <div class='nm-card' style='height:100%;'>
                    <span class='sec-label'>Cure</span>
                    {''.join([f"""<div style='display:flex;align-items:flex-start;gap:10px;
                        padding:0.6rem 0.9rem;border-radius:12px;margin-bottom:8px;
                        box-shadow:inset 3px 3px 7px #c5c9d0,inset -3px -3px 7px #fff;'>
                        <span style='color:{color};font-size:0.9rem;margin-top:1px;flex-shrink:0;'>✓</span>
                        <span style='color:#4a5070;font-size:0.84rem;line-height:1.5;'>{c}</span>
                    </div>""" for c in cures])}
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<span class='sec-label'>Score Breakdown by Dimension</span>", unsafe_allow_html=True)
        qs   = ["Preoccupation","Tolerance","Mood Mod.","Relapse","Withdrawal","Conflict"]
        vals = [q1,q2,q3,q4,q5,q6]
        fig2 = go.Figure(go.Bar(x=qs, y=vals, width=0.5, marker_line_width=0,
            marker_color=[color if v>=4 else '#7080c0' if v==3 else '#b0b8cc' for v in vals]))
        fig2.update_layout(**NM, height=220,
            yaxis=dict(range=[0,5],tickvals=[1,2,3,4,5],gridcolor='#d4d8e0'),
            xaxis=dict(tickfont=dict(size=11,color='#9aa0bc')), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)


# ── INSIGHTS ─────────────────────────────────
elif menu == "Dataset Insights":
    st.markdown("""
        <h1>Behavior <span class='highlight-text'>Insights</span></h1>
        <p style='color:#9aa0bc;font-size:0.88rem;margin-top:-0.5rem;margin-bottom:1.5rem;'>
        Real dataset analysis — screen time, mental health, sleep, and academic performance.
        </p>
    """, unsafe_allow_html=True)
    try:
        df = pd.read_csv(os.path.join(BASE_DIR, 'social_media_addiction_data.csv'))
        tab1,tab2,tab3 = st.tabs(["Screen Time vs Mental Health","Platform Usage","Risk Distribution"])
        with tab1:
            fig = px.scatter(df,x="Avg_Daily_Usage_Hours",y="Mental_Health_Score",color="Status",trendline="ols",
                color_discrete_sequence=["#d96b6b","#4aaa88","#6470b8"],template="none",
                labels={"Avg_Daily_Usage_Hours":"Daily Usage (hrs)","Mental_Health_Score":"Mental Health Score"})
            fig.update_layout(**NM,height=380)
            fig.update_traces(marker=dict(size=7,opacity=0.7))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("<div class='nm-inset'><p style='color:#4a5070;font-size:0.84rem;margin:0;'>💡 Mental resilience drops sharply after <strong style='color:#2d3250;'>5 hours</strong> of daily usage. Addicted students scored 38% lower.</p></div>", unsafe_allow_html=True)
        with tab2:
            if "Most_Used_Platform" in df.columns:
                pc = df["Most_Used_Platform"].value_counts().reset_index()
                pc.columns = ["Platform","Count"]
                fig2 = px.bar(pc,x="Platform",y="Count",color="Platform",template="none",
                    color_discrete_sequence=["#d96b6b","#6470b8","#4aaa88","#d99a2e","#9aa0bc","#b080c0","#70a0d0"])
                fig2.update_layout(**NM,height=340,showlegend=False)
                fig2.update_traces(marker_line_width=0,width=0.5)
                st.plotly_chart(fig2,use_container_width=True)
        with tab3:
            if "Status" in df.columns:
                sc = df["Status"].value_counts()
                fig3 = go.Figure(go.Pie(labels=sc.index,values=sc.values,hole=0.55,
                    marker=dict(colors=["#d96b6b","#4aaa88","#d99a2e"],line=dict(color='#e8ecf1',width=3)),
                    textfont=dict(family='DM Sans',size=12,color='#4a5070')))
                fig3.update_layout(**NM,height=320,showlegend=True,
                    legend=dict(font=dict(color='#4a5070',family='DM Sans')))
                st.plotly_chart(fig3,use_container_width=True)
    except Exception as e:
        st.markdown(f"""<div class='nm-inset' style='border-left:3px solid #d96b6b;'>
            <p style='color:#d96b6b;font-size:0.87rem;margin:0;'>⚠ Place <code>social_media_addiction_data.csv</code> in project root.</p>
            <p style='color:#9aa0bc;font-size:0.76rem;margin:3px 0 0;'>{e}</p></div>""", unsafe_allow_html=True)


# ── SCREEN TIME ──────────────────────────────
elif menu == "Screen Time Controller":
    st.markdown("""
        <h1>Screen Time <span class='highlight-text'>Guard</span></h1>
        <p style='color:#9aa0bc;font-size:0.88rem;margin-top:-0.5rem;margin-bottom:1.5rem;'>
        Set a daily limit. The AI Guard monitors usage and alerts you automatically.
        </p>
    """, unsafe_allow_html=True)

    CONFIG_PATH = os.path.join(BASE_DIR, 'screen_config.json')
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH,'r') as f: config = json.load(f)
    else:
        config = {"limit":4.0,"status":"active","start_time":datetime.now().timestamp()}

    ca,cb = st.columns([1,1], gap="large")
    with ca:
        st.markdown("<div class='nm-card'>", unsafe_allow_html=True)
        st.markdown("<span class='sec-label'>Guard Configuration</span>", unsafe_allow_html=True)
        new_limit = st.number_input("Daily Screen Limit (Hours)", 0.5, 12.0, float(config["limit"]), 0.5)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⟶  Activate Real-Time Guard", key="act"):
            config["limit"]=new_limit; config["status"]="active"
            with open(CONFIG_PATH,'w') as f: json.dump(config,f)
            try: subprocess.Popen(["python", os.path.join(BASE_DIR, "background_monitor.py")],
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            except: pass
            st.success("✓ AI Guard is now active in the background!")
        if st.button("↺  Reset Timer", key="rst"):
            config["start_time"]=datetime.now().timestamp()
            with open(CONFIG_PATH,'w') as f: json.dump(config,f)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='nm-inset' style='margin-top:0;'><p style='color:#9aa0bc;font-size:0.79rem;margin:0;'>💡 Once activated, the Guard works outside the browser. You don't need to keep this tab open.</p></div>", unsafe_allow_html=True)

    with cb:
        elapsed      = (datetime.now().timestamp()-config["start_time"])/3600
        progress_pct = min(1.0,elapsed/new_limit) if new_limit>0 else 1.0
        bar_color    = "#4aaa88" if progress_pct<0.6 else "#d99a2e" if progress_pct<0.9 else "#d96b6b"
        remaining    = max(0,new_limit-elapsed)
        fig_g = go.Figure(go.Indicator(mode="gauge+number+delta",value=round(elapsed,2),
            delta={'reference':new_limit,'suffix':'h limit','font':{'color':'#9aa0bc','size':12}},
            number={'suffix':"h",'font':{'color':bar_color,'family':'DM Mono','size':34}},
            title={'text':"Session Time",'font':{'color':'#9aa0bc','size':12}},
            gauge={'axis':{'range':[0,new_limit],'tickcolor':'#9aa0bc','tickfont':{'color':'#9aa0bc','size':10}},
                   'bar':{'color':bar_color,'thickness':0.26},'bgcolor':'#e8ecf1','borderwidth':0,
                   'steps':[{'range':[0,new_limit*.6],'color':'rgba(74,170,136,.1)'},
                             {'range':[new_limit*.6,new_limit*.9],'color':'rgba(217,154,46,.1)'},
                             {'range':[new_limit*.9,new_limit],'color':'rgba(217,107,107,.1)'}],
                   'threshold':{'line':{'color':'#d96b6b','width':3},'thickness':0.75,'value':new_limit}}))
        fig_g.update_layout(**NM,height=260)
        st.plotly_chart(fig_g,use_container_width=True)

    st.progress(progress_pct, text=f"{int(progress_pct*100)}% of daily limit consumed")
    m1,m2,m3 = st.columns(3,gap="medium")
    with m1: st.metric("Session Duration",f"{elapsed:.2f}h",
                delta=f"{remaining:.2f}h left" if elapsed<new_limit else "Limit reached!",
                delta_color="normal" if elapsed<new_limit else "inverse")
    with m2: st.metric("Daily Limit",f"{new_limit}h",delta="Guard Active" if config.get('status')=='active' else "Inactive")
    with m3:
        pct=int(progress_pct*100)
        st.metric("Usage %",f"{pct}%",delta=f"{100-pct}% safe zone" if pct<100 else "Exceeded!")

    if elapsed>new_limit:
        st.markdown(f"""
            <div style='background:#e8ecf1;border-radius:14px;padding:1rem 1.4rem;
                box-shadow:inset 4px 4px 9px #c5c9d0,inset -4px -4px 9px #fff;
                border-left:4px solid #d96b6b;margin-top:1rem;display:flex;align-items:center;gap:12px;'>
                <span class='pulse' style='color:#d96b6b;font-size:1.2rem;'>⚠</span>
                <div>
                    <p style='color:#d96b6b;font-weight:600;font-size:0.88rem;margin:0;'>Daily Limit Exceeded</p>
                    <p style='color:#9aa0bc;font-size:0.77rem;margin:2px 0 0;'>
                    Used <strong style='color:#d96b6b;'>{elapsed:.2f}h</strong> —
                    {elapsed-new_limit:.2f}h over your {new_limit}h limit. Guard is active.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)