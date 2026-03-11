import streamlit as st
import math
import pandas as pd
import numpy as np

st.set_page_config(page_title="ChemE Process Pro", layout="wide")

# Custom CSS to remove white backgrounds and make metrics clean
st.markdown("""
    <style>
    /* Remove white background from metric boxes */
    div[data-testid="stMetric"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    /* Optional: Remove card-like background from containers */
    div[data-testid="column"] {
        background-color: transparent !important;
    }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Engineering Process Dashboard")
st.markdown("---")

tab_pump, tab_hex, tab_comp, tab_dist = st.tabs(["Pump System", "Heat Exchanger", "Compressor", "Distillation"])

# --- PUMP SYSTEM TAB ---
with tab_pump:
    st.header("Pump System Analysis")
    
    with st.expander("1. Power Calculation & Performance Curve", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            flow = st.number_input("Design Flow Rate (m³/h)", value=50.0)
            rho = st.number_input("Fluid Density (kg/m³)", value=1000.0)
            head = st.number_input("Design Head (m)", value=30.0)
            p_eff = st.slider("Pump Efficiency (%)", 10, 100, 75) / 100
            m_eff = st.slider("Motor Efficiency (%)", 10, 100, 90) / 100
            
            hyd_p = (flow * rho * 9.81 * head) / 3600000
            shaft_p = hyd_p / p_eff
            motor_hp = (shaft_p / m_eff) / 0.746
            
            st.metric("Shaft Power", f"{shaft_p:.2f} kW")
            st.metric("Motor Required", f"{motor_hp:.2f} HP")

        with col2:
            st.subheader("Simulated Performance Curve")
            # Generate Curve Data
            q_range = np.linspace(0, flow * 1.5, 20)
            h0 = head * 1.25 
            k = (h0 - head) / (flow**2)
            h_range = h0 - k * (q_range**2)
            
            # Use st.area_chart or st.line_chart with labels (Requires Streamlit 1.30+)
            df = pd.DataFrame({'Flow (m³/h)': q_range, 'Head (m)': h_range})
            st.line_chart(
                df, 
                x="Flow (m³/h)", 
                y="Head (m)", 
                x_label="Flow Rate (m³/h)", 
                y_label="Total Head (m)"
            )

    with st.expander("2. NPSH Available Calculation"):
        n_c1, n_c2 = st.columns(2)
        with n_c1:
            p_abs = st.number_input("Source Pressure (bar a)", 1.013)
            p_vap = st.number_input("Vapor Pressure (bar a)", 0.03)
        with n_c2:
            h_suc = st.number_input("Static Suction Head (m)", 2.0)
            h_f_s = st.number_input("Suction Friction Loss (m)", 0.5)
            npsha = ((p_abs - p_vap) * 100000 / (rho * 9.81)) + h_suc - h_f_s
            st.metric("NPSH Available", f"{npsha:.2f} m")

# --- OTHER TABS (Same logic as before) ---
with tab_hex:
    st.header("Heat Exchanger Analysis")
    # ... (Keep previous HE code)

with tab_dist:
    st.header("Distillation Analysis")
    # ... (Keep previous Distillation code)

st.markdown("---")
st.markdown("### Developed by: **Dilip Kumar B**")
