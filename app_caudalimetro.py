import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# =====================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# =====================================================
st.set_page_config(
    layout="wide",
    page_title="Simulador Adriana",
    initial_sidebar_state="collapsed"
)

is_mobile = st.session_state.get("is_mobile", False)
if "grafica_interactiva" not in st.session_state:
    st.session_state.grafica_interactiva = False

URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# =====================================================
# 2. CSS GENERAL
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
[data-testid="stAppViewContainer"] {
    background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.title-bar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(3px);
    padding: 35px 0 10px 0;
    text-align: center;
    z-index: 1000;
    border-bottom: 2px solid #00d4ff;
}
.main-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00d4ff, #ff8c00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: 1.5rem;
    color: #cccccc;
    margin-top: 5px;
}
.block-container {
    position: relative;
    z-index: 1;
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding: 200px 2rem 4rem 2rem !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-bar">
    <div class="main-title">
        Simulador de Caudalímetro Electromagnético
    </div>
    <div class="subtitle">
        Modelado y calibración digital de flujo industrial
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SISTEMA DE UNIDADES
# =====================================================
sistema = st.radio(
    "Selecciona el Sistema de Unidades:",
    ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"),
    horizontal=True
)

if sistema == "Métrico (T, μS/cm, m)":
    u_b, u_sig, u_d, u_q = "T", "μS/cm", "m", "m³/s"
    conv_cond = 1
    conv_diam = 1
    conv_vel = 1
    b_min, b_max, b_def = 0.1, 1.5, 0.5
    sig_min, sig_max, sig_def = 1.0, 5000.0, 1000.0
    d_min, d_max, d_def = 0.005, 0.500, 0.0127
    conv_q = 1.0
else:
    u_b, u_sig, u_d, u_q = "G", "μmhos/in", "in", "GPM"
    conv_cond = 2.54
    conv_diam = 1 / 25.4
    conv_vel = 3.28084
    b_min, b_max, b_def = 1000.0, 15000.0, 5000.0
    sig_min, sig_max, sig_def = 2.5, 12700.0, 2540.0
    d_min, d_max, d_def = 0.2, 20.0, 0.5
    conv_q = 15850.3

# =====================================================
# PARÁMETROS
# =====================================================
st.markdown(f"#### Configuración de Parámetros ({sistema})")

B_val = st.number_input(
    f'B: Campo Magnético ({u_b})',
    float(b_min), float(b_max), float(b_def)
)

B_user = st.slider(
    'Ajustar B',
    float(b_min), float(b_max), float(B_val),
    key="B_slider"
)

st.write("")

sig_val = st.number_input(
    f'σ: Conductividad ({u_sig})',
    float(sig_min), float(sig_max), float(sig_def)
)

sigma_user = st.slider(
    'Ajustar σ',
    float(sig_min), float(sig_max), float(sig_val),
    key="sig_slider"
)

st.write("")

D_val = st.number_input(
    f'D: Diámetro ({u_d})',
    float(d_min), float(d_max), float(d_def),
    format="%.4f"
)

D_user = st.slider(
    'Ajustar D',
    float(d_min), float(d_max), float(D_val),
    key="D_slider"
)

st.write("---")

# =====================================================
# CÁLCULOS
# =====================================================
if sistema == "Americano (G, mhos/in, in)":
    B_si = B_user / 10000.0
    D_si = D_user * 0.0254
    sigma_si = sigma_user / 2.54
else:
    B_si = B_user
    D_si = D_user
    sigma_si = sigma_user

A_m2 = np.pi * (D_si / 2)**2
v = np.linspace(0.1, 5.0, 100)
f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
V_mv = (B_si * D_si * v * f_cond * 1000)
Q_plot = (A_m2 * v) * conv_q
coef = np.polyfit(Q_plot, V_mv, 1)
m_eq = coef[0]
b_eq = coef[1]
V_pred = m_eq * Q_plot + b_eq
SS_res = np.sum((V_mv - V_pred)**2)
SS_tot = np.sum((V_mv - np.mean(V_mv))**2)
R2 = 1 - SS_res / SS_tot

# =====================================================
# GRÁFICA
# =====================================================
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=Q_plot,
    y=V_mv,
    mode='markers',
    name="Datos simulados"
))

fig.add_trace(go.Scatter(
    x=Q_plot,
    y=V_pred,
    mode='lines',
    name="Curva de calibración"
))

st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
### Ecuación Ajustada
V = {m_eq:.4f} · Q + {b_eq:.4f}
""")

st.write(f"Coeficiente de determinación R² = {R2:.6f}")
st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
