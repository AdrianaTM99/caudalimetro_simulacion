import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana", initial_sidebar_state="expanded")

# ENLACE RAW
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS MAESTRO (ENCAPSULAMIENTO TOTAL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* --- FONDO DE PANTALLA --- */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* --- BARRA LATERAL (SIDEBAR) --- */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.95) !important;
        border-right: 2px solid #00d4ff !important;
        z-index: 10000 !important;
    }

    /* --- BOTÓN DE DESPLIEGUE AZUL NEÓN --- */
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

    /* --- CONTENEDOR CENTRAL "ISLA" --- */
    /* Este bloque contiene el fondo negro y la info juntos */
    .main-island {
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        max-width: 1100px;
        margin: 0 auto;
        color: white;
    }

    /* HEADER FIJO */
    .fixed-header {
        position: fixed; top: 0; left: 0; width: 100vw;
        z-index: 999; display: flex; justify-content: center;
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
    
    /* Ajuste de márgenes de Streamlit */
    .block-container {
        padding-top: 120px !important;
        max-width: 1200px !important;
    }

    /* UI NEÓN */
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child { border: 2px solid #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; }
    .stButton > button {
        width: 100%; background-color: #1a5276 !important; color: white !important;
        border: 1px solid #00d4ff !important; font-weight: bold;
    }

    .equation-box {
        background: rgba(0,0,0,0.6); border: 2px solid #00d4ff; border-radius: 15px;
        padding: 20px; text-align: center; margin-top:20px;
    }

    .loading-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.9); z-index: 99999;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }

    p, label, .stMarkdown, h1, h2, h3 { color: white !important; font-family: 'Roboto'; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1 style="margin:0; font-size: 1.8rem;">Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- INICIO DEL CONTENIDO ENCAPSULADO ---
# Usamos un div con la clase 'main-island' para que la info y el fondo sean uno solo
st.markdown('<div class="main-island">', unsafe_allow_html=True)

# 3. LÓGICA DE UNIDADES
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

# --- SIDEBAR (REFERENCIAS) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>📋 Referencias σ</h2>", unsafe_allow_html=True)
    fluidos = {
        "Agua Destilada": 0.5, "Agua Potable": 500, "Agua de Mar": 50000,
        "Leche": 5000, "Zumo de Frutas": 3000, "Ácido Sulfúrico": 700000
    }
    if sistema == "Métrico (T, μS/cm, m)":
        u_label, tabla = "μS/cm", {f: f"{v:,} μS/cm" for f, v in fluidos.items()}
    else:
        u_label, tabla = "μmhos/in", {f: f"{v * 2.54:,} μmhos/in" for f, v in fluidos.items()}
    st.table(list(tabla.items()))
    st.info("💡 Cierra este panel con la flecha azul arriba a la izquierda.")

st.write("---")

# --- PARÁMETROS ---
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

st.markdown(f"#### Configuración de Parámetros ({sistema})")
B_val = st.number_input(f'B: Campo Magnético ({u_b})', float(b_min), float(b_max), float(b_def))
B_user = st.slider(f'Ajustar B', float(b_min), float(b_max), float(B_val), key="B_s", label_visibility="collapsed")

sig_val = st.number_input(f'σ: Conductividad ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
sigma_user = st.slider(f'Ajustar σ', float(sig_min), float(sig_max), float(sig_val), key="s_s", label_visibility="collapsed")

D_val = st.number_input(f'D: Diámetro ({u_d})', float(d_min), float(d_max), float(d_def), format="%.4f")
D_user = st.slider(f'Ajustar D', float(d_min), float(d_max), float(D_val), key="d_s", label_visibility="collapsed")

st.write("---")

# --- CÁLCULOS Y RESULTADOS ---
if st.button('🚀 Generar curva de calibración'):
    # Overlay de carga
    st.markdown(f"""
        <div class="loading-overlay">
            <img src="{URL_GIF}" width="400">
            <h2 style="color:#00d4ff;">Procesando Inducción...</h2>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(2.5)
    
    # Simulación matemática
    B_si = B_user if sistema == "Métrico (T, μS/cm, m)" else B_user / 10000.0
    D_si = D_user if sistema == "Métrico (T, μS/cm, m)" else D_user * 0.0254
    sigma_si = sigma_user if sistema == "Métrico (T, μS/cm, m)" else sigma_user / 2.54

    v = np.linspace(0.1, 5.0, 100)
    V_mv = (B_si * D_si * v * 1000)
    Q_plot = (np.pi * (D_si / 2)**2 * v) * conv_q
    m_eq = V_mv[-1] / Q_plot[-1]

    # Gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown(f"""
        <div class="equation-box">
            <h2 style="color:#00d4ff; font-size: 2.2rem; margin:0;">V = {m_eq:.4f} · Q</h2>
        </div>
    """, unsafe_allow_html=True)

st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
st.markdown('</div>', unsafe_allow_html=True) # CIERRE DE LA ISLA
