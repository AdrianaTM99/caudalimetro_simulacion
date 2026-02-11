import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# --- CONTROL SIDEBAR ---
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = False

# ENLACE RAW
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS Maestro (MANTENIENDO TU DISEÑO ORIGINAL)
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
    -webkit-backdrop-filter: blur(3px);
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
    left: 0;
    width: 100vw;
    background-color: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(10px);
    z-index: 999;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: center;
}

.header-content {
    width: 100%;
    max-width: 1100px;
    padding: 10px 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 15px;
}

.fixed-header h1 {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    margin: 0;
    color: white;
}

.stButton > button {
    background-color: #00d4ff !important;
    color: black !important;
    border-radius: 8px;
    font-weight: bold;
}

.equation-box {
    background: rgba(0, 0, 0, 0.5);
    border: 2px solid #00d4ff;
    border-radius: 15px;
    padding: 30px;
    margin: 20px auto;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.3);
}

.equation-large {
    font-size: 3rem !important;
    color: #00d4ff;
    font-weight: 700;
}

header[data-testid="stHeader"] { visibility: hidden; }
.stApp { background: transparent !important; }

</style>

<div class="fixed-header">
    <div class="header-content">
        <div class="header-left">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# BOTÓN ARRIBA IZQUIERDA (REAL)
col_btn, col_space = st.columns([1,10])
with col_btn:
    if st.button("📘 Panel Técnico"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open

# --- SIDEBAR CONTENIDO ---
if st.session_state.sidebar_open:
    with st.sidebar:
        st.markdown("## 📘 Panel Técnico de Referencia")

        with st.expander("⚡ Conductividades típicas"):
            st.markdown("""
            **Agua potable:** 50 – 1500 μS/cm  
            **Agua de mar:** ~50,000 μS/cm  
            **Agua desionizada:** 0.05 – 1 μS/cm  
            **Solución salina:** ~15,000 μS/cm  
            **Ácidos diluidos:** 10,000 – 80,000 μS/cm  
            """)

        with st.expander("🔩 Diámetros nominales y usos"):
            st.markdown("""
            **1/2\" (DN15):** Uso doméstico  
            **2\" (DN50):** Industria ligera  
            **4\" (DN100):** Procesos industriales  
            **8\" (DN200):** Distribución municipal  
            **12\" (DN300):** Plantas grandes  
            """)

        with st.expander("🧲 Campos magnéticos recomendados"):
            st.markdown("""
            **0.1 – 0.3 T:** Baja conductividad  
            **0.3 – 0.6 T:** Uso estándar  
            **0.6 – 1.0 T:** Señal baja  
            """)

st.write("---")

# --- RESTO DE TU CÓDIGO ORIGINAL ---
sistema = st.radio("Selecciona el Sistema de Unidades:",
                   ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"),
                   horizontal=True)

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

# (Todo tu sistema de parámetros, cálculos y gráfica queda igual)
