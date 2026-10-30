import os
import sqlite3
from contextlib import closing
from datetime import date, datetime, time

import pandas as pd
import psycopg
import streamlit as st

st.set_page_config(page_title="BIOMEDICS | Gestión de clientes", page_icon="🦻", layout="wide")

st.sidebar.markdown("""
<div class="brand-lockup">
  <div class="brand-symbol">
    <svg viewBox="0 0 96 96" role="img" aria-label="BIOMEDICS">
      <path d="M56 12c-20 0-34 15-34 35 0 14 7 23 17 28 6 3 8 7 8 13" fill="none" stroke="#54D6D0" stroke-width="7" stroke-linecap="round"/>
      <path d="M56 27c-11 0-19 8-19 20 0 8 4 13 10 17 5 3 8 7 8 13" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
      <path d="M63 38c7 4 11 10 11 18" fill="none" stroke="#54D6D0" stroke-width="6" stroke-linecap="round"/>
      <circle cx="74" cy="61" r="5" fill="#54D6D0"/>
    </svg>
  </div>
  <div class="brand-name">BIOMEDICS</div>
  <div class="brand-tag">EXPERTOS EN AUDICIÓN</div>
  <div class="brand-rule"></div>
  <div class="brand-caption">GESTIÓN CLÍNICA</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
:root { --ink:#142B43; --navy:#102B46; --blue:#176B87; --cyan:#54D6D0; --paper:#F3F7FA; --muted:#64788A; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background:var(--paper); }
[data-testid="stHeader"] { background:rgba(243,247,250,.92); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#102B46 0%,#173E5B 100%); border-right:1px solid #254B67; }
[data-testid="stSidebar"] * { color:#F4FAFC; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { color:#EAF5F8 !important; }
[data-testid="stSidebar"] [role="radio"] { padding:9px 12px; border-radius:10px; }
[data-testid="stSidebar"] [aria-checked="true"] { background:rgba(84,214,208,.16); border:1px solid rgba(84,214,208,.35); }
[data-testid="stSidebar"] input[type="radio"] { accent-color:#54D6D0 !important; }
.brand-lockup { display:flex; flex-direction:column; align-items:center; padding:18px 8px 26px; text-align:center; }
.brand-symbol { width:76px; height:76px; display:grid; place-items:center; border:1px solid rgba(84,214,208,.4); border-radius:24px; background:rgba(255,255,255,.06); }
.brand-symbol svg { width:65px; height:65px; }
.brand-name { margin-top:14px; color:#fff; font:800 25px Arial,sans-serif; letter-spacing:2.8px; }
.brand-tag { margin-top:5px; color:#A8D9DC; font:600 9px Arial,sans-serif; letter-spacing:2.2px; }
.brand-rule { width:48px; height:2px; background:#54D6D0; margin:19px 0 10px; }
.brand-caption { color:#A8BDCC; font:600 9px Arial,sans-serif; letter-spacing:2px; }
.block-container { padding-top:2.1rem; padding-bottom:3rem; max-width:1500px; }
h1 { color:var(--ink) !important; font-size:2rem !important; font-weight:800 !important; letter-spacing:-.6px; }
h2,h3 { color:var(--ink) !important; font-weight:750 !important; }
p, label, [data-testid="stMarkdownContainer"] { color:var(--ink); }
[data-testid="stCaptionContainer"] { color:var(--muted); }
[data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#EAF3F7); border:1px solid #D7E4EA; border-radius:16px; padding:18px 20px; box-shadow:0 5px 18px rgba(16,43,70,.06); }
[data-testid="stMetricLabel"] { color:#587184 !important; }
[data-testid="stMetricValue"] { color:#123D59 !important; font-weight:800; }
[data-testid="stForm"], [data-testid="stExpander"] { background:#FFFFFF; border:1px solid #DCE7EC; border-radius:14px; padding:14px; }
[data-testid="stDataFrame"] { border:1px solid #DCE7EC; border-radius:12px; overflow:hidden; }
.stButton > button, [data-testid="stFormSubmitButton"] > button { border-radius:10px; border:0; background:#176B87; color:white; font-weight:700; padding:.55rem 1.1rem; }
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover { background:#12566D; color:white; border:0; }
input, textarea, [data-baseweb="select"] > div { border-radius:9px !important; }
hr { border-color:#DCE7EC; }
</style>
""", unsafe_allow_html=True)

