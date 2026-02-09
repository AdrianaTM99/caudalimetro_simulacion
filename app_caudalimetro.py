import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página e Icono personalizado
URL_ICONO = "https://raw.githubusercontent.com/AdrianaTM99/caudalimetro_simulacion/main/ICONO_CAUDALIMETRO.png"

st.set_page_config(
    layout="centered", 
    page_title="Simulador Caudalímetro Adriana",
    page_icon=URL_ICONO
)

# 2. CSS AVANZADO: Fondo negro translúcido reforzado y desenfoque
st.markdown("""
    <style>
    /* Imagen de fondo del mar */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* EL PANEL CENTRAL: Negro sólido al 90% con desenfoque extremo */
    /* Esto garantiza que NO se vea transparente el texto sobre las olas */
    .main .block-container {
        max-width: 850px;
        padding: 3rem;
        background-color: rgba(0, 0, 0, 0.9) !important; /* Casi negro total */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(25px); /* Desenfoque muy fuerte */
        box-shadow: 0 15px 60px rgba(0, 0, 0, 1);
        margin-top: 40px;
        margin-bottom: 40px;
    }

    /* Forzar texto blanco nítido con sombra negra para legibilidad absoluta */
    h1, h2, h3, h4, p, label, span, .stMarkdown {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 1) !important;
    }

    /* Sliders Azules */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: #ffffff !important;
    }

    /* Estilo del Botón */
    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 15px;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: scale(1.01);
    }

    /* Quitar barra superior blanca para que sea todo oscuro */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIO DEL CONTENIDO ---

st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")

st.markdown("#### Parámetros del Sistema (Entrada Manual o Slider)")

# Organización en columnas
col1, col2, col3 = st.columns(3)

with col1:
    B_val = st.number_input('B: Campo Magnético (T)', 0.1, 1.0, 0.5, 0.1)
    B = st.slider('Ajuste B', 0.1, 1.0, float(B_val), 0.1, label_visibility="collapsed")

with col2:
    sigma_val = st.number_input('σ: Conductividad (µS/cm)', 1, 5000, 1000, 100)
    sigma = st.slider('Ajuste σ', 1, 5000, int(sigma_val), 100, label_visibility="collapsed")

with col3:
    D_val = st.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")
    D = st.slider('Ajuste D', 0.005, 0.050, float(D_val), 0.001, label_visibility="collapsed")

# Lógica de cálculo (Ley de Faraday)
def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min))) 

factor = conductivity_factor(sigma)

st.write("")

if st.button('🚀 Generar curva de calibración'):
    # Cálculos físicos
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5, 100) 
    Q = A * v 
    V_theor = B * D * v * factor * 1000 # Resultado en mV
    
    # Pendiente m (Ecuación lineal)
    m = (B * D * factor * 1000) / A
    
    # GRÁFICA EN MODO OSCURO TOTAL
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.plot(Q, V_theor, color='#00d4ff', linewidth=3, label='Respuesta del sensor')
    ax.set_xlabel('Caudal Q (m³/s)', color='white', fontsize=10)
    ax.set_ylabel('Voltaje V (mV)', color='white', fontsize=10)
    ax.set_title(f'Curva de Calibración: V vs Q', color='white', pad=20)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    # Ajustar para que no haya bordes blancos en la imagen generada
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    st.pyplot(fig)
    
    # IMPRESIÓN DE LA ECUACIÓN
    st.markdown("### Ecuación de la Curva Calculada:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}} + 0")
    
    st.success(f"Sensibilidad calculada: {m:.2f} mV / (m³/s)")

st.write("---")

# Diagrama del principio de funcionamiento

st.caption("Fórmula base: $V = B \cdot D \cdot v \cdot k$ | Basado en la Ley de Inducción de Faraday.")
