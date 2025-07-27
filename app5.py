import math
import streamlit as st

Oo = 0.75

def punching_shear_check(Cx, Cy, h, Vu, Mux, Muy, fc):
    d = h - 40
    b = 2*(Cx + Cy + 2*d) 
    Vc = 0.33 * math.sqrt(fc) * b * d * (10 ** -3)
    Vc_max = Vc * 2

    D_d = d / 2
    Bo = 2*((Cx + 2*D_d) + (Cy + 2*D_d))
    vu_direct = Vu / (Bo * d)
    eX = (Mux * 10 ** 3) / (Vu * 10 ** 3) * 10 ** 3 
    eY = (Muy * 10 ** 3) / (Vu * 10 ** 3) * 10 ** 3
    eEQ = math.sqrt((eX ** 2) + (eY ** 2))
    r = (Cx + d + Cy + d) / 2
    B_b = 1 + ((1.5 * eEQ) / r)
    vu = B_b * (Vu / (Bo * d)) * 10 ** 3

    results = {}
    results['b'] = b
    results['Vc'] = Vc
    results['Vc_max'] = Vc_max
    results['vu'] = vu
    results['vu_direct'] = vu_direct
    results['eX'] = eX
    results['eY'] = eY
    results['eEQ'] = eEQ
    results['B_b'] = B_b
    results['d'] = d
    results['Bo'] = Bo
    results['r'] = r

    if vu > Oo * Vc:
        status = "FAIL: Slab fails in punching shear even when including moments in both directions."
        reinforcement_needed = False
    elif Vu <= Oo * Vc:
        status = "SUCCESS: No reinforcement needed."
        reinforcement_needed = False
    elif Vu > Oo * Vc and Vu <= Oo * Vc_max:
        status = "SUCCESS but shear reinforcement is needed."
        reinforcement_needed = True
    else:
        status = "FAIL: Slab fails even with shear reinforcement."
        reinforcement_needed = False

    results['status'] = status
    results['reinforcement_needed'] = reinforcement_needed
    return results

def shear_reinforcement(Vu, Vc, d, fy, no, diameter, spacing):
    Vs = (Vu - (Oo * Vc)) / Oo
    As = (math.pi * (diameter / 2) ** 2)
    vs = (As * fy * d * no) / (spacing * 1000)
    return Vs, vs

def main():
    st.title("Punching Shear Check for Slab")

    st.sidebar.header("Input Parameters")
    Cx = st.sidebar.number_input("Enter Cx (mm)", min_value=0.0, value=200.0, step=10.0)
    Cy = st.sidebar.number_input("Enter Cy (mm)", min_value=0.0, value=200.0, step=10.0)
    h = st.sidebar.number_input("Enter Slab Thickness (mm)", min_value=50.0, value=200.0, step=10.0)
    Vu = st.sidebar.number_input("Enter Vu (kN)", min_value=0.0, value=150.0, step=10.0)
    Mux = st.sidebar.number_input("Enter Mux (kN·mm)", min_value=0.0, value=0.0, step=10.0)
    Muy = st.sidebar.number_input("Enter Muy (kN·mm)", min_value=0.0, value=0.0, step=10.0)
    fc = st.sidebar.number_input("Enter Concrete strength fc (MPa)", min_value=1.0, value=25.0, step=1.0)

    if st.button("Check Punching Shear"):
        results = punching_shear_check(Cx, Cy, h, Vu, Mux, Muy, fc)

        st.subheader("Results:")
        st.write(f"Effective depth, d = {results['d']:.2f} mm")
        st.write(f"Perimeter b = {results['b']:.2f} mm")
        st.write(f"Concrete shear capacity, Vc = {results['Vc']:.2f} kN")
        st.write(f"Maximum concrete shear capacity, Vc_max = {results['Vc_max']:.2f} kN")
        st.write(f"Shear stress vu = {results['vu']:.2f} MPa")
        st.write(f"Equivalent eccentricity, eEQ = {results['eEQ']:.2f} mm")
        st.write(f"Beta factor, β = {results['B_b']:.3f}")
        st.write(f"Status: **{results['status']}**")

        if results['reinforcement_needed']:
            st.subheader("Shear Reinforcement Check")

            fy = st.number_input("Yield strength fy (MPa)", min_value=100.0, max_value=600.0, value=415.0, step=5.0)
            no = st.number_input("Number of legs", min_value=1, max_value=10, value=2, step=1)
            diameter = st.number_input("Bar diameter (mm)", min_value=5.0, max_value=50.0, value=12.0, step=1.0)
            spacing = st.number_input("Spacing (mm)", min_value=50.0, max_value=1000.0, value=200.0, step=10.0)

            if st.button("Calculate Shear Reinforcement"):
                Vs, vs = shear_reinforcement(Vu, results['Vc'], results['d'], fy, no, diameter, spacing)
                st.write(f"Required shear reinforcement Vs = {Vs:.2f} kN")
                st.write(f"Provided shear reinforcement vs = {vs:.2f} kN")

                if vs >= Vs:
                    st.success("OK: Shear reinforcement is sufficient.")
                else:
                    st.error("FAILED: Shear reinforcement is insufficient. Try changing parameters.")

if __name__ == "__main__":
    main()
