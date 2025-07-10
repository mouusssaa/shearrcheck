import streamlit as st
import math

st.title("Two-Way Shear Check (ACI 318-19)")

Oo = 0.75

# Input fields
thickness = st.number_input("Enter Slab Thickness (mm):", min_value=1.0)
Cx = st.number_input("Enter Cx (mm):", min_value=1.0)
Cy = st.number_input("Enter Cy (mm):", min_value=1.0)
Vu = st.number_input("Enter Vu (kN):", min_value=0.0)
Fc = st.number_input("Enter f'c (MPa):", min_value=0.0)

if st.button("Check Shear"):
    d = thickness - 35
    b = 2 * (Cx + Cy + 2 * d)
    Vc = 0.17 * math.sqrt(Fc) * b * d * 1e-3  # ACI 318-19 for slabs
    Vc_rounded = round(Vc, 1)
    phi_Vc = round(Oo * Vc, 1)

    # Check result
    if Vu <= Oo * Vc:
        st.success("✅ SUCCEEDED: No reinforcement needed.")
    else:
        v_u = Vu * 1000 / (b * d)
        v_max = 0.66 * math.sqrt(Fc) * 1e6
        if v_u <= v_max:
            st.warning("⚠️ SUCCEEDED: Shear reinforcement is needed.")
        else:
            st.error("❌ FAILED: Even with shear reinforcement.")

    # Optional detailed output
    with st.expander("Show Calculations"):
        st.write(f"b = {round(b)} mm")
        st.write(f"Effective depth d = {round(d)} mm")
        st.write(f"Vc = {Vc_rounded} kN")
        st.write(f"φVc = {phi_Vc} kN")
