import streamlit as st
import pandas as pd
import numpy as np
from backend.app.model import CLVEngine

st.set_page_config(page_title='LifeTimeIQ - CLV Predictor', layout='wide')

@st.cache_resource
def load_engine():
    engine = CLVEngine()
    engine.load()
    return engine

engine = load_engine()
st.title('LifeTimeIQ: AI Customer Lifetime Value Predictor')

col1, col2 = st.columns([1, 1])
with col1:
    st.subheader('Customer Transaction Details')
    name = st.text_input('Customer Name', value='Aarav Sharma')
    freq = st.number_input('Repeat Orders (Frequency)', min_value=0.0, value=6.0)
    rec = st.number_input('Days Since Last Order (Recency)', min_value=0.0, value=35.0)
    aov = st.number_input('Average Order Value (INR)', min_value=1.0, value=1200.0)
    tenure = st.number_input('Customer Tenure (Days)', min_value=1.0, value=320.0)
    predict_btn = st.button('Run AI Forecast')

with col2:
    st.subheader('Prediction Result')
    if predict_btn:
        if rec > tenure:
            st.error('Recency cannot exceed total tenure.')
        else:
            clv, seg, orders, exp_aov = engine.predict(freq, rec, aov, tenure)
            st.metric('Predicted 12-Month CLV', f'INR {clv:,.2f}')
            st.info(f'Assigned Tier: {seg}')
            st.write(f'Expected Orders: {orders}')
            st.write(f'Expected Order Value: INR {exp_aov:,.2f}')
