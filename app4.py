# --- Initial Setup ---
import streamlit as st
import math

st.set_page_config(page_title="Punching Shear Check", layout="wide")
st.title("🔍 Two-Way Punching Shear Check (ACI 318-19)")

# --- Constants ---
phi = 0.75
cover = 35  # mm

# --- Setup Session State ---
if "run_check" not in st.session_state:
    st.session_state.run_check = False

# --- Input Section ---
st.header("📥 Input Parameters")
col1, col2 = st.columns(2)
with col1:
    Cx = st.number_input("Column dimension Cx (mm)", min_value=0.0, step=10.0)
    Vu = st.number_input("Factored shear Vu (kN)", min_value=0.0, step=10.0)
    Mux = st.number_input("Moment Mux (kN·m)", min_value=0.0, step=10.0)
with col2:
    Cy = st.number_input("Column dimension Cy (mm)", min_value=0.0, step=10.0)
    h = st.number_input("Slab thickness h (mm)", min_value=0.0, step=10.0)
    Muy = st.number_input("Moment Muy (kN·m)", min_value=0.0, step=10.0)

fc = st.number_input("Concrete compressive strength f'c (MPa)", min_value=0.0, step=5.0)

# --- Trigger Button ---
if st.button("🔎 Run Check"):
    st.session_state.run_check = True  # Store trigger flag

# --- Run Punching Shear Check If Triggered ---
if st.session_state.run_check:
    d = h - cover
    b = 2 * (Cx + Cy + 2 * d)
    Vc = 0.33 * math.sqrt(fc) * b * d * 1e-3
    Vc_max = 2 * Vc
    D_d = d / 2
    Bo = 2 * ((Cx + 2 * D_d) + (Cy + 2 * D_d))
    vu_direct = Vu / (Bo * d)
    eX = (Mux * 1e6) / (Vu * 1e3)
    eY = (Muy * 1e6) / (Vu * 1e3)
    eEQ = math.sqrt(eX**2 + eY**2)
    r = (Cx + d + Cy + d) / 2
    B_b = 1 + ((1.5 * eEQ) / r)
    vu = B_b * (Vu / (Bo * d)) * 1e3

    # --- Results Display ---
    st.subheader("📊 Punching Shear Check Result")

    if Vu > phi * Vc_max:
        st.error("❌ FAILED: Even with shear reinforcement.")
    elif Vu > phi * Vc:
        st.warning("⚠️ SUCCEEDED: But shear reinforcement is required.")

        # --- Shear Reinforcement Section ---
        st.subheader("🧮 Shear Reinforcement Design")
        fy = st.number_input("Yield Strength fy (MPa)", min_value=0.0, step=10.0, key="fy")
        no_legs = st.number_input("Number of Legs", min_value=1, step=1, key="legs")
        dia = st.number_input("Bar Diameter (mm)", min_value=6.0, step=2.0, key="dia")
        spacing = st.number_input("Stirrup Spacing (mm)", min_value=50.0, step=25.0, key="spacing")

        if st.button("🔧 Check Reinforcement"):
            As = math.pi * (dia / 2) ** 2
            vs = (As * fy * d * no_legs) / (spacing * 1000)  # kN
            Vs_required = (Vu - phi * Vc) / phi

            st.write(f"🔹 Required Vs: `{Vs_required:.2f} kN`")
            st.write(f"🔹 Provided Vs: `{vs:.2f} kN`")

            if vs >= Vs_required:
                st.success("✅ Shear reinforcement is sufficient.")
            else:
                st.error("❌ Shear reinforcement is NOT sufficient.")
    else:
        st.success("✅ SUCCEEDED: No shear reinforcement required.")

    # --- Optional Calculation Output ---
    st.header("📐 Calculation Details")
    st.markdown(f"**Effective Depth d** = `{round(d)} mm`")
    st.markdown(f"**Critical Perimeter b** = `{round(b)} mm`")
    st.markdown(f"**Concrete Shear Vc** = `{round(Vc)} kN`")
    st.markdown(f"**φVc** = `{round(phi * Vc)} kN`")
    st.markdown(f"**Max Vc (2·Vc)** = `{round(Vc_max)} kN`")
    st.markdown(f"**φVc-max** = `{round(phi * Vc_max)} kN`")
    st.markdown(f"**eX** = `{round(eX, 2)} mm`")
    st.markdown(f"**eY** = `{round(eY, 2)} mm`")
    st.markdown(f"**eEQ** = `{round(eEQ, 2)} mm`")
    st.markdown(f"**β (Amplification)** = `{round(B_b, 3)}`")
    st.markdown(f"**vu** = `{round(vu, 2)} MPa`")
