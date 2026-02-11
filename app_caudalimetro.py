import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# ENLACE RAW CORREGIDO
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS Maestro con corrección para el botón del Sidebar
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

    /* BOTÓN DEL SIDEBAR (FLECHA): Forzar visibilidad y color */
    [data-testid="stSidebarCollapseButton"] {
        background-color: rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
        border-radius: 50% !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 10000;
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

    /* Estilo para el Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid #00d4ff;
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

    .equation-box {
        background: rgba(0, 0, 0, 0.5);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 30px;
        margin: 20px auto;
        text-align: center;
        box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.3);
    }

    .loading-overlay {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        text-align: center;
        background: rgba(0, 0, 0, 0.95);
        padding: 20px;
        border-radius: 25px;
        border: 2px solid #00d4ff;
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

    header[data-testid="stHeader"] { visibility: hidden; }
    .stApp { background: transparent !important; }

    .fixed-header h1 { font-size: 1.8rem !important; font-weight: 700 !important; margin: 0; color: white; }

    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
        border: 2px solid #00d4ff !important;
        background-color: #000000 !important;
    }
    div[data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] > div:first-child > div {
        background-color: #00d4ff !important;
    }

    .stButton > button {
        width: 100%;
        background-color: #1a5276 !important;
        color: white !important;
        font-weight: bold;
    }

    p, label, .stMarkdown { font-size: 1.1rem !important; color: white !important; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR: LISTA DE CONDUCTIVIDADES ---
with st.sidebar:
    st.markdown("### 📋 Referencia de Fluidos")
    st.write("Conductividades típicas para configurar el parámetro σ.")
    
    fluidos = {
        "Agua Destilada": 0.5,
        "Agua Potable": 500,
        "Agua de Mar": 50000,
        "Leche": 5000,
        "Zumo de Frutas": 3000,
        "Ácido Sulfúrico (30%)": 700000
    }

# --- LÓGICA DE UNIDADES ---
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

with st.sidebar:
    if sistema == "Métrico (T, μS/cm, m)":
        unit_label = "μS/cm"
        tabla_data = {f: f"{v:,} {unit_label}" for f, v in fluidos.items()}
    else:
        unit_label = "μmhos/in"
        tabla_data = {f: f"{v * 2.54:,} {unit_label}" for f, v in fluidos.items()}
    
    st.table(list(tabla_data.items()))
    st.info("Puedes cerrar esta barra con la flecha de arriba.")

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

# --- PARÁMETROS ---
st.markdown(f"#### Configuración de Parámetros ({sistema})")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B_val = st.number_input(f'B: Campo Magnético ({u_b})', float(b_min), float(b_max), float(b_def))
    B_user = st.slider(f'Ajustar B', float(b_min), float(b_max), float(B_val), key="B_slider", label_visibility="collapsed")
with col2:
    sig_val = st.number_input(f'σ: Conductividad ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
    sigma_user = st.slider(f'Ajustar σ', float(sig_min), float(sig_max), float(sig_val), key="sig_slider", label_visibility="collapsed")
with col3:
    D_val = st.number_input(f'D: Diámetro ({u_d})', float(d_min), float(d_max), float(d_def), format="%.4f")
    D_user = st.slider(f'Ajustar D', float(d_min), float(d_max), float(D_val), key="D_slider", label_visibility="collapsed")

st.write("---")

# --- BOTÓN DE CÁLCULO ---
if st.button('🚀 Generar curva de calibración'):
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
            <div class="loading-overlay">
                <img src="{URL_GIF}" width="360">
                <p style="color:#00d4ff; font-weight:bold; margin-top:10px; font-size:1.2rem;">Procesando simulación...</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    placeholder.empty()

    # Cálculos simplificados para la curva
    A_m2 = np.pi * (D_si / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
    V_mv = (B_si * D_si * v * f_cond * 1000)
    Q_plot = (A_m2 * v) * conv_q
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
