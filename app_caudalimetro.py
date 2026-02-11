import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="Simulador Adriana",
    initial_sidebar_state="collapsed"
)

# ENLACE RAW CORREGIDO
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# =====================================================
# 🔹 SIDEBAR FIJA QUE NO DESPLAZA CONTENIDO
# =====================================================
st.markdown("""
<style>

section[data-testid="stSidebar"] {
    position: fixed !important;
    left: 0;
    top: 0;
    height: 100vh;
    width: 330px !important;
    background: rgba(0,0,0,0.97) !important;
    backdrop-filter: blur(10px);
    border-right: 2px solid #00d4ff;
    z-index: 800;
}

div[data-testid="collapsedControl"] {
    z-index: 2000 !important;
}

[data-testid="stAppViewContainer"] {
    margin-left: 0 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# CONTENIDO DE LA SIDEBAR
# =========================
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

    with st.expander("🧲 Campos Magnéticos Recomendados", expanded=True):
        st.markdown("""
        | Campo (T) | Aplicación |
        |------------|------------|
        | 0.1 – 0.3 T | Alta conductividad |
        | 0.3 – 0.6 T | Uso industrial estándar |
        | 0.6 – 1.0 T | Baja conductividad |
        | 1.0 – 1.5 T | Aplicaciones especiales |
        """)

    with st.expander("🌊 Velocidades Recomendadas", expanded=True):
        st.markdown("""
        | Aplicación | Velocidad Recomendada |
        |-------------|----------------------|
        | Agua potable | 1 – 3 m/s |
        | Industria química | 1 – 5 m/s |
        | Lodos | 0.5 – 2 m/s |
        | Alimentos | 1 – 4 m/s |
        """)

# =====================================================
# INTERFAZ ORIGINAL (SOLO HEADER CORREGIDO)
# =====================================================

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

    .equation-large {
        font-size: 3rem !important;
        color: #00d4ff;
        font-weight: 700;
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

    /* 🔥 SOLO CAMBIO AQUÍ */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 1100px;
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
        justify-content: center;
        align-items: center;
    }

    header[data-testid="stHeader"] { visibility: visible; }
    .stApp { background: transparent !important; }

    .fixed-header h1 { 
        font-size: 1.8rem !important; 
        font-weight: 700 !important; 
        margin: 0; 
        color: white; 
    }

    p, label, .stMarkdown { font-size: 1.1rem !important; color: white !important; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- LÓGICA DE UNIDADES ---
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

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

if 'edit_error' not in st.session_state:
    st.session_state.edit_error = False

st.markdown("#### Factor de Error del Sistema")
c_err1, c_err2 = st.columns([1, 3]) 

with c_err1:
    if st.button('🔄 Cambiar Factor'):
        st.session_state.edit_error = not st.session_state.edit_error

with c_err2:
    error_factor = st.slider('Error', 0.80, 1.20, 1.00, 0.01) if st.session_state.edit_error else 1.00

# --- CÁLCULOS ---
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
                <p style="color:#00d4ff; font-weight:bold; margin-top:10px; font-size:1.2rem;">
                Calculando flujo electromagnético...
                </p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)

    placeholder.empty()

    A_m2 = np.pi * (D_si / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
    V_mv = (B_si * D_si * v * f_cond * 1000) * error_factor
    Q_plot = (A_m2 * v) * conv_q
    m_eq = V_mv[-1] / Q_plot[-1]

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
            <div class="equation-large">
                V<sub>(mV)</sub> = {m_eq:.4f} · Q<sub>({u_q})</sub>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")


