import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS Maestro: Franja Negra Infinita y Persistente
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* 1. Fondo de imagen FIJO y la FRANJA NEGRA INFINITA pintada en el fondo */
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

    /* 2. Hacemos que todo lo demás sea totalmente transparente para que se vea el fondo de arriba */
    .stApp, [data-testid="stHeader"], .block-container {
        background: transparent !important;
    }

    /* 3. Ajuste de contenido */
    .block-container {
        font-family: 'Roboto', sans-serif;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 4rem 2rem !important;
        color: white !important;
    }

    /* TÍTULO A LA IZQUIERDA */
    h1 { 
        font-size: 3rem !important; 
        font-weight: 700 !important; 
        text-align: left !important; 
    }
    h3 { 
        font-size: 1.6rem !important; 
        text-align: left !important; 
        font-weight: 300 !important;
    }

    /* SLIDERS AZULES (#00D4FF) */
    div[data-testid="stSlider"] > div > div > div > div {
        background-color: #00d4ff !important;
    }
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #00d4ff !important;
        border: 2px solid white !important;
    }

    /* BOTÓN AZUL */
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

    p, label, .stMarkdown { font-size: 1.1rem !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---

st.title('Simulación de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")



st.markdown("#### Configuración de Parámetros")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B_val = st.number_input('B: Campo Magnético (T)', 0.1, 1.0, 0.5, 0.1)
    B = st.slider('Ajustar B', 0.1, 1.0, float(B_val), 0.01, label_visibility="collapsed")

with col2:
    sigma_val = st.number_input('σ: Conductividad (μS/cm)', 1, 5000, 1000, 100)
    sigma = st.slider('Ajustar σ', 1, 5000, int(sigma_val), 10, label_visibility="collapsed")

with col3:
    D_val = st.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")
    D = st.slider('Ajustar D', 0.005, 0.050, float(D_val), 0.0001, label_visibility="collapsed")

st.write("---")

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
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma - 5)))
    V_mv = (B * D * v * f_cond * 1000) * error_factor
    m = ((B * D * f_cond * 1000) / A) * error_factor

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(v*A, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel('Caudal Q (m³/s)')
    ax.set_ylabel('Voltaje V (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}}")

st.write("---")
st.caption("Adriana Teixeira 2026")
