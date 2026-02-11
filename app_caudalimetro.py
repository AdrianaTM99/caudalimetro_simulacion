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
        margin-left: auto !important;
        margin-right: auto !important;
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

# --- 3. LÓGICA DE UNIDADES ---
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>📋 Conductividades (σ)</h2>", unsafe_allow_html=True)
    fluidos = {
        "Agua Destilada": 0.5, "Agua Potable": 500, "Agua de Mar": 50000,
        "Leche": 5000, "Zumo de Frutas": 3000, "Ácido Sulfúrico": 700000
    }
    if sistema == "Métrico (T, μS/cm, m)":
        u_label = "μS/cm"
        tabla = {f: f"{v:,} {u_label}" for f, v in fluidos.items()}
    else:
        u_label = "μmhos/in"
        tabla = {f: f"{v * 2.54:,} {u_label}" for f, v in fluidos.items()}
    st.table(list(tabla.items()))
    st.write("---")
    st.info("💡 Haz clic en la flecha azul (esquina superior izquierda) para cerrar este panel.")

st.write("---")

# --- VARIABLES Y PARÁMETROS ---
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

# --- CÁLCULOS Y GRÁFICA ---
if sistema == "Americano (G, mhos/in, in)":
    B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
else:
    B_si, D_si, sigma_si = B_user, D_user, sigma_user

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

    A_m2 = np.pi * (D_si / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
    V_mv = (B_si * D_si * v * f_cond * 1000)
    Q_plot = (A_m2 * v) * conv_q
    m_eq = V_mv[-1] / Q_plot[-1] if Q_plot[-1] != 0 else 0

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown(f"""
        <div class="equation-box">
            <h2 style="color:#00d4ff; font-size: 2.5rem; margin:0;">V = {m_eq:.4f} · Q</h2>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
