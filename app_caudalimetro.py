import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS Maestro: Encabezado FIJO y Contenido DESLIZABLE
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de imagen base FIJO */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* RECUADRO FIJO PARA EL TÍTULO */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    .fixed-header {
        position: fixed;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 1100px;
        background-color: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        padding: 1.5rem 2rem;
        z-index: 1000;
        border-bottom: 2px solid #00d4ff;
    }

    /* ESPACIADOR para que el contenido no empiece debajo del header fijo */
    .header-spacer {
        height: 180px;
    }

    /* FRANJA NEGRA CENTRAL PARA EL CONTENIDO */
    .block-container {
        background-image: linear-gradient(
            rgba(0, 0, 0, 0.5), 
            rgba(0, 0, 0, 0.5)
        ) !important;
        backdrop-filter: blur(4px);
        max-width: 1100px !important;
        margin: auto !important;
        padding-top: 0rem !important;
        color: white !important;
        min-height: 100vh;
    }

    /* Ajustes de Texto */
    h1 { font-family: 'Roboto'; font-weight: 700; color: white; margin: 0; font-size: 2.5rem !important; }
    h3 { font-family: 'Roboto'; font-weight: 300; color: #00d4ff; margin: 0; font-size: 1.2rem !important; }

    /* Estética de Sliders y Botones */
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; border: 2px solid white !important; }
    
    .stButton > button {
        width: 100%;
        background-color: #00d4ff;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.8rem;
    }

    p, label, .stMarkdown { color: white !important; }
    </style>
    
    <div class="fixed-header">
        <h1>Simulación de Caudalímetro Electromagnético</h1>
        <h3>Por: Adriana Teixeira Mendoza</h3>
    </div>
    <div class="header-spacer"></div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE UNIDADES ---
sistema = st.radio("Sistema de Unidades Global:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

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
    B_user = st.slider(f'Ajustar B', float(b_min), float(b_max), float(B_val), label_visibility="collapsed")

with col2:
    sig_val = st.number_input(f'σ: Conductividad ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
    sigma_user = st.slider(f'Ajustar σ', float(sig_min), float(sig_max), float(sig_val), label_visibility="collapsed")

with col3:
    D_val = st.number_input(f'D: Diámetro ({u_d})', float(d_min), float(d_max), float(d_def), format="%.4f")
    D_user = st.slider(f'Ajustar D', float(d_min), float(d_max), float(D_val), label_visibility="collapsed")

st.write("---")

# Error
if 'edit_error' not in st.session_state: st.session_state.edit_error = False
c_err1, c_err2 = st.columns([3, 1])
with c_err2:
    if st.button('🔄 Cambiar Factor'): st.session_state.edit_error = not st.session_state.edit_error
with c_err1:
    error_factor = st.slider('Error', 0.80, 1.20, 1.00, 0.01) if st.session_state.edit_error else 1.00

# --- CÁLCULOS ---
if sistema == "Americano (G, mhos/in, in)":
    B_si = B_user / 10000.0
    D_si = D_user * 0.0254
    sigma_si = sigma_user / 2.54
else:
    B_si, D_si, sigma_si = B_user, D_user, sigma_user

if st.button('🚀 Generar curva de calibración'):
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

    st.latex(rf"V_{{(mV)}} = {m_eq:.4f} \cdot Q_{{({u_q})}}")

st.write("---")
st.caption("Adriana Teixeira Mendoza 2026")
