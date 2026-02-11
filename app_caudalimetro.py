import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana", initial_sidebar_state="expanded")

# ENLACE RAW
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS MAESTRO: Sidebar Flotante y Centro Fijo
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

    /* --- CAPA CENTRAL NEGRA (Fondo del Simulador) --- */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 50%; transform: translateX(-50%);
        width: 100%; max-width: 1200px; height: 100vh;
        background: rgba(0, 0, 0, 0.7); 
        backdrop-filter: blur(5px); 
        z-index: 0;
    }

    /* --- FORZAR CONTENIDO SIEMPRE AL CENTRO (No se mueve con el sidebar) --- */
    [data-testid="stMain"] {
        align-items: center !important;
    }

    [data-testid="stAppViewBlockContainer"] {
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding-top: 130px !important;
        z-index: 1;
    }

    /* --- TRUCO MAESTRO: SIDEBAR OVERLAY (Flota sobre el contenido) --- */
    [data-testid="stSidebar"] {
        position: fixed !important;
        background-color: rgba(0, 0, 0, 0.95) !important;
        border-right: 2px solid #00d4ff !important;
        z-index: 10000 !important;
        width: 350px !important;
    }

    /* Evita que el sidebar "empuje" al contenido principal */
    [data-testid="stSidebar"][aria-expanded="true"] + section {
        margin-left: 0 !important;
    }

    /* --- BOTÓN DE LA BARRA LATERAL --- */
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

    /* --- HEADER FIJO --- */
    .fixed-header {
        position: fixed; top: 0; left: 0; width: 100vw;
        z-index: 999; display: flex; justify-content: center;
        pointer-events: none;
    }
    .header-content {
        pointer-events: auto;
        width: 100%; max-width: 1200px;
        background: rgba(0,0,0,0.9);
        padding: 15px; text-align: center;
        border-bottom: 2px solid #00d4ff;
        border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;
    }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* --- ESTILOS NEÓN Y TEXTOS --- */
    p, label, .stMarkdown, h1, h2, h3 { color: white !important; font-family: 'Roboto'; }
    
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child { border: 2px solid #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; }
    
    .stButton > button {
        width: 100%; background-color: #1a5276 !important; color: white !important;
        border: 1px solid #00d4ff !important; border-radius: 8px;
    }

    /* Pantalla de Carga */
    .loading-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.9); z-index: 99999;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }

    .equation-box {
        background: rgba(0, 212, 255, 0.1); border: 2px solid #00d4ff;
        border-radius: 15px; padding: 25px; text-align: center; margin-top: 20px;
    }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1 style="margin:0; font-size: 1.8rem; color: #00d4ff;">Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE UNIDADES ---
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

# --- SIDEBAR (CONTENIDO) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>📋 Referencias σ</h2>", unsafe_allow_html=True)
    fluidos = {
        "Agua Destilada": 0.5, "Agua Potable": 500, "Agua de Mar": 50000,
        "Leche": 5000, "Zumo de Frutas": 3000, "Ácido Sulfúrico": 700000
    }
    if sistema == "Métrico (T, μS/cm, m)":
        tabla = {f: f"{v:,} μS/cm" for f, v in fluidos.items()}
    else:
        tabla = {f: f"{v * 2.54:,} μmhos/in" for f, v in fluidos.items()}
    st.table(list(tabla.items()))

# --- PARÁMETROS (DISEÑO VERTICAL) ---
st.write("---")
st.markdown(f"### Parámetros de Simulación ({sistema})")

# Los inputs ahora están uno debajo del otro, centrados en el fondo negro
B_val = st.number_input(f'Campo Magnético (B)', value=0.5 if "Métrico" in sistema else 5000.0)
B_user = st.slider('Ajustar B', 0.1, 15000.0, float(B_val), label_visibility="collapsed")

sig_val = st.number_input(f'Conductividad (σ)', value=1000.0 if "Métrico" in sistema else 2540.0)
sigma_user = st.slider('Ajustar σ', 1.0, 700000.0, float(sig_val), label_visibility="collapsed")

D_val = st.number_input(f'Diámetro del Tubo (D)', value=0.0127 if "Métrico" in sistema else 0.5, format="%.4f")
D_user = st.slider('Ajustar D', 0.005, 20.0, float(D_val), label_visibility="collapsed")

st.write("---")

# --- CÁLCULOS Y ACCIÓN ---
if st.button('🚀 GENERAR CURVA DE CALIBRACIÓN'):
    # Overlay de carga
    loading_placeholder = st.empty()
    with loading_placeholder:
        st.markdown(f"""
            <div class="loading-overlay">
                <img src="{URL_GIF}" width="400">
                <h2 style="color: #00d4ff;">Analizando Inducción Magnética...</h2>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    loading_placeholder.empty()

    # Cálculos SI
    if "Americano" in sistema:
        B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
        u_q = "GPM"
        conv_q = 15850.3
    else:
        B_si, D_si, sigma_si = B_user, D_user, sigma_user
        u_q = "m³/s"
        conv_q = 1.0

    v = np.linspace(0.1, 5.0, 100)
    V_mv = (B_si * D_si * v * 1000)
    Q_plot = (np.pi * (D_si / 2)**2 * v) * conv_q
    m_eq = V_mv[-1] / Q_plot[-1]

    # Gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f"Caudal Q ({u_q})")
    ax.set_ylabel("Voltaje V (mV)")
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown(f"""
        <div class="equation-box">
            <h2 style="color:#00d4ff; margin:0; font-size: 2.2rem;">V = {m_eq:.4f} · Q</h2>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
