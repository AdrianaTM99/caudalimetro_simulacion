import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Caudalímetro Adriana")

# 2. CSS Mejorado: Franja persistente, Fuente Roboto y Sliders Azules
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de pantalla fijo */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Contenedor de la App transparente para ver el fondo */
    [data-testid="stHeader"], .stApp {
        background: rgba(0,0,0,0);
    }

    /* FRANJA NEGRA TRASLÚCIDA: Se ajusta al contenido para que no salga transparente */
    .main .block-container {
        font-family: 'Roboto', sans-serif;
        background-color: rgba(0, 0, 0, 0.65) !important; /* Negro translúcido sin desenfoque */
        padding: 4rem !important;
        max-width: 1100px; 
        min-height: 100vh; /* Ocupa al menos el alto de pantalla */
        height: auto;      /* Crece con el contenido para que no se corte al imprimir la gráfica */
        margin: 0 auto;
        color: white !important;
    }

    /* FUERZA SLIDERS AZULES (Elimina el naranja) */
    div[data-baseweb="slider"] div {
        background-color: transparent !important;
    }
    /* Color de la barra recorrida */
    div[data-testid="stSlider"] div[role="slider"] + div {
        background-color: #00bfff !important;
    }
    /* Color del círculo del slider */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #00bfff !important;
        border: 2px solid white !important;
    }

    /* Títulos y textos */
    h1 { font-size: 3rem !important; font-weight: 700 !important; text-align: center; }
    h3 { font-size: 1.8rem !important; text-align: center; }
    p, label, .stMarkdown { font-size: 1.1rem !important; color: white !important; }

    /* Botón */
    .stButton > button {
        width: 100%;
        background-color: #00bfff;
        color: white;
        border-radius: 8px;
        padding: 1rem;
        font-size: 1.4rem;
        font-weight: bold;
        border: none;
    }
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
    B = st.slider('Ajuste B', 0.1, 1.0, float(B_val), 0.01, label_visibility="collapsed")

with col2:
    sigma_val = st.number_input('σ: Conductividad (μS/cm)', 1, 5000, 1000, 100)
    sigma = st.slider('Ajuste σ', 1, 5000, int(sigma_val), 10, label_visibility="collapsed")

with col3:
    D_val = st.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")
    D = st.slider('Ajuste D', 0.005, 0.050, float(D_val), 0.0001, label_visibility="collapsed")

st.write("---")

# Factor de Error
st.markdown("#### Factor de Error del Sistema")
c_err1, c_err2 = st.columns([3, 1])

if 'edit_error' not in st.session_state:
    st.session_state.edit_error = False

with c_err2:
    if st.button('🔄 Modificar'):
        st.session_state.edit_error = not st.session_state.edit_error

with c_err1:
    if st.session_state.edit_error:
        error_factor = st.slider('Factor de Error Manual', 0.80, 1.20, 1.00, 0.01)
    else:
        error_factor = 1.00
        st.write(f"**Factor por defecto:** {error_factor:.2f}")

def conductivity_factor(s):
    return 1 / (1 + np.exp(-0.01 * (s - 5)))

f_cond = conductivity_factor(sigma)

if st.button('🚀 Generar curva de calibración'):
    # Cálculos
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    Q = A * v
    V_mv = (B * D * v * f_cond * 1000) * error_factor
    m = ((B * D * f_cond * 1000) / A) * error_factor

    # Gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=12)
    ax.set_ylabel('Voltaje V (mV)', fontsize=12)
    ax.grid(True, alpha=0.1)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown("#### Ecuación del Sensor:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}} \times {error_factor}")
    st.success(f"Sensibilidad: {m:.2f} mV / (m³/s)")

st.write("---")
st.caption("Fórmula base: ε = (B ⋅ D ⋅ v ⋅ f(σ)) ⋅ Factor_Error | Adriana Teixeira 2026")
