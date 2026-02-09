import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS Maestro: Franja Negra Infinita y Persistente (DISEÑO INTACTO)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

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

    /* Desenfoque sutil solicitado */
    .stApp {
        backdrop-filter: blur(4px);
    }

    .stApp, [data-testid="stHeader"], .block-container {
        background: transparent !important;
    }

    .block-container {
        font-family: 'Roboto', sans-serif;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 4rem 2rem !important;
        color: white !important;
    }

    h1 { font-size: 3rem !important; font-weight: 700 !important; text-align: left !important; }
    h3 { font-size: 1.6rem !important; text-align: left !important; font-weight: 300 !important; }

    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; border: 2px solid white !important; }

    .stButton > button {
        width: 100%;
        background-color: #00d4ff;
        color: white;
        border-radius: 8px;
        padding: 1rem;
        font-size: 1.4rem;
        font-weight: bold;
        border: none;
    }

    /* Cero naranja en inputs */
    input[type="number"]:focus { border-color: #00d4ff !important; box-shadow: 0 0 0 1px #00d4ff !important; }

    p, label, .stMarkdown { font-size: 1.1rem !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE UNIDADES ---
st.title('Simulación de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')

# Selector de unidades (Unico cambio funcional)
sistema = st.radio("Sistema de Unidades:", ("Métrico (m, m³/s)", "Americano (in, GPM)"), horizontal=True)

if sistema == "Métrico (m, m³/s)":
    u_d, u_q = "m", "m³/s"
    d_min, d_max, d_def = 0.005, 0.500, 0.0127
    conv_q = 1.0  # Ya está en SI
else:
    u_d, u_q = "in", "GPM"
    d_min, d_max, d_def = 0.2, 20.0, 0.5
    conv_q = 15850.3  # 1 m3/s = 15850.3 GPM

st.write("---")

# --- CONTENIDO ---
st.markdown(f"#### Parámetros de Configuración ({u_d})")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B_val = st.number_input('B: Campo Magnético (T)', 0.1, 1.5, 0.5, 0.1)
    B = st.slider('Ajustar B', 0.1, 1.5, float(B_val), 0.01, label_visibility="collapsed")

with col2:
    sigma_val = st.number_input('σ: Conductividad (μS/cm)', 1, 5000, 1000, 100)
    sigma = st.slider('Ajustar σ', 1, 5000, int(sigma_val), 10, label_visibility="collapsed")

with col3:
    D_val = st.number_input(f'D: Diámetro ({u_d})', d_min, d_max, d_def, format="%.4f")
    D = st.slider(f'Ajustar D', d_min, d_max, float(D_val), 0.0001, label_visibility="collapsed")

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
    if not st.session_state.edit_error: st.write(f"Factor por defecto: **{error_factor}**")

if st.button('🚀 Generar curva de calibración'):
    # Física interna siempre en SI para evitar errores
    D_m = D if u_d == "m" else D * 0.0254
    A_m2 = np.pi * (D_m / 2)**2
    v = np.linspace(0.1, 5.0, 100) # velocidad m/s
    
    # Efecto de conductividad
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma - 5)))
    
    # Cálculo de Voltaje (mV)
    V_mv = (B * D_m * v * f_cond * 1000) * error_factor
    
    # Caudal para el eje X según unidad elegida
    Q_final = (A_m2 * v) * conv_q
    
    # Pendiente (m) de la ecuación V = m * Q
    m_eq = V_mv[-1] / Q_final[-1]

    

    # Gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q_final, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.latex(rf"V_{{(mV)}} = {m_eq:.4f} \cdot Q_{{({u_q})}}")

st.write("---")
st.caption("Adriana Teixeira Mendoza 2026")
