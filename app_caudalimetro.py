import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de página (Quitamos el modo wide para que esté centrado)
st.set_page_config(layout="centered", page_title="Simulador Caudalímetro")

# 2. CSS para fondo total, contenido centrado/ancho y sliders azules
st.markdown("""
    <style>
    /* Imagen de fondo total con alta calidad */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://img.freepik.com/foto-gratis/fondo-galaxia-estilo-fantasia_23-2151114299.jpg?semt=ais_hybrid&w=740&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Ajustar el ancho del contenedor centrado */
    .main .block-container {
        max-width: 900px; /* Aquí controlas qué tan ancho es el programa en el centro */
        padding-top: 2rem;
        background-color: rgba(0, 0, 0, 0.4); /* Fondo sutil para legibilidad */
        border-radius: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* Forzar texto blanco */
    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
    }

    /* CAMBIAR SLIDERS A AZUL */
    /* Parte recorrida de la barra */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    /* El círculo o tirador */
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: #007bff !important;
    }

    /* El valor que aparece sobre el slider */
    div[data-testid="stThumbValue"] {
        color: white !important;
    }

    /* Barra superior transparente */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Contenido de la App ---

st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')

# Sliders (Ahora azules)
B = st.slider('Intensidad del Campo Magnético B (T)', 0.1, 1.0, 0.5, 0.1)
sigma = st.slider('Conductividad del Fluido σ (µS/cm)', 1, 5000, 1000, 100)
D = st.slider('Diámetro Interno D (m)', 0.005, 0.02, 0.0127, 0.001)

def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min))) 

factor = conductivity_factor(sigma)

# Botón centrado
if st.button('Generar Gráfica V vs Q'):
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 10, 100)
    V_theor = B * D * v * factor * 1000 
    Q = A * v 
    
    # Gráfica en modo oscuro
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    
    # Color de línea azul/cian para combinar
    ax.plot(Q, V_theor, color='#00d4ff', linewidth=3)
    ax.set_xlabel('Caudal Q (m³/s)')
    ax.set_ylabel('Voltaje V (mV)')
    ax.set_title(f'Relación Voltaje vs Caudal (B={B}T)')
    ax.grid(True, alpha=0.3)
    
    # Fondo transparente de la figura
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    st.pyplot(fig)

st.info('Ajusta los valores en el centro y observa el comportamiento del caudalímetro.')
