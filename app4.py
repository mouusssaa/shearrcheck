import streamlit as st
import math

st.set_page_config(page_title="Punching Shear Check", layout="centered")
st.title("Punching Shear Check (ACI 318-19)")

Oo = 0.75  # Strength reduction factor

# Initialize session state variable
if "run_check" not in st.session_state:
    st.session_state.run_check = False

# --- User Inputs ---
st.header("Input Parameters")
col1, col2 = st.columns(2)
with col1:
    Cx = st.number_input("Cx (mm)", min_value=0.0, step=10.0)
    Vu = st.number_input("Vu (kN)", min_value=0.0, step=10.0)
    Mux = st.number_input("Mux (kN·m)", min_value=0.0, step=10.0)
with col2:
    Cy = st.number_input("Cy (mm)", min_value=0.0, step=10.0)
    h = st.number_input("Slab Thickness h (mm)", min_value=0.0, step=10.0)
    Muy = st.number_input("Muy (kN·m)", min_value=0.0, step=10.0)

fc = st.number_input("Concrete compressive strength f'c (MPa)", min_value=0.0, step=5.0)

# When button clicked, set session_state flag
if st.button("Run Punching Shear Check"):
    st.session_state.run_check = True

# Only run calculations and show results if button was clicked
if st.session_state.run_check:
    # Basic input validation
    if Vu == 0 or h == 0 or fc == 0:
        st.error("Please enter non-zero values for Vu, h, and f'c.")
    else:
        d = h - 40  
        b = 2 * (Cx + Cy + 2 * d)
        Vc = 0.33 * math.sqrt(fc) * b * d * 1e-3 
        Vc_max = 2 * Vc

        D_d = d / 2
        Bo = 2 * ((Cx + 2 * D_d) + (Cy + 2 * D_d))
        vu_direct = Vu / (Bo * d)
        eX = (Mux * 1e3) / (Vu * 1e3) * 1e3  
        eY = (Muy * 1e3) / (Vu * 1e3) * 1e3  
        eEQ = math.sqrt(eX ** 2 + eY ** 2)
        r = (Cx + d + Cy + d) / 2
        B_b = 1 + ((1.5 * eEQ) / r)
        vu = B_b * (Vu / (Bo * d)) * 1e3  

        st.subheader("Punching Shear Check Result")
        if vu > Oo * Vc:
            st.error("❌ FAILED: The slab fails in punching shear even with moments included.")
            
            if Vu <= Oo * Vc_max:
                st.warning("⚠️ Shear Reinforcement is needed.")
                with st.expander("Shear Reinforcement Design"):
                    fy = st.number_input("f yield (MPa)", min_value=0.0, step=50.0, key="fy")
                    no = st.number_input("Number of legs", min_value=1, step=1, key="no")
                    diameter = st.number_input("Bar diameter (mm)", min_value=4.0, step=1.0, key="diameter")
                    spacing = st.number_input("Assumed spacing (mm)", min_value=10.0, step=5.0, key="spacing")

                    if fy > 0 and diameter > 0 and spacing > 0:
                        Vs = (Vu - (Oo * Vc)) / Oo  # Required shear strength
                        As = (math.pi * (diameter / 2) ** 2)  # mm²
                        vs = (As * fy * d * no) / (spacing * 1000)  # kN

                        if vs >= Vs:
                            st.success(f"✅ OK: vs = {round(vs)} kN ≥ Vs_required = {round(Vs)} kN")
                        else:
                            st.error(f"❌ NOT OK: vs = {round(vs)} kN < Vs_required = {round(Vs)} kN")
            else:
                st.error("❌ FAILED: Even with shear reinforcement.")

        else:
            st.success("✅ SUCCEEDED: No reinforcement needed.")

        # --- Show Calculations ---
        with st.expander("Show Full Calculations"):
            st.write(f"**Effective depth, d** = {round(d)} mm")
            st.write(f"**b (critical perimeter)** = {round(b)} mm")
            st.write(f"**Vc** = {round(Vc, 2)} kN")
            st.write(f"**φVc** = {round(Vc * Oo, 2)} kN")
            st.write(f"**Vc-max** = {round(Vc_max, 2)} kN")
            st.write(f"**φVc-max** = {round(Vc_max * Oo, 2)} kN")
            st.write(f"**eX** = {round(eX, 2)} mm")
            st.write(f"**eY** = {round(eY, 2)} mm")
            st.write(f"**eEQ** = {round(eEQ, 2)} mm")
            st.write(f"**β (Bb)** = {round(B_b, 3)}")
            st.write(f"**vu** = {round(vu, 3)} MPa")

# Optional reset button
if st.button("Reset"):
    st.session_state.run_check = False
    for key in ["fy", "no", "diameter", "spacing"]:
        if key in st.session_state:
            del st.session_state[key]
