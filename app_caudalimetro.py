import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana", initial_sidebar_state="expanded")

# ENLACE RAW GIF
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS Maestro (Ajustado para cubrir todo y fuentes grandes)
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

    /* CAPA CENTRAL - Ensanchada para cubrir todo */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 1250px; /* Aumentado para cubrir la info */
        height: 100vh;
        background: rgba(0, 0, 0, 0.7); 
        backdrop-filter: blur(5px); 
        z-index: 0;
    }

    /* BARRA LATERAL */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.95) !important;
        border-right: 2px solid #00d4ff !important;
    }
    
    [data-testid="stSidebarCollapseButton"] {
        background-color: #00d4ff !important;
        color: black !important;
    }

    /* CONTENEDOR PRINCIPAL */
    .block-container {
        position: relative;
        z-index: 1;
        max-width: 1150px !important;
        margin: 0 auto !important;
        padding: 120px 2rem 4rem 2rem !important;
        font-size: 1.3rem !important; /* Fuente general más grande */
    }

    /* HEADER CENTRADO */
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
        max-width: 1250px;
        background: rgba(0, 0, 0, 0.9);
        padding: 20px;
        text-align: center;
        border-bottom: 3px solid #00d4ff;
        border-bottom-left-radius: 20px;
        border-bottom-right-radius: 20px;
    }

    /* FUENTES Y ETIQUETAS */
    h1, h2, h3, h4 { color: #00d4ff !important; font-weight: 700 !important; }
    label, p, .stMarkdown { font-size: 1.4rem !important; color: white !important; font-weight: 400 !important; }
    
    /* INPUTS Y SLIDERS */
    div[data-testid="stNumberInput"] input { font-size: 1.3rem !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; }

    /* ANIMACIÓN DE CARGA (OVERLAY) */
    .loading-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.85);
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        z-index: 9999;
    }

    .equation-box {
        background: rgba(0, 212, 255, 0.1);
        border: 2px solid #00d4ff;
        border-radius: 20px;
        padding: 40px;
        margin-top: 30px;
        text-align: center;
        font-size: 3.5rem !important;
        color: #00d4ff;
        font-weight: bold;
    }

    header[data-testid="stHeader"] { visibility: hidden; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1 style="margin:0; font-size: 2.2rem !important;">Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 📋 Referencias de Fluido")
    st.write("Conductividad típica (σ) en μS/cm:")
    st.markdown("""
    * **Agua Destilada:** 0.5
    * **Agua Potable:** 500
    * **Agua de Mar:** 50,000
    * **Leche:** 5,000
    * **Zumo de Frutas:** 3,000
    * **Ácido Sulfúrico:** 700,000
    """)
    st.info("Oculta este panel con la flecha superior.")

# --- CUERPO PRINCIPAL ---
st.markdown("### 1. Sistema de Unidades")
sistema = st.radio("", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

st.write("---")

# --- ENTRADA DE DATOS (UNA DEBAJO DE OTRA) ---
st.markdown("### 2. Parámetros de Simulación")

# Campo B
B_val = st.number_input('B: Campo Magnético', 0.1, 15000.0, 0.5)
B_user = st.slider('Ajuste fino de B', 0.1, 15000.0, float(B_val), label_visibility="collapsed")

# Conductividad sigma
sig_val = st.number_input('σ: Conductividad', 1.0, 700000.0, 1000.0)
sigma_user = st.slider('Ajuste fino de σ', 1.0, 700000.0, float(sig_val), label_visibility="collapsed")

# Diámetro D
D_val = st.number_input('D: Diámetro', 0.005, 20.0, 0.0127, format="%.4f")
D_user = st.slider('Ajuste fino de D', 0.005, 20.0, float(D_val), label_visibility="collapsed")

st.write("---")

# --- BOTÓN Y ANIMACIÓN ---
if st.button('🚀 GENERAR CURVA DE CALIBRACIÓN'):
    # Mostrar animación
    loading_placeholder = st.empty()
    with loading_placeholder:
        st.markdown(f"""
            <div class="loading-overlay">
                <img src="{URL_GIF}" width="450">
                <h2 style="color: #00d4ff; font-family: Roboto;">Procesando inducción electromagnética...</h2>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(3)
    loading_placeholder.empty()

    # Cálculos
    v = np.linspace(0.1, 5.0, 100)
    V_mv = B_user * D_user * v * 1000  # Ejemplo simplificado
    Q_plot = (np.pi * (D_user/2)**2) * v
    
    # Gráfica
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.style.use('dark_background')
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=4)
    ax.set_xlabel("Caudal Q", fontsize=12)
    ax.set_ylabel("Voltaje V (mV)", fontsize=12)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    # Resultado
    m = V_mv[-1] / Q_plot[-1]
    st.markdown(f'<div class="equation-box">V = {m:.4f} · Q</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
