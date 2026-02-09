import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página con tu icono personalizado de GitHub
# Usamos la URL raw para que Streamlit pueda renderizar el archivo de imagen
URL_ICONO = "https://raw.githubusercontent.com/AdrianaTM99/caudalimetro_simulacion/main/ICONO_CAUDALIMETRO.png"

st.set_page_config(
    layout="centered", 
    page_title="Simulador Caudalímetro Adriana",
    page_icon=URL_ICONO
)

# 2. CSS para Fondo de Unsplash, Panel de Contraste y Sliders Azules
st.markdown("""
    <style>
    /* Imagen de fondo de alta calidad */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1580659986392-440ea995857c?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8bGF1dGFuJTIwbWFsYW18ZW58MHx8MHx8fDA%3D");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* EL PANEL DE CONTRASTE: Negro traslúcido con desenfoque */
    .main .block-container {
        max-width: 850px;
        padding: 3rem;
        background-color: rgba(0, 0, 0, 0.75); 
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        backdrop-filter: blur(12px); 
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.9);
        margin-top: 40px;
        margin-bottom: 40px;
    }

    /* Forzar texto blanco nítido */
    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 1);
    }

    /* Sliders en color Azul */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: #ffffff !important;
    }

    /* Botón personalizado */
    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
        transform: scale(1.02);
    }

    /* Barra superior transparente */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO DEL PROGRAMA ---

st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")

# Parámetros de entrada
st.markdown("#### Ajuste de Variables del Sistema")
B = st.slider('Intensidad del Campo Magnético B (T)', 0.1, 1.0, 0.5, 0.1)
sigma = st.slider('Conductividad del Fluido σ (µS/cm)', 1, 5000, 1000, 100)
D = st.slider('Diámetro Interno D (m)', 0.005, 0.02, 0.0127, 0.001)

def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min))) 

factor = conductivity_factor(sigma)

st.write("") 

# Acción y Gráfica
if st.button('Generar curva de calibreación'):
    # Física del problema (Ley de Faraday)
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 10, 100) 
    V_theor = B * D * v * factor * 1000 # Resultado en mV
    Q = A * v # m³/s
    
    # Configuración visual de la gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Línea de la señal
    ax.plot(Q, V_theor, color='#00e5ff', linewidth=3)
    
    ax.set_xlabel('Caudal Volumétrico Q (m³/s)', fontsize=10)
    ax.set_ylabel('Voltaje Inducido V (mV)', fontsize=10)
    ax.set_title(f'Respuesta en Función del Caudal (B={B}T)', fontsize=12, pad=15)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    # Integración con el fondo del panel
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    st.pyplot(fig)
    st.success(f"Simulación lista. Factor de corrección aplicado: {factor:.4f}")



st.markdown("---")
st.caption("Fórmula base: $V = B \cdot D \cdot v \cdot k$ | Basado en la Ley de Inducción de Faraday.")

