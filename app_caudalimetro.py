import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# =====================================
# CONFIGURACIÓN DE PÁGINA
# =====================================
st.set_page_config(
    layout="wide",
    page_title="Simulador Adriana",
    initial_sidebar_state="collapsed"
)

URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# =====================================
# SIDEBAR FIJA (SIN TAPAR BOTÓN)
# =====================================
st.markdown("""
<style>

/* Sidebar fija */
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

/* Botón nativo visible */
div[data-testid="collapsedControl"] {
    z-index: 3000 !important;
}

/* No desplazar contenido */
[data-testid="stAppViewContainer"] {
    margin-left: 0 !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# CONTENIDO SIDEBAR
# =====================================
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

# =====================================
# FONDO Y ESTILO GENERAL
# =====================================
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

/* Capa oscura SOLO en el centro */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 1100px;
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
    padding: 120px 2rem 4rem 2rem !important;
    color: white !important;
}

/* HEADER CENTRADO (NO 100vw) */
.fixed-header {
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 1100px;
    background-color: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(10px);
    z-index: 900;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: 15px 2rem;
    text-align: center;
}

.fixed-header h1 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 700;
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
    font-size: 3rem;
    color: #00d4ff;
    font-weight: 700;
}

header[data-testid="stHeader"] { visibility: hidden; }
.stApp { background: transparent !important; }

</style>

<div class="fixed-header">
    <h1>Simulación de Caudalímetro Electromagnético</h1>
</div>
""", unsafe_allow_html=True)

# =====================================
# SISTEMA DE UNIDADES
# =====================================
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

# =====================================
# PARÁMETROS
# =====================================
st.markdown(f"#### Configuración de Parámetros ({sistema})")

col1, col2, col3 = st.columns(3)

with col1:
    B_user = st.slider(f'B ({u_b})', b_min, b_max, b_def)

with col2:
    sigma_user = st.slider(f'σ ({u_sig})', sig_min, sig_max, sig_def)

with col3:
    D_user = st.slider(f'D ({u_d})', d_min, d_max, d_def)

if sistema == "Americano (G, mhos/in, in)":
    B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
else:
    B_si, D_si, sigma_si = B_user, D_user, sigma_user

if st.button('🚀 Generar curva de calibración'):

    A_m2 = np.pi * (D_si / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    V_mv = (B_si * D_si * v * 1000)

    Q_plot = A_m2 * v * conv_q
    m_eq = V_mv[-1] / Q_plot[-1]

    fig, ax = plt.subplots()
    ax.plot(Q_plot, V_mv)
    ax.set_xlabel(f'Caudal ({u_q})')
    ax.set_ylabel('Voltaje (mV)')
    st.pyplot(fig)

    st.markdown(f"""
        <div class="equation-box">
            <div class="equation-large">
                V = {m_eq:.4f} · Q
            </div>
        </div>
    """, unsafe_allow_html=True)

st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
