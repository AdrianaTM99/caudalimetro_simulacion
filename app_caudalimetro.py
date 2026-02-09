import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS Maestro: Título FIJO, Fondo de Agua y Franja Negra Deslizable
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

    /* RECUADRO FIJO PARA EL TÍTULO (CONGELADO ARRIBA) */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 1100px;
        background-color: rgba(0, 0, 0, 0.85); /* Un poco más oscuro para legibilidad */
        backdrop-filter: blur(12px);
        padding: 20px 40px;
        z-index: 9999;
        border-bottom: 3px solid #00d4ff;
        border-radius: 0 0 15px 15px;
        text-align: left;
    }

    /* TÍTULOS DENTRO DEL HEADER */
    .fixed-header h1 { 
        margin: 0; 
        font-size: 2.2rem !important; 
        color: white !important;
        font-family: 'Roboto', sans-serif;
    }
    .fixed-header h3 { 
        margin: 0; 
        font-size: 1.1rem !important; 
        color: #00d4ff !important;
        font-weight: 300;
        font-family: 'Roboto', sans-serif;
    }

    /* CONTENEDOR DE CONTENIDO (CON FRANJA NEGRA) */
    .block-container {
        background-color: rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(4px);
        max-width: 1100px !important;
        margin: auto !important;
        padding-top: 160px !important; /* Espacio para que el header no tape el inicio */
        min-height: 100vh;
        color: white !important;
    }

    /* Ocultar elementos nativos de Streamlit que ensucian la vista */
    header[data-testid="stHeader"] { visibility: hidden; }
    
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
        font-size: 1.2rem;
    }

    p, label, .stMarkdown { color: white !important; }
    </style>

    <div class="fixed-header">
        <h1>Simulación de Caudalímetro Electromagnético</h1>
        <h3>Por: Adriana Teixeira Mendoza</h3>
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE UNIDADES ---
# Colocamos el selector de unidades justo al inicio del área deslizable
sistema = st.radio("Selecciona el Sistema de Unidades de Trabajo:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

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
st.markdown(f"#### ⚙️ Parámetros del Sensor ({u_d})")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B_val = st.number_input(f'Campo Magnético ({u_b})', float(b_min), float(b_max), float(b_def))
    B_user = st.slider(f'B slider', float(b_min), float(b_max), float(B_val), label_visibility="collapsed")

with col2:
    sig_val = st.number_input(f'Conductividad ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
    sigma_user = st.slider(f'σ slider', float(sig_min), float(sig_max), float(sig_val), label_visibility="collapsed")

with col3:
    D_val = st.number_input(f'Diámetro del Tubo ({u_d})', float(d_min), float(d_max), float(d_def), format="%.4f")
    D_user = st.slider(f'D slider', float(d_min), float(d_max), float(D_val), label_visibility="collapsed")

# --- AJUSTE DE ERROR ---
st.write("---")
if 'edit_error' not in st.session_state: st.session_state.edit_error = False
err_col1, err_col2 = st.columns([3, 1])
with err_col2:
    if st.button('🔧 Ajustar Error'): st.session_state.edit_error = not st.session_state.edit_error
with err_col1:
    error_factor = st.slider('Factor de Corrección', 0.80, 1.20, 1.00, 0.01) if st.session_state.edit_error else 1.00

# --- CÁLCULOS ---
if sistema == "Americano (G, mhos/in, in)":
    B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
else:
    B_si, D_si, sigma_si = B_user, D_user, sigma_user

if st.button('🚀 GENERAR ANÁLISIS COMPLETO'):
    A_m2 = np.pi * (D_si / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
    V_mv = (B_si * D_si * v * f_cond * 1000) * error_factor
    Q_plot = (A_m2 * v) * conv_q
    m_eq = V_mv[-1] / Q_plot[-1]

    

    # Gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=4, shadow=True)
    ax.set_xlabel(f'Caudal Q ({u_q})', fontsize=12, color='#00d4ff')
    ax.set_ylabel('Voltaje Inducido V (mV)', fontsize=12, color='#00d4ff')
    ax.grid(True, alpha=0.15)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown("#### 📐 Ecuación de Calibración Generada:")
    st.latex(rf"V_{{(mV)}} = {m_eq:.4f} \cdot Q_{{({u_q})}}")

    st.write("---")
    
    # --- CALCULADORA AUTOMÁTICA ---
    st.markdown(f"#### 💡 Calculadora de Predicción ({u_q} ↔ mV)")
    c_calc1, c_calc2 = st.columns(2)
    with c_calc1:
        q_in = st.number_input(f"Ingresa Caudal en {u_q}:", value=0.0)
        st.success(f"Voltaje Estimado: **{(q_in * m_eq):.4f} mV**")
    with c_calc2:
        v_in = st.number_input(f"Ingresa Voltaje en mV:", value=0.0)
        q_res = (v_in / m_eq) if m_eq != 0 else 0
        st.info(f"Caudal Estimado: **{q_res:.4f} {u_q}**")

st.write("---")
st.caption("Simulador de Ingeniería | Adriana Teixeira Mendoza 2026")
