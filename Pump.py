import streamlit as st
import math
import pandas as pd
import numpy as np

st.set_page_config(page_title="Chemical Engineering Process Calculator", layout="wide")

# Custom CSS to remove white backgrounds and make metrics clean
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
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
            q_range = np.linspace(0, flow * 1.5, 20)
            h0 = head * 1.25 
            k = (h0 - head) / (flow**2) if flow != 0 else 0
            h_range = h0 - k * (q_range**2)
            
            df_curve = pd.DataFrame({'Flow (m³/h)': q_range, 'Head (m)': h_range})
            st.line_chart(df_curve, x="Flow (m³/h)", y="Head (m)", x_label="Flow Rate (m³/h)", y_label="Total Head (m)")

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

    with st.expander("3. Pipe Sizing & Frictional Drop"):
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            v_limit = st.number_input("Target Velocity (m/s)", value=1.5)
            q_m3s = flow / 3600
            # Area = Q/V -> D = sqrt(4A/pi)
            d_req = math.sqrt((4 * q_m3s) / (math.pi * v_limit)) # meters
            st.metric("Required Pipe ID", f"{d_req*1000:.1f} mm")
        
        with p_col2:
            st.write("**Frictional Loss Calculation (Darcy-Weisbach)**")
            pipe_len = st.number_input("Pipe Length (m)", value=100.0)
            f_factor = 0.02 # Assumed friction factor for turbulent flow
            # hf = f * (L/D) * (v^2 / 2g)
            head_loss = f_factor * (pipe_len / d_req) * (v_limit**2 / (2 * 9.81))
            st.metric("Estimated Head Loss", f"{head_loss:.2f} m")
            st.caption(f"Based on Velocity of {v_limit} m/s and Length of {pipe_len}m")

# --- HEAT EXCHANGER TAB ---
with tab_hex:
    st.header("Heat Exchanger Analysis")
    with st.expander("LMTD & Duty Calculation", expanded=True):
        h_c1, h_c2 = st.columns(2)
        with h_c1:
            thi, tho = st.number_input("Hot In (°C)", 90.0), st.number_input("Hot Out (°C)", 60.0)
            tci, tco = st.number_input("Cold In (°C)", 25.0), st.number_input("Cold Out (°C)", 45.0)
        with h_c2:
            dt1, dt2 = (thi - tco), (tho - tci)
            if dt1 <= 0 or dt2 <= 0:
                st.error("Temperature approach error: Check In/Out values.")
                lmtd = 0
            else:
                lmtd = (dt1 - dt2) / math.log(dt1/dt2) if dt1 != dt2 else dt1
            u_val = st.number_input("Overall U (W/m²K)", 500.0)
            area = st.number_input("Heat Transfer Area (m²)", 10.0)
            duty = (u_val * area * lmtd)/1000
            st.metric("Heat Duty", f"{duty:.2f} kW")
            st.metric("LMTD", f"{lmtd:.2f} °C")

# --- COMPRESSOR TAB ---
with tab_comp:
    st.header("Compressor Analysis")
    with st.expander("Isentropic Power Calculation", expanded=True):
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            k_val = st.number_input("Isentropic Exponent (k)", 1.4)
            p1_c, p2_c = st.number_input("Inlet Pressure (bar a)", 1.0), st.number_input("Outlet Pressure (bar a)", 3.0)
            t1_c = st.number_input("Inlet Temp (°C)", 25.0) + 273.15
        with c_col2:
            mass_f = st.number_input("Mass Flow Rate (kg/s)", 1.0)
            c_isen_eff = st.slider("Isentropic Efficiency (%)", 50, 95, 75) / 100
            # P = m * Cp * T1 * [(P2/P1)^((k-1)/k) - 1] / eff
            ratio_c = (p2_c/p1_c)**((k_val-1)/k_val) - 1
            # Using R = 0.287 kJ/kgK for air-like gases
            cp_val = (k_val * 0.287) / (k_val - 1)
            c_power = (mass_f * cp_val * t1_c * ratio_c) / c_isen_eff
            st.metric("Compressor Power", f"{c_power:.2f} kW")

# --- DISTILLATION TAB ---
with tab_dist:
    st.header("Distillation Analysis (Fenske Shortcut)")
    chem_db = {"Methanol/Water": 3.6, "Ethanol/Water": 2.4, "Benzene/Toluene": 2.5, "Custom": 1.0}
    
    d_c1, d_c2 = st.columns(2)
    with d_c1:
        mix_sel = st.selectbox("Select Binary Mixture", list(chem_db.keys()))
        alpha_val = st.number_input("Relative Volatility (α)", chem_db[mix_sel]) if mix_sel == "Custom" else chem_db[mix_sel]
        xd_val = st.number_input("Distillate Purity (%)", 98.0) / 100
        xw_val = st.number_input("Bottoms Concentration (%)", 1.0) / 100
        reflux = st.number_input("Actual Reflux Ratio (R/D)", value=2.0)
    with d_c2:
        # Nm = log((xd/1-xd)/(xw/1-xw)) / log(alpha)
        nm_val = math.log((xd_val/(1-xd_val)) / (xw_val/(1-xw_val))) / math.log(alpha_val) if alpha_val > 1 else 0
        st.metric("Min. Theoretical Stages (Nm)", f"{nm_val:.1f}")
        st.info(f"Mixture: {mix_sel} | α: {alpha_val}")

st.markdown("---")
st.markdown("### Developed by: **Dilip Kumar B**")
