import streamlit as st

st.set_page_config(page_title="ChemE Pump Kit", layout="wide")

st.title("🚀 Centrifugal Pump Power")
st.markdown("---")

# Sidebar for Inputs
with st.sidebar:
    st.header("Input Parameters")
    flow = st.number_input("Flow Rate (m³/h)", value=50.0)
    head = st.number_input("Differential Head (m)", value=30.0)
    rho = st.number_input("Fluid Density (kg/m³)", value=1000.0)
    st.markdown("---")
    
    # Efficiencies
    pump_eff = st.slider("Pump Efficiency (%)", 10, 100, 75) / 100
    motor_eff = st.slider("Motor Efficiency (%)", 10, 100, 90) / 100

# Calculations
g = 9.81
# 1. Hydraulic Power (kW)
hyd_power = (flow * rho * g * head) / 3600000

# 2. Shaft Power (kW)
shaft_power = hyd_power / pump_eff

# 3. Motor Power (kW & HP)
motor_power_kw = shaft_power / motor_eff
motor_power_hp = motor_power_kw / 0.746

# Standard HP Suggestions (NEMA/IEC typical sizes)
standard_hp_list = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7.5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100]
suggested_hp = next((x for x in standard_hp_list if x >= motor_power_hp), "Above 100 HP")

# Display Results
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Hydraulic Power", value=f"{hyd_power:.2f} kW")
    st.caption("Theoretical Power")

with col2:
    st.metric(label="Shaft Power", value=f"{shaft_power:.2f} kW")
    st.caption("Brake Power (BHP)")

with col3:
    st.metric(label="Motor Power Required", value=f"{motor_power_hp:.2f} HP")
    st.success(f"Suggested Motor: {suggested_hp} HP")

st.markdown("---")
# This is line 57 - ensure it stays as one single line in your editor!
st.info(f"Summary: For {flow} m3/h at {head}m head, use a {suggested_hp} HP motor")
