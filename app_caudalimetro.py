import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana", initial_sidebar_state="expanded")

# ENLACE RAW
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS MAESTRO (SOLUCIÓN AL DESPLAZAMIENTO)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    /* --- FONDO --- */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* --- CAPA CENTRAL NEGRA (FIJA) --- */
    /* Usamos fixed y left: 50% para que nunca se mueva al abrir el sidebar */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 1150px;
        height: 100vh;
        background: rgba(0, 0, 0, 0.65);
        backdrop-filter: blur(4px);
        z-index: 0;
    }
    /* --- BARRA LATERAL --- */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.95) !important;
        border-right: 2px solid #00d4ff !important;
        z-index: 10000 !important;
        position: fixed !important;  # Fija el sidebar para no desplazar contenido
        height: 100vh !important;  # Altura completa
        overflow: auto !important;
    }
    /* --- BOTÓN DE DESPLIEGUE --- */
    [data-testid="stSidebarCollapseButton"] {
        color: #00d4ff !important;
        background-color: rgba(0,0,0,0.8) !important;
        border: 1px solid #00d4ff !important;
        border-radius: 50% !important;
        position: fixed !important;
        top: 25px !important;
        left: 20px !important;
        z-index: 1000001 !important;
    }
    /* --- CONTENEDOR PRINCIPAL FIJO --- */
    /* Forzamos a que el contenido no se desplace con el margen de Streamlit */
    .stMainBlockContainer {
        margin-left: 0 !important;
        margin-right: 0 !important;
        position: fixed !important;  # Fija el contenido central
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 1150px !important;
        height: 100vh;
        overflow: auto;
        z-index: 1 !important;
    }
    .block-container {
        position: relative;
        z-index: 1;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 130px 2rem 4rem 2rem !important;
        font-family: 'Roboto', sans-serif;
    }
    /* --- HEADER PERSONALIZADO --- */
    .fixed-header {
        position: fixed; top: 0; left: 0; width: 100vw;
        z-index: 900;
        display: flex; justify-content: center;
        pointer-events: none;
    }
    .header-content {
        pointer-events: auto;
        width: 100%; max-width: 1150px;
        background-color: rgba(0, 0, 0, 0.9);
        padding: 15px; text-align: center;
        border-bottom: 2px solid #00d4ff;
        border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    /* --- COMPONENTES UI --- */
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
        border: 2px solid #00d4ff !important; background-color: #000 !important;
    }
    div[data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] > div:first-child > div {
        background-color: #00d4ff !important;
    }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; }
    
    .stButton > button {
        width: 100%; background-color: #1a5276 !important; color: white !important;
        border: 1px solid #00d4ff !important; border-radius: 8px; padding: 0.8rem;
    }
    .loading-overlay {
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
        z-index: 9999; text-align: center; background: rgba(0,0,0,0.95);
        padding: 20px; border-radius: 25px; border: 2px solid #00d4ff;
    }
    
    .equation-box {
        background: rgba(0,0,0,0.5); border: 2px solid #00d4ff; border-radius: 15px;
        padding: 25px; text-align: center; margin-top:20px;
    }
    
    p, label, .stMarkdown, h1, h2, h3 { color: white !important; }
    </style>
    <div class="fixed-header">
        <div class="header-content">
            <h1 style="color: white; margin:0; font-family: 'Roboto'; font-size: 1.8rem;">Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---
st.write("---")
st.markdown("#### Configuración de Parámetros")
# Columnas para las entradas
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    B_val = st.number_input('B: Campo Magnético (T)', 0.1, 1.0, 0.5, 0.1)
    B = st.slider('Ajustar B', 0.1, 1.0, float(B_val), 0.1, label_visibility="collapsed")
with col2:
    sigma_val = st.number_input('σ: Conductividad (μS/cm)', 1, 5000, 1000, 100)
    sigma = st.slider('Ajustar σ', 1, 5000, int(sigma_val), 100, label_visibility="collapsed")
with col3:
    D_val = st.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")
    D = st.slider('Ajustar D', 0.005, 0.050, float(D_val), 0.001, label_visibility="collapsed")
st.write("---")
# --- CÁLCULOS Y GRÁFICA ---
if st.button('🚀 Generar curva de calibración'):
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
            <div class="loading-overlay">
                <img src="{URL_GIF}" width="450">
                <p style="color:#00d4ff; font-weight:bold; margin-top:10px; font-size:1.5rem;">Calculando flujo...</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    placeholder.empty()
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma - 5)))
    V_mv = (B * D * v * f_cond * 1000)
    Q = A * v
    m = V_mv[-1] / Q[-1] if Q[-1] != 0 else 0
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q, V_mv, color='#00d4ff', linewidth=2.5)
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=9)
    ax.set_ylabel('Voltaje V (mV)', fontsize=9)
    ax.set_title('Calibración V vs Q', fontsize=11)
    ax.grid(True, alpha=0.1)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)
    st.markdown(f"""
        <div class="equation-box">
            <h2 style="color:#00d4ff; font-size: 2.5rem; margin:0;">V = {m:.4f} · Q</h2>
        </div>
    """, unsafe_allow_html=True)
st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
