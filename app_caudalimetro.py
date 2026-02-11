import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="Simulador Adriana",
    initial_sidebar_state="collapsed"
)

URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# =====================================================
# 🔹 SIDEBAR FIJA
# =====================================================
st.markdown("""
<style>

section[data-testid="stSidebar"] {
    position: fixed !important;
    left: 0;
    top: 0;
    height: 100vh;
    width: 330px !important;
    background: rgba(0,0,0,0.97) !important;
    backdrop-filter: blur(10px);
    border-right: 2px solid #00d4ff;
    z-index: 1000;
}

div[data-testid="collapsedControl"] {
    position: fixed !important;
    top: 10px !important;
    left: 10px !important;
    z-index: 3000 !important;
}

/* NO ocultamos el header */
header[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stAppViewContainer"] {
    margin-left: 0 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# CONTENIDO SIDEBAR
# =========================
with st.sidebar:

    st.markdown("## 📘 Biblioteca Técnica")

    with st.expander("🔬 Conductividades de Fluidos Comunes", expanded=True):
        st.markdown("""
        | Fluido | Conductividad (μS/cm aprox.) |
        |---------|-----------------------------|
        | Agua destilada | 0.5 – 5 |
        | Agua potable | 50 – 1500 |
        | Agua de mar | 50,000 |
        | Leche | 4000 – 6000 |
        | Sangre | 7000 |
        | Soluciones salinas | 10,000 – 80,000 |
        | Ácidos diluidos | 10,000 – 100,000 |
        """)

    with st.expander("🔵 Diámetros Nominales y Usos", expanded=True):
        st.markdown("""
        | DN | Diámetro (mm) | Uso Común |
        |----|---------------|------------|
        | DN15 | 15 mm | Laboratorio |
        | DN25 | 25 mm | Procesos ligeros |
        | DN50 | 50 mm | Agua potable |
        | DN100 | 100 mm | Industria alimentaria |
        | DN200 | 200 mm | PTAR |
        | DN500 | 500 mm | Sistemas municipales |
        """)

    with st.expander("🧲 Campos Magnéticos Recomendados", expanded=True):
        st.markdown("""
        | Campo (T) | Aplicación |
        |------------|------------|
        | 0.1 – 0.3 T | Alta conductividad |
        | 0.3 – 0.6 T | Uso industrial estándar |
        | 0.6 – 1.0 T | Baja conductividad |
        | 1.0 – 1.5 T | Aplicaciones especiales |
        """)

    with st.expander("🌊 Velocidades Recomendadas", expanded=True):
        st.markdown("""
        | Aplicación | Velocidad Recomendada |
        |-------------|----------------------|
        | Agua potable | 1 – 3 m/s |
        | Industria química | 1 – 5 m/s |
        | Lodos | 0.5 – 2 m/s |
        | Alimentos | 1 – 4 m/s |
        """)

# =====================================================
# INTERFAZ PRINCIPAL
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

[data-testid="stAppViewContainer"] {
    background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 1150px;
    height: 100vh;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(3px);
    z-index: 0;
}

.block-container {
    position: relative;
    z-index: 1;
    font-family: 'Roboto', sans-serif;
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding: 100px 2rem 4rem 2rem !important;
    color: white !important;
}

.fixed-header {
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 1100px;
    background-color: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(10px);
    z-index: 900;
    display: flex;
    justify-content: center;
}

.header-content {
    width: 100%;
    max-width: 1100px;
    padding: 10px 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
}

.fixed-header h1 {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    margin: 0;
    color: white;
}

.equation-box {
    background: rgba(0, 0, 0, 0.5);
    border: 2px solid #00d4ff;
    border-radius: 15px;
    padding: 30px;
    margin: 20px auto;
    text-align: center;
}

.equation-large {
    font-size: 3rem !important;
    color: #00d4ff;
    font-weight: 700;
}

.loading-overlay {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999;
    text-align: center;
    background: rgba(0, 0, 0, 0.95);
    padding: 20px;
    border-radius: 25px;
    border: 2px solid #00d4ff;
}

</style>

<div class="fixed-header">
    <div class="header-content">
        <h1>Simulación de Caudalímetro Electromagnético</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# --- RESTO DEL CÓDIGO SIN CAMBIOS ---
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

if sistema == "Métrico (T, μS/cm, m)":
    u_b, u_sig, u_d, u_q = "T", "μS/cm", "m", "m³/s"
    b_min, b_max, b_def = 0.1, 1.5, 0.5
    sig_min, sig_max, sig_def = 1.0, 5000.0, 1000.0
    d_min, d_max, d_def = 0.005, 0.500, 0.0127
    conv_q = 1.0
else:
    u_b, u_sig, u_d, u_q = "G", "μmhos/in", "in", "GPM"
    b_min, b_max, b_def = 1000.0, 15000.0, 5000.0
    sig_min, sig_max, sig_def = 2.5, 12700.0, 2540.0
    d_min, d_max, d_def = 0.2, 20.0, 0.5
    conv_q = 15850.3

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
