import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# ENLACE RAW CORREGIDO
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS Maestro (Todo Azul Neón + Encabezado Centrado)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de imagen base */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* CAPA CENTRAL CON DESENFOQUE */
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

    /* HEADER AJUSTADO SOLO AL CENTRO */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        background-color: transparent;
        z-index: 999;
        display: flex;
        justify-content: center;
    }

    .header-content {
        width: 100%;
        max-width: 1150px;
        background-color: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(10px);
        padding: 15px 2rem;
        text-align: center;
        border-bottom: 2px solid #00d4ff;
        border-bottom-left-radius: 15px;
        border-bottom-right-radius: 15px;
    }

    header[data-testid="stHeader"] { visibility: hidden; }
    .stApp { background: transparent !important; }

    /* Forzar visibilidad del botón de la barra lateral en azul neón */
    [data-testid="stSidebarCollapseButton"] {
        background-color: rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
        border: 1px solid #00d4ff !important;
        top: 85px !important;
    }

    /* Estilo barra lateral */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.9) !important;
        border-right: 2px solid #00d4ff !important;
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

    /* Sliders y Radio en Azul Neón */
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
        border: 2px solid #00d4ff !important;
        background-color: #000000 !important;
    }
    div[data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] > div:first-child > div {
        background-color: #00d4ff !important;
    }
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; border: 2px solid white !important; }

    .stButton > button {
        width: 100%;
        background-color: #1a5276 !important;
        color: white !important;
        border: 1px solid #00d4ff !important;
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
    }
    .equation-large { font-size: 2.5rem; color: #00d4ff; font-weight: 700; }

    p, label, .stMarkdown { font-size: 1.1rem !important; color: white !important; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR: LISTA DE CONDUCTIVIDADES ---
fluidos = {
    "Agua Destilada": 0.5, "Agua Potable": 500, "Agua de Mar": 50000,
    "Leche": 5000, "Zumo de Frutas": 3000, "Ácido Sulfúrico (30%)": 700000
}

with st.sidebar:
    st.markdown("### 📋 Panel de Referencia")
    st.write("Valores típicos de conductividad (σ):")
    # Tabla dinámica según el sistema seleccionado
    
# --- LÓGICA PRINCIPAL ---
col_sidebar_trigger, _ = st.columns([1, 3])
with col_sidebar_trigger:
    if st.button("📂 Abrir/Cerrar Referencias"):
        st.info("Usa la flecha azul neón en la esquina superior izquierda.")

sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

# Actualizar tabla en sidebar
with st.sidebar:
    if sistema == "Métrico (T, μS/cm, m)":
        tabla = {f: f"{v:,} μS/cm" for f, v in fluidos.items()}
    else:
        tabla = {f: f"{v * 2.54:,} μmhos/in" for f, v in fluidos.items()}
    st.table(list(tabla.items()))

st.write("---")

# --- PARÁMETROS ---
st.markdown(f"#### Parámetros de Simulación ({sistema})")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B_val = st.number_input(f'B: Campo Magnético', 0.1, 15000.0, 0.5)
    B_user = st.slider('Ajuste fino B', 0.1, 15000.0, float(B_val), label_visibility="collapsed")
with col2:
    sig_val = st.number_input(f'σ: Conductividad', 1.0, 700000.0, 1000.0)
    sigma_user = st.slider('Ajuste fino σ', 1.0, 700000.0, float(sig_val), label_visibility="collapsed")
with col3:
    D_val = st.number_input(f'D: Diámetro', 0.005, 20.0, 0.0127, format="%.4f")
    D_user = st.slider('Ajuste fino D', 0.005, 20.0, float(D_val), label_visibility="collapsed")

st.write("---")

# --- SIMULACIÓN ---
if st.button('🚀 Generar curva de calibración'):
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f'<div style="text-align:center;"><img src="{URL_GIF}" width="400"><p style="color:#00d4ff;">Procesando datos...</p></div>', unsafe_allow_html=True)
        time.sleep(2)
    placeholder.empty()

    # Cálculos simplificados
    v = np.linspace(0.1, 5.0, 100)
    V_mv = (B_user * D_user * v * 0.95) # Factor de ejemplo
    Q_plot = (np.pi * (D_user/2)**2) * v
    
    fig, ax = plt.subplots(figsize=(10, 4))
    plt.style.use('dark_background')
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=2)
    ax.set_xlabel("Caudal")
    ax.set_ylabel("Voltaje (mV)")
    st.pyplot(fig)

    st.markdown(f'<div class="equation-box"><div class="equation-large">V = {(V_mv[-1]/Q_plot[-1]):.4f} · Q</div></div>', unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
