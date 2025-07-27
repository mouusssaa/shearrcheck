import streamlit as st
import math

# -- App Config --
st.set_page_config(page_title="Punching Shear Check", layout="centered")
st.title("🧱 Punching Shear Check (ACI 318-19)")

# -- Initialize Session State --
if "run_check" not in st.session_state:
    st.session_state["run_check"] = False

# -- Constants --
Oo = 0.75  # Strength reduction factor

# -- Input Fields --
st.header("🔢 Input Parameters")
col1, col2 = st.columns(2)
with col1:
    Cx = st.number_input("Column dimension Cx (mm)", min_value=0.0, step=10.0)
    Vu = st.number_input("Factored Shear Vu (kN)", min_value=0.0, step=10.0)
    Mux = st.number_input("Moment Mux (kN·m)", min_value=0.0, step=10.0)
with col2:
    Cy = st.number_input("Column dimension Cy (mm)", min_value=0.0, step=10.0)
    h = st.number_input("Slab Thickness h (mm)", min_value=0.0, step=10.0)
    Muy = st.number_input("Moment Muy (kN·m)", min_value=0.0, step=10.0)

fc = st.number_input("Concrete compressive strength f'c (MPa)", min_value=0.0, step=5.0)

# -- Button --
if st.button("🔍 Run Punching Shear Check"):
    st.session_state["run_check"] = True

# -- Run Check --
if st.session_state["run_check"]:
    d = h - 40  # Effective depth (simplified assumption)
    b = 2 * (Cx + Cy + 2 * d)
    Vc = 0.33 * math.sqrt(fc) * b * d * 1e-3  # kN
    Vc_max = 2 * Vc

    D_d = d / 2
    Bo = 2 * ((Cx + 2 * D_d) + (Cy + 2 * D_d))
    vu_direct = Vu / (Bo * d)
    eX = (Mux * 1e3) / (Vu * 1e3) * 1e3  # mm
    eY = (Muy * 1e3) / (Vu * 1e3) * 1e3  # mm
    eEQ = math.sqrt(eX ** 2 + eY ** 2)
    r = (Cx + d + Cy + d) / 2
    B_b = 1 + ((1.5 * eEQ) / r)
    vu = B_b * (Vu / (Bo * d)) * 1e3  # MPa

    st.subheader("📊 Punching Shear Check Result")
    if vu > Oo * Vc:
        st.error("❌ FAILED: The slab fails in punching shear even with moments included.")
        if Vu <= Oo * Vc_max:
            st.warning("⚠️ Shear Reinforcement is needed.")

            with st.expander("🧮 Shear Reinforcement Design"):
                fy = st.number_input("Yield strength fy (MPa)", min_value=0.0, step=50.0, key="fy")
                no = st.number_input("Number of legs", min_value=1.0, step=1.0, key="legs")
                diameter = st.number_input("Bar diameter (mm)", min_value=4.0, step=1.0, key="dia")
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
            st.error("❌ FAILED: Even with shear reinforcement, the slab does not satisfy the punching shear check.")
    elif Vu <= Oo * Vc:
        st.success("✅ PASSED: Punching shear check OK. No reinforcement needed.")
    elif Vu <= Oo * Vc_max:
        st.warning("⚠️ PASSED: But shear reinforcement is required.")

    # -- Full Calculations Expander --
    with st.expander("📐 Show Full Calculations"):
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
