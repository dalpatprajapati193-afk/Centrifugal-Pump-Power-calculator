import streamlit as st

st.set_page_config(page_title="ChemE Pump Kit", layout="wide")

st.title("🚀 Centrifugal Pump Power")
st.markdown("---")

# Sidebar for Inputs
with st.sidebar:
    st.header("Input Parameters")
    flow = st.number_input("Flow Rate (m³/h)", value=50.0)
    head = st.number_input("Differential Head (m)", value=30.0)
    # Added Density as requested
    rho = st.number_input("Fluid Density (kg/m³)", value=1000.0, help="Water is ~1000 kg/m³")
    st.markdown("---")
    # Efficiency for Shaft Power
    eff = st.slider("Pump Efficiency (%)", 10, 100, 75) / 100

# Physics constants
g = 9.81

# Calculations
# 1. Hydraulic Power (Theoretical power needed to move the fluid)
# Formula: P (kW) = (Q * rho * g * h) / (3600 * 1000)
hyd_power = (flow * rho * g * head) / 3600000

# 2. Shaft Power (Actual power required from the motor/shaft)
# Formula: Shaft Power = Hydraulic Power / Efficiency
shaft_power = hyd_power / eff

# Display Results in a nice layout
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Hydraulic Power", value=f"{hyd_power:.2f} kW")
    st.info("Theoretical power transmitted to the liquid.")

with col2:
    st.metric(label="Shaft Power (Brake Power)", value=f"{shaft_power:.2f} kW")
    st.warning("Actual power required at the pump shaft.")

# Optional: Add a small chart or tip
st.markdown("---")
st.caption(f"Note: Based on a density of {rho} kg/m³ and {eff*100}% efficiency.")