import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load model and input scaler
model = joblib.load("random_forest_model.pkl")
scaler_X = joblib.load("scaler_X_rf.pkl")

st.title("Nano FET Id Prediction using Random Forest")

st.markdown("Enter the following parameters to predict the Drain Current (Id):")

# User inputs
vg_input = st.number_input("Vg (in V)", min_value=0.0, max_value=5.0, step=0.1)
vd_input = st.number_input("Vd (in V)", min_value=0.0, max_value=5.0, step=0.1)
gate_input = st.number_input("Gate Length (nm)", min_value=1.0, max_value=100.0, step=0.1)
channel_input = st.number_input("Channel Thickness (nm)", min_value=1.0, max_value=50.0, step=0.1)
sio2_input = st.number_input("SiO2 Thickness (nm)", min_value=0.1, max_value=10.0, step=0.1)
hfo2_input = st.number_input("HfO2 Thickness (nm)", min_value=0.1, max_value=10.0, step=0.1)
work_function_input = st.number_input("Work Function (eV)", min_value=4.0, max_value=5.5, step=0.1)
trap_input = st.selectbox("Trap Charge Present?", ["No", "Yes"])
trap_input_val = 1.0 if trap_input == "Yes" else 0.0
trap_concentration_input = st.number_input("Trap Charge Concentration", min_value=0.0, max_value=1e20, step=1e18)

# Prediction button
if st.button("Predict Id"):
    custom_input = {
        'Vg': vg_input,
        'Vd': vd_input,
        'gate_length': gate_input,
        'channel_thickness': channel_input,
        'SiO2_thickness': sio2_input,
        'HfO2_thickness': hfo2_input,
        'work_function': work_function_input,
        'trap_charges': trap_input_val,
        'trap_charge_concentration': trap_concentration_input
    }

    # Convert to DataFrame and scale
    custom_df = pd.DataFrame([custom_input])
    custom_input_scaled = scaler_X.transform(custom_df)

    # Predict
    predicted_id = model.predict(custom_input_scaled)[0]

    st.success(f"Predicted Drain Current (Id): {predicted_id:.4e} A")