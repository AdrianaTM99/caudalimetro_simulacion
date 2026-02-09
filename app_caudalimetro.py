import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS Maestro (Diseño unificado: Título fijo, botones opacos, radio buttons personalizados)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de imagen base FIJO con franja central sombreada */
    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(
                to right, 
                transparent 0%, 
                transparent calc(50% - 550px), 
                rgba(0, 0, 0, 0.5) calc(50% - 550px), 
                rgba(0, 0, 0, 0.5) calc(50% + 550px), 
                transparent calc(50% + 550px), 
                transparent 100%
            ),
            url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* RECUADRO FIJO DEL TÍTULO (Extremo a Extremo) */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        background-color: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(4px);
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

    .block-container {
        font-family: 'Roboto', sans-serif;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 100px 2rem 4rem 2rem !important;
        color: white !important;
    }

    .fixed-header h1 { font-size: 1.8rem !important; font-weight: 700 !important; margin: 0; color: white; }
    .fixed-header h3 { font-size: 1.1rem !important; font-weight: 300 !important; margin: 0; color: white; }

    /* INDICADORES DE SELECCIÓN (RADIO BUTTONS) - AZUL Y NEGRO */
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
        border: 2px solid #00d4ff !important;
        background-color: #000000 !important;
        width: 20px !important;
        height: 20px !important;
    }
    div[data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] > div:first-child > div {
        background-color: #00d4ff !important;
        width: 100% !important;
        height: 100% !important;
        border: 2px solid black !important;
    }

    /* SLIDERS (Azul cian para resaltar) */
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; border: 2px solid white !important; }

    /* BOTONES (Azul cobalto opaco) */
    .stButton > button {
        width: 100%;
        background-color: #1a5276 !important;
        color: white !important;
        border-radius: 8px;
        padding: 0.8rem;
        font-size: 1.2rem;
        font-weight: bold;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #21618c !important;
        border-color: #00d4ff !important;
    }

    /* RESULTADOS CALCULADORA */
    .stSuccess, .stInfo {
        background-color: rgba(26, 82, 118, 0.5) !important;
        color: white !important;
        border: 1px solid #00d4ff !important;
    }

    p, label, .stMarkdown { font-size: 1.1rem !important; color: white !important; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
            <h3>Por: Adriana Teixeira Mendoza</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE UNIDADES ---
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

# --- 4. PARÁMETROS DINÁMICOS ---
st.markdown(f"#### Configuración de Parámetros ({sistema})")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B_val = st.number_input(f'B: Campo Magnético ({u_b})', float(b_min), float(b_max), float(b_def))
    B_user = st.slider(f'B_slider', float(b_min), float(b_max), float(B_val), label_visibility="collapsed")

with col2:
    sig_val = st.number_input(f'σ: Conductividad ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
    sigma_user = st.slider(f'Sig_slider', float(sig_min), float(sig_max), float(sig_val), label_visibility="collapsed")

with col3:
    D_val = st.number_input(f'D: Diámetro ({u_d})', float(d_min), float(d_max), float(d_def), format="%.4f")
    D_user = st.slider(f'D_slider', float(d_min), float(d_max), float(D_val), label_visibility="collapsed")

st.write("---")

# Factor de Error
if 'edit_error' not in st.session_state:
    st.session_state.edit_error = False

st.markdown("#### Factor de Error del Sistema")
c_err1, c_err2 = st.columns([3, 1])
with c_err2:
    if st.button('🔄 Cambiar Factor'):
        st.session_state.edit_error = not st.session_state.edit_error
with c_err1:
    error_factor = st.slider('Error', 0.80, 1.20, 1.00, 0.01) if st.session_state.edit_error else 1.00

# --- 5. CÁLCULOS Y GRÁFICA ---
if sistema == "Americano (G, mhos/in, in)":
    B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
else:
    B_si, D_si, sigma_si = B_user, D_user, sigma_user

A_m2 = np.pi * (D_si / 2)**2
f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
m_eq = (B_si * D_si * f_cond * 1000 * error_factor) / (A_m2 * conv_q)

if st.button('🚀 Generar curva de calibración'):
    v_range = np.linspace(0.1, 5.0, 100)
    V_mv = (B_si * D_si * v_range * f_cond * 1000) * error_factor
    Q_plot = (A_m2 * v_range) * conv_q

    

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.latex(rf"V_{{(mV)}} = {m_eq:.4f} \cdot Q_{{({u_q})}}")

st.write("---")

# --- 6. CALCULADORA DE VALORES ---
st.markdown(f"#### 🧮 Calculadora de Predicción ({u_q} ↔ mV)")
st.write("Calcula resultados basados en la configuración de parámetros de arriba:")

calc_col1, calc_col2 = st.columns(2)

with calc_col1:
    q_input = st.number_input(f"Si el Caudal (Q) es:", value=0.0, step=0.1, format="%.2f")
    v_res = q_input * m_eq
    st.success(f"El Voltaje inducido será: **{v_res:.4f} mV**")

with calc_col2:
    v_input = st.number_input(f"Si el Voltaje (V) es (mV):", value=0.0, step=0.1, format="%.2f")
    q_res = v_input / m_eq if m_eq != 0 else 0
    st.info(f"El Caudal estimado es: **{q_res:.4f} {u_q}**")

st.write("---")
st.caption("Adriana Teixeira Mendoza 2026")
