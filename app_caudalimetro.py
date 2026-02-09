import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS: Azul Bonito (#00D4FF) + Franja Persistente
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de mar fijo */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Fondo transparente para los elementos de Streamlit */
    [data-testid="stHeader"], .stApp {
        background: rgba(0,0,0,0);
    }

    /* FRANJA NEGRA PERSISTENTE: 50% transparencia y 5px de desenfoque */
    .main .block-container {
        font-family: 'Roboto', sans-serif;
        background-color: rgba(0, 0, 0, 0.5) !important; 
        padding: 4rem !important;
        max-width: 1100px; 
        min-height: 100vh;
        height: auto; /* IMPORTANTE: Hace que el fondo crezca con el contenido */
        margin: 0 auto;
        color: white !important;
        backdrop-filter: blur(5px);
    }

    /* --- EL AZUL BONITO (#00D4FF) EN LOS SLIDERS --- */
    /* Color de la barra activa */
    div[data-testid="stSlider"] > div > div > div > div {
        background-color: #00D4FF !important;
    }
    /* Color del círculo deslizable */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #00D4FF !important;
        border: 2px solid white !important;
    }

    /* Botón Principal con el mismo Azul */
    .stButton > button {
        width: 100%;
        background-color: #00D4FF;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 1rem;
        font-size: 1.4rem;
        font-weight: bold;
        transition: 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #00A8CC; /* Un azul un poco más oscuro al pasar el mouse */
        transform: scale(1.01);
    }

    /* Texto blanco nítido */
    h1, h3, h4, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---

st.title('Simulación de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")

st.markdown("#### Ajuste de Parámetros")

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

# Factor de Error con botón de habilitación
if 'edit_error' not in st.session_state:
    st.session_state.edit_error = False

c_err1, c_err2 = st.columns([3, 1])
with c_err2:
    if st.button('🔄 Cambiar Error'):
        st.session_state.edit_error = not st.session_state.edit_error

with c_err1:
    if st.session_state.edit_error:
        error_factor = st.slider('Modificar Factor de Error', 0.80, 1.20, 1.00, 0.01)
    else:
        error_factor = 1.00
        st.write(f"Factor por defecto: **{error_factor}**")

# Lógica
def conductivity_factor(s):
    return 1 / (1 + np.exp(-0.01 * (s - 5)))

if st.button('🚀 Generar curva de calibración'):
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    Q = A * v
    f_c = conductivity_factor(sigma)
    V_mv = (B * D * v * f_c * 1000) * error_factor
    m = ((B * D * f_c * 1000) / A) * error_factor

    # Gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q, V_mv, color='#00D4FF', linewidth=3) # Usando el azul bonito
    ax.set_xlabel('Caudal Q (m³/s)')
    ax.set_ylabel('Voltaje V (mV)')
    ax.grid(True, alpha=0.1)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown("#### Resultado:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}}")

st.write("---")
st.caption("ε = (B ⋅ D ⋅ v ⋅ f(σ)) ⋅ Factor_Error | Adriana Teixeira 2026")
