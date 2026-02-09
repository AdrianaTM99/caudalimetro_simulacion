import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS con Fuente Roboto, Sliders Azules y Diseño de Franja
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

    [data-testid="stHeader"], .stApp {
        background: rgba(0,0,0,0);
    }

    .block-container {
        font-family: 'Roboto', sans-serif;
        background-color: rgba(0, 0, 0, 0.6); 
        padding: 4rem !important;
        max-width: 1100px; 
        min-height: 100vh;
        margin: 0 auto;
        color: white !important;
        backdrop-filter: none !important;
    }

    /* Estilo de textos */
    h1 { font-size: 3rem !important; font-weight: 700 !important; text-align: center; }
    h3 { font-size: 1.8rem !important; text-align: center; }
    h4 { font-size: 1.5rem !important; margin-top: 20px; }
    p, label, .stMarkdown { font-size: 1.1rem !important; color: white !important; }

    /* Personalización de Sliders a Azul */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"] {
        background-color: #00bfff !important;
    }
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #00bfff !important;
    }

    /* Botón Principal */
    .stButton > button {
        width: 100%;
        background-color: #00bfff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 1rem;
        font-size: 1.4rem;
        font-weight: bold;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---

st.title('Simulación de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")

st.markdown("#### Configuración de Parámetros")
st.info("Puedes ingresar los datos manualmente o deslizando la barra azul.")

# Columnas para los parámetros principales
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

# Sección del Factor de Error
st.markdown("#### Factor de Error del Sistema")
c_err1, c_err2 = st.columns([3, 1])

# Valor por defecto del error es 1.0 (sin error) o 0.05 (5% de error) según se prefiera
# Aquí lo definimos como 1.0 para que el cálculo sea puro por defecto
if 'edit_error' not in st.session_state:
    st.session_state.edit_error = False

with c_err2:
    if st.button('🔄 Cambiar Factor'):
        st.session_state.edit_error = not st.session_state.edit_error

with c_err1:
    if st.session_state.edit_error:
        error_factor = st.slider('Modificar Factor de Error (Manual)', 0.80, 1.20, 1.00, 0.01)
        st.warning(f"Factor de error actual: {error_factor:.2f} (Modificado)")
    else:
        error_factor = 1.00
        st.success(f"Factor de error por defecto: {error_factor:.2f} (Estable)")

# Lógica de cálculo
def conductivity_factor(s, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (s - sigma_min)))

f_cond = conductivity_factor(sigma)

if st.button('🚀 Generar curva de calibración'):
    # Cálculos incluyendo el factor de error
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    Q = A * v
    V_mv = (B * D * v * f_cond * 1000) * error_factor
    m = ((B * D * f_cond * 1000) / A) * error_factor

    # Gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q, V_mv, color='#00d4ff', linewidth=3, label='Respuesta con Error')
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=12)
    ax.set_ylabel('Voltaje V (mV)', fontsize=12)
    ax.set_title('Calibración V vs Q (Ajustada)', fontsize=16, pad=20)
    ax.grid(True, alpha=0.1)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    # Resultados y Ecuación
    st.markdown("#### Ecuación Final del Sensor:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}} \times {error_factor}")
    st.info(f"Sensibilidad Resultante: {m:.2f} mV / (m³/s)")

st.write("---")
st.caption("Fórmula base: ε = (B ⋅ D ⋅ v ⋅ f(σ)) ⋅ Factor_Error | Adriana Teixeira 2026")
