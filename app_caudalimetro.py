import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# =====================================================
# CONFIGURACIÓN
# =====================================================
st.set_page_config(
    layout="wide",
    page_title="Simulador Adriana",
    initial_sidebar_state="collapsed"
)

URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# =====================================================
# ESTILOS GLOBALES + BOTÓN SIEMPRE VISIBLE
# =====================================================
st.markdown("""
<style>

/* ============================= */
/* SIDEBAR FIJA */
/* ============================= */
section[data-testid="stSidebar"] {
    position: fixed !important;
    left: 0;
    top: 0;
    height: 100vh;
    width: 330px !important;
    background: rgba(0,0,0,0.97) !important;
    backdrop-filter: blur(10px);
    border-right: 2px solid #00d4ff;
    z-index: 1000;
}

/* ============================= */
/* BOTÓN ☰ SIEMPRE VISIBLE */
/* ============================= */
button[kind="header"] {
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 5000 !important;
    background-color: rgba(0,0,0,0.8) !important;
    border: 1px solid #00d4ff !important;
    border-radius: 8px !important;
}

/* Hover azul */
button[kind="header"]:hover {
    background-color: #001f2e !important;
}

/* No ocultar header */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Evita desplazamiento */
[data-testid="stAppViewContainer"] {
    margin-left: 0 !important;
}

/* ============================= */
/* FONDO PRINCIPAL */
/* ============================= */
[data-testid="stAppViewContainer"] {
    background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Capa oscura centrada */
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

/* Contenedor principal */
.block-container {
    position: relative;
    z-index: 1;
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding: 100px 2rem 4rem 2rem !important;
    color: white !important;
}

/* ============================= */
/* HEADER CENTRADO */
/* ============================= */
.fixed-header {
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 1100px;
    background-color: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(10px);
    z-index: 2000;
    display: flex;
    justify-content: center;
    border-bottom: 1px solid rgba(0, 212, 255, 0.4);
}

.header-content {
    width: 100%;
    padding: 12px 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
}

.fixed-header h1 {
    font-size: 1.9rem;
    font-weight: 700;
    color: #00d4ff;
    margin: 0;
}

/* ============================= */
/* CAJAS Y ECUACIÓN */
/* ============================= */
.equation-box {
    background: rgba(0, 0, 0, 0.5);
    border: 2px solid #00d4ff;
    border-radius: 15px;
    padding: 30px;
    margin: 20px auto;
    text-align: center;
    box-shadow: 0px 0px 20px rgba(0, 212, 255, 0.3);
}

.equation-large {
    font-size: 3rem;
    color: #00d4ff;
    font-weight: 700;
}

/* Loading */
.loading-overlay {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999;
    text-align: center;
    background: rgba(0, 0, 0, 0.95);
    padding: 25px;
    border-radius: 25px;
    border: 2px solid #00d4ff;
}

</style>

<div class="fixed-header">
    <div class="header-content">
        <h1>Simulación de Caudalímetro Electromagnético</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
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

# =====================================================
# RESTO DEL SIMULADOR (IGUAL)
# =====================================================
sistema = st.radio(
    "Selecciona el Sistema de Unidades:",
    ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"),
    horizontal=True
)

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
