import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página con tu icono personalizado
URL_ICONO = "https://raw.githubusercontent.com/AdrianaTM99/caudalimetro_simulacion/main/ICONO_CAUDALIMETRO.png"

st.set_page_config(
    layout="centered", 
    page_title="Simulador Caudalímetro Adriana",
    page_icon=URL_ICONO
)

# 2. CSS para el fondo del mar, panel translúcido y sliders azules
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/large_2x/sea-surface-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* RECUADRO NEGRO TRANSLÚCIDO CON DESENFOQUE */
    .main .block-container {
        max-width: 850px;
        padding: 3rem;
        background-color: rgba(0, 0, 0, 0.75); /* Fondo negro con 75% opacidad */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        backdrop-filter: blur(15px); /* Desenfoque de la imagen de fondo */
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.9);
        margin-top: 40px;
        margin-bottom: 40px;
    }

    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 1);
    }

    /* SLIDERS AZULES */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: #ffffff !important;
    }

    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO DEL PROGRAMA ---

st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")

st.markdown("#### Parámetros del Sistema (Ajuste Manual o Deslizante)")

# Función para entrada manual + slider
col1, col2, col3 = st.columns(3)

with col1:
    B = st.number_input('B: Campo Magnético (T)', 0.1, 1.0, 0.5, 0.1)
    B = st.slider('Ajuste B', 0.1, 1.0, float(B), 0.1, label_visibility="collapsed")

with col2:
    sigma = st.number_input('σ: Conductividad (µS/cm)', 1, 5000, 1000, 100)
    sigma = st.slider('Ajuste σ', 1, 5000, int(sigma), 100, label_visibility="collapsed")

with col3:
    D = st.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")
    D = st.slider('Ajuste D', 0.005, 0.050, float(D), 0.001, label_visibility="collapsed")

# Lógica del Factor de Conductividad
def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min))) 

factor = conductivity_factor(sigma)

st.write("") 

if st.button('🚀 Generar curva de calibración'):
    # Cálculos
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5, 100) # Rango de velocidad del fluido
    Q = A * v # m³/s
    V_theor = B * D * v * factor * 1000 # mV
    
    # Cálculo de la pendiente de la curva V vs Q
    # V = B * D * (Q/A) * factor * 1000 -> Pendiente m = (B * D * factor * 1000) / A
    pendiente = (B * D * factor * 1000) / A
    
    # Gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(Q, V_theor, color='#00e5ff', linewidth=3)
    ax.set_xlabel('Caudal Q (m³/s)')
    ax.set_ylabel('Voltaje V (mV)')
    ax.set_title(f'Curva de Calibración: Voltaje vs Caudal')
    ax.grid(True, alpha=0.2)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)
    
    # MOSTRAR ECUACIÓN DE LA CURVA
    st.markdown("### Ecuación de la Curva Calculada:")
    st.latex(rf"V_{(mV)} = {pendiente:.2f} \cdot Q_{(m^3/s)} + 0")
    
    st.info(f"Sensibilidad del sensor: {pendiente:.2f} mV / (m³/s)")



st.markdown("---")
st.caption("Fórmula base: $V = B \cdot D \cdot v \cdot k$ | Basado en la Ley de Inducción de Faraday.")
