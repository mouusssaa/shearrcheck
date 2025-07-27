import streamlit as st
import math

st.set_page_config(page_title="Punching Shear Check", layout="centered")
st.title("🔍 Two-Way Punching Shear Check (ACI 318-19)")

Oo = 0.75  # Strength reduction factor
i = "i"
# --- User Inputs ---
st.header("Input Parameters")
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

if st.button("🔎 Run Check"):
    d = h - 35  # Effective depth
    b = 2 * (Cx + Cy + 2 * d)
    Vc = 0.33 * math.sqrt(fc) * b * d * 1e-3  # kN
    Vc_max = 2 * Vc

    D_d = d / 2
    Bo = 2 * ((Cx + 2 * D_d) + (Cy + 2 * D_d))
    vu_direct = Vu / (Bo * d)
    eX = (Mux * 1e3) / (Vu * 1e3) * 1e3  # in mm
    eY = (Muy * 1e3) / (Vu * 1e3) * 1e3
    eEQ = math.sqrt(eX**2 + eY**2)
    r = (Cx + d + Cy + d) / 2
    B_b = 1 + ((1.5 * eEQ) / r)
    vu = B_b * (Vu / (Bo * d)) * 1e3  # in MPa

    # --- Results Section ---
    st.subheader("🔎 Result")
    if vu > Oo * Vc:
        st.error("❌ FAILED: Even when including moments in both directions, the slab FAILS in punching shear.")
    elif Vu <= Oo * Vc:
        st.success("✅ SUCCEEDED: No reinforcement needed.")
    elif Vu <= Oo * Vc_max:
        st.warning("⚠️ SUCCEEDED: But shear reinforcement is needed.")
        i = "l"
    else:
        st.error("❌ FAILED: Even with shear reinforcement.")

    if i == "l" :
        with st.button("spacing?") :
            fy = st.number_input("Enter f yeild in MPa: ")
            no = st.number_input("Enter number of legs you want to assume: ")
            diameter = st.number_input("Enter the bar diameter you want to assume: ")
            spacing = st.number_input("Enter the spacing in mm: ")
            
            if st.button("calculte") : 
                Vs = (Vu - (Oo * Vc)) / Oo
                As = ((diameter / 2) ** 2 * 3.14 )
                vs = (As * fy * d * no) / (spacing * 1000)
                if vs > Vs:
                    st.success(f"**Vs equation ({round(vs)}kN) > Vs actual ({round(Vs)}kN) **")
                elif vs == Vs:
                    st.success(f"**Vs equation ({round(vs)}kN) = Vs actual ({round(Vs)}kN) **")
                else :
                    st.error(f"**Vs equation ({round(vs)}kN) < Vs actual ({round(Vs)}kN) **")
    
    # --- Optional Calculations ---
    with st.expander("📐 Show Calculations"):
        st.write(f"**b** = {round(b)} mm")
        st.write(f"**Effective depth d** = {round(d)} mm")
        st.write(f"**Vc** = {round(Vc)} kN")
        st.write(f"**φVc** = {round(Oo * Vc)} kN")
        st.write(f"**Vc-max** = {round(Vc_max)} kN")
        st.write(f"**φVc-max** = {round(Vc_max * Oo)} kN")
        st.write(f"**eX** = {round(eX, 2)} mm")
        st.write(f"**eY** = {round(eY, 2)} mm")
        st.write(f"**eEQ** = {round(eEQ, 2)} mm")
        st.write(f"**β (B_b)** = {round(B_b, 3)}")
        st.write(f"**vu** = {round(vu, 2)} MPa")

   

            
