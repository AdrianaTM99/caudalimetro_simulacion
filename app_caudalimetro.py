import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    layout="wide",
    page_title="Simulador Adriana",
    initial_sidebar_state="expanded"
)

URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# =========================================================
# CSS MAESTRO (CENTRO FIJO + BOTÓN VISIBLE)
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

/* ===== FONDO BASE ===== */
[data-testid="stAppViewContainer"] {
    background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* ===== CAPA CENTRAL OSCURA (SOLO CENTRO) ===== */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 1100px;
    height: 100vh;
    background: rgba(0,0,0,0.75);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    z-index: 0;   /* IMPORTANTE: menor que el botón */
}

/* ===== CONTENIDO PRINCIPAL ===== */
.block-container {
    position: relative;
    z-index: 1;
    font-family: 'Roboto', sans-serif;
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding: 100px 2rem 4rem 2rem !important;
    color: white !important;
}

/* ===== HEADER SUPERIOR ===== */
.fixed-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(8px);
    z-index: 900;
    display: flex;
    justify-content: center;
}

.header-content {
    width: 100%;
    max-width: 1100px;
    padding: 10px 2rem;
}

.fixed-header h1 {
    margin: 0;
    color: white;
}

/* Ocultar header default */
header[data-testid="stHeader"] { visibility: hidden; }

/* ===== BOTÓN COLAPSABLE (FORZAR VISIBILIDAD) ===== */
div[data-testid="collapsedControl"] {
    z-index: 2000 !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: rgba(0,0,0,0.95) !important;
}

/* ===== ESTILOS VARIOS ===== */
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

.stButton > button {
    width: 100%;
    background-color: #1a5276 !important;
    color: white !important;
}

p, label { color: white !important; }

</style>

<div class="fixed-header">
    <div class="header-content">
        <h1>Simulación de Caudalímetro Electromagnético</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR CON CONTENIDO COMPLETO
# =========================================================

with st.sidebar:

    st.markdown("## 📘 Biblioteca Técnica")

    with st.expander("🔬 Conductividades", expanded=True):
        st.markdown("""
        Agua destilada: 0.5 – 5 μS/cm  
        Agua potable: 50 – 1500 μS/cm  
        Agua de mar: 50,000 μS/cm  
        """)

    with st.expander("🔵 Diámetros Nominales", expanded=True):
        st.markdown("""
        DN15 – Laboratorio  
        DN50 – Agua potable  
        DN200 – PTAR  
        """)

    with st.expander("🌊 Velocidades Recomendadas", expanded=True):
        st.markdown("""
        Agua potable: 1 – 3 m/s  
        Industria química: 1 – 5 m/s  
        """)

# =========================================================
# CONTENIDO PRINCIPAL (TU INTERFAZ ORIGINAL)
# =========================================================

sistema = st.radio(
    "Selecciona el Sistema de Unidades:",
    ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"),
    horizontal=True
)

if sistema == "Métrico (T, μS/cm, m)":
    u_q = "m³/s"
    conv_q = 1.0
else:
    u_q = "GPM"
    conv_q = 15850.3

st.write("---")

col1, col2, col3 = st.columns(3)

with col1:
    B_user = st.slider("Campo Magnético", 0.1, 1.5, 0.5)
with col2:
    sigma_user = st.slider("Conductividad", 1.0, 5000.0, 1000.0)
with col3:
    D_user = st.slider("Diámetro", 0.005, 0.5, 0.0127)

if st.button('🚀 Generar curva de calibración'):

    A_m2 = np.pi * (D_user / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    V_mv = (B_user * D_user * v * 1000)
    Q_plot = (A_m2 * v) * conv_q

    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.plot(Q_plot, V_mv)
    ax.set_xlabel(f'Caudal ({u_q})')
    ax.set_ylabel('Voltaje (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
