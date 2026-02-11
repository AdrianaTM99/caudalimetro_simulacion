import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana", initial_sidebar_state="expanded")

# ENLACE RAW CORREGIDO
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS Maestro con BOTÓN DE BARRA LATERAL FORZADO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo base */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* CAPA CENTRAL DESENFOCADA */
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

    /* HEADER FLOTANTE CENTRADO */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        z-index: 999;
        display: flex;
        justify-content: center;
    }
    .header-content {
        width: 100%;
        max-width: 1150px;
        background-color: rgba(0, 0, 0, 0.9);
        padding: 15px;
        text-align: center;
        border-bottom: 2px solid #00d4ff;
        border-bottom-left-radius: 15px;
        border-bottom-right-radius: 15px;
    }

    /* FORZAR EL BOTÓN DEL SIDEBAR (FLECHA) */
    /* Lo hacemos gigante y con brillo neón */
    button[kind="headerNoPadding"] {
        background-color: #00d4ff !important;
        color: black !important;
        width: 50px !important;
        height: 50px !important;
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        z-index: 1000000 !important;
        border-radius: 10px !important;
        box-shadow: 0px 0px 20px #00d4ff !important;
        display: flex !important;
        visibility: visible !important;
    }

    /* ESTILO BARRA LATERAL */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.95) !important;
        border-right: 3px solid #00d4ff !important;
    }

    /* Ajuste de contenido para no chocar con el header */
    .block-container {
        position: relative;
        z-index: 1;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 130px 2rem 2rem 2rem !important;
    }

    /* Colores Neón para Sliders y Radios */
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child { border: 2px solid #00d4ff !important; }
    div[data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] > div:first-child > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; border: 2px solid white !important; }

    header[data-testid="stHeader"] { visibility: hidden; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1 style="color: white; margin: 0; font-family: 'Roboto';">Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CONTENIDO BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>📋 Referencias</h2>", unsafe_allow_html=True)
    st.write("Conductividad (σ) según el fluido:")
    
    fluidos = {
        "Agua Destilada": 0.5, "Agua Potable": 500, "Agua de Mar": 50000,
        "Leche": 5000, "Zumo de Frutas": 3000, "Ácido Sulfúrico (30%)": 700000
    }
    
    # Tabla dinámica
    st.table(list(fluidos.items()))
    st.info("Para ocultar, pulsa la flecha dentro de este panel.")

# --- CUERPO PRINCIPAL ---
st.markdown("### Ajustes del Sistema")
sistema = st.radio("Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

st.write("---")

col1, col2, col3 = st.columns(3)
with col1:
    B = st.slider('B: Campo Magnético', 0.1, 1.5, 0.5)
with col2:
    sigma = st.slider('σ: Conductividad', 1.0, 5000.0, 1000.0)
with col3:
    D = st.slider('D: Diámetro', 0.005, 0.5, 0.0127)

if st.button('🚀 Ejecutar Simulación'):
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f'<div style="text-align:center;"><img src="{URL_GIF}" width="350"></div>', unsafe_allow_html=True)
        time.sleep(2)
    placeholder.empty()

    # Gráfica
    x = np.linspace(0, 10, 100)
    y = B * D * x
    fig, ax = plt.subplots()
    plt.style.use('dark_background')
    ax.plot(x, y, color='#00d4ff', linewidth=3)
    ax.set_title("Relación Voltaje vs Caudal", color="#00d4ff")
    st.pyplot(fig)

st.caption("Adriana Teixeira Mendoza - UCV 2026")
