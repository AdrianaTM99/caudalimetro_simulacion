import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página (Estado inicial: Abierto para que la veas de una vez)
st.set_page_config(layout="wide", page_title="Simulador Adriana", initial_sidebar_state="expanded")

# ENLACE RAW
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS Maestro (Corregido para no tapar el botón lateral)
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

    /* CAPA CENTRAL CON DESENFOQUE - Ajustada para no interferir con el Sidebar */
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

    /* ESTILO BARRA LATERAL (SIDEBAR) */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.9) !important;
        border-right: 2px solid #00d4ff !important;
        z-index: 100;
    }

    /* BOTÓN DE DESPLIEGUE (Flecha superior izquierda) */
    [data-testid="stSidebarCollapseButton"] {
        background-color: #00d4ff !important;
        color: black !important;
        border-radius: 5px !important;
        top: 10px !important;
    }

    /* HEADER CENTRADO */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        z-index: 99;
        display: flex;
        justify-content: center;
        pointer-events: none; /* Permite que los clics pasen a través si es necesario */
    }

    .header-content {
        pointer-events: auto; /* El título sí recibe clics */
        width: 100%;
        max-width: 1100px;
        background-color: rgba(0, 0, 0, 0.85);
        padding: 15px;
        text-align: center;
        border-bottom: 2px solid #00d4ff;
        border-bottom-left-radius: 20px;
        border-bottom-right-radius: 20px;
    }

    .block-container {
        position: relative;
        z-index: 1;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 120px 2rem 4rem 2rem !important;
    }

    header[data-testid="stHeader"] { background: transparent !important; }
    
    /* UI AZUL NEÓN */
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child { border: 2px solid #00d4ff !important; }
    div[data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] > div:first-child > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; border: 2px solid white !important; }
    
    .equation-box {
        background: rgba(0, 0, 0, 0.5);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
    }

    p, label, .stMarkdown { color: white !important; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1 style="color: white; margin:0; font-family: 'Roboto';">Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CONTENIDO DE LA BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>📋 Referencias σ</h2>", unsafe_allow_html=True)
    st.write("Conductividades típicas (μS/cm):")
    
    data = {
        "Fluido": ["Agua Destilada", "Agua Potable", "Agua de Mar", "Leche", "Zumo", "Ácido Sulf."],
        "Valor (μS/cm)": [0.5, 500, 50000, 5000, 3000, 700000]
    }
    st.table(data)
    
    st.markdown("---")
    st.info("💡 Puedes ocultar esta barra tocando la flecha azul arriba a la izquierda.")

# --- CUERPO PRINCIPAL ---
sistema = st.radio("Sistema de Unidades:", ("Métrico", "Americano"), horizontal=True)

st.write("---")

col1, col2, col3 = st.columns(3)
with col1:
    B_user = st.slider('B: Campo Magnético', 0.1, 2.0, 0.5)
with col2:
    sigma_user = st.slider('σ: Conductividad', 1.0, 10000.0, 1000.0)
with col3:
    D_user = st.slider('D: Diámetro', 0.005, 0.5, 0.0127)

if st.button('🚀 Generar curva de calibración'):
    # Simulación de carga
    with st.spinner('Procesando...'):
        time.sleep(1)
        
    # Gráfica Simple
    v = np.linspace(0, 10, 100)
    V_mv = B_user * D_user * v * 0.98
    
    fig, ax = plt.subplots()
    plt.style.use('dark_background')
    ax.plot(v, V_mv, color='#00d4ff', linewidth=3)
    ax.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    st.pyplot(fig)

    st.markdown(f"""
        <div class="equation-box">
            <h2 style="color:#00d4ff; margin:0;">V = {(B_user*D_user):.4f} · Q</h2>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
