import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title='Zimbabwe Migration Risk', layout='wide')

st.title('🌍 Zimbabwe Internal Migration Risk Dashboard')

# Simple Authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if username == 'admin' and password == 'migration2026':
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error('Invalid credentials')
else:
    st.success('✅ Authenticated - Welcome!')
    tab1, tab2, tab3 = st.tabs(['Model', 'Interactive Maps', 'Policy Scenarios'])
    with tab1:
        st.write('Enhanced Bayesian Model with JAX acceleration')
    with tab2:
        st.write('Kepler.gl maps would load here')
    with tab3:
        st.write('Counterfactual scenarios')
