import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# =====================================================
# CONFIGURACIÓN
# =====================================================
st.set_page_config(
    layout="wide",
    page_title="Simulador Adriana",
    initial_sidebar_state="collapsed"
)

URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# =====================================================
# ESTILOS
# =====================================================
st.markdown("""
<style>

/* ===== BOTÓN ORIGINAL DE STREAMLIT ===== */
div[data-testid="collapsedControl"] {
    position: fixed !important;
    top: 10px !important;
    left: 10px !important;
    z-index: 9999 !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.97) !important;
    backdrop-filter: blur(10px);
    border-right: 2px solid #00d4ff;
}

/* ===== FONDO GENERAL ===== */
[data-testid="stAppViewContainer"] {
    background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Overlay solo centro */
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

/* Contenido */
.block-container {
    position: relative;
    z-index: 1;
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding: 100px 2rem 4rem 2rem !important;
    color: white !important;
}

/* ===== HEADER PERSONALIZADO (z-index MÁS BAJO que el botón) ===== */
.fixed-header {
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 1100px;
    background-color: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(10px);
    z-index: 1000; /* menor que 9999 */
    display: flex;
    justify-content: center;
}

.header-content {
    width: 100%;
    padding: 10px 2rem;
    text-align: center;
}

.fixed-header h1 { 
    font-size: 1.8rem !important; 
    font-weight: 700 !important; 
    margin: 0; 
    color: white; 
}

p, label, .stMarkdown { 
    font-size: 1.1rem !important; 
    color: white !important; 
}

</style>

<div class="fixed-header">
    <div class="header-content">
        <h1>Simulación de Caudalímetro Electromagnético</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("## 📘 Biblioteca Técnica")
    with st.expander("🔬 Conductividades", expanded=True):
        st.write("Agua destilada: 0.5–5 μS/cm")
    with st.expander("🔵 Diámetros", expanded=True):
        st.write("DN15–DN500")
    with st.expander("🧲 Campos Magnéticos", expanded=True):
        st.write("0.1–1.5 T")
    with st.expander("🌊 Velocidades", expanded=True):
        st.write("0.5–5 m/s")

# =====================================================
# SIMULADOR
# =====================================================

sistema = st.radio(
    "Selecciona el Sistema de Unidades:",
    ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"),
    horizontal=True
)

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

col1, col2, col3 = st.columns(3)

with col1:
    B_user = st.slider(f'Campo Magnético ({u_b})', b_min, b_max, b_def)

with col2:
    sigma_user = st.slider(f'Conductividad ({u_sig})', sig_min, sig_max, sig_def)

with col3:
    D_user = st.slider(f'Diámetro ({u_d})', d_min, d_max, d_def)

st.write("---")

if st.button('🚀 Generar curva de calibración'):

    A_m2 = np.pi * (D_user / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    V_mv = B_user * D_user * v * 1000
    Q_plot = A_m2 * v * conv_q

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q_plot, V_mv, linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    st.pyplot(fig)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
