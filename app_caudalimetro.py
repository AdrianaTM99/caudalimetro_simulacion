import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="Simulador Caudalímetro")

# 2. CSS para Fondo, Texto Blanco y Sliders Azules
st.markdown("""
    <style>
    /* Fondo total de la app */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://img.freepik.com/fotos-premium/hermosa-playa-nocturna-rocas-via-lactea_104785-856.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Quitar color a la cabecera */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    /* Forzar texto blanco en toda la app */
    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
    }

    /* CAMBIAR COLOR DE LOS SLIDERS A AZUL */
    /* Color de la barra recorrida */
    .stSlider [data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    .stSlider [data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    /* Color del círculo (tirador) del slider */
    div[data-testid="stThumbValue"] {
        background-color: #007bff !important;
    }
    
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: #007bff !important;
    }

    /* Fondo de los widgets para que resalten un poco */
    .stSlider, .stButton {
        background-color: rgba(0, 0, 0, 0.4);
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Lógica de la simulación ---

st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('**Por:** Adriana Teixeira Mendoza')

# Sliders (ahora se verán azules gracias al CSS)
B = st.slider('Intensidad del Campo Magnético B (T)', 0.1, 1.0, 0.5, 0.1)
sigma = st.slider('Conductividad del Fluido σ (µS/cm)', 1, 5000, 1000, 100)
D = st.slider('Diámetro Interno D (m)', 0.005, 0.02, 0.0127, 0.001)

def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min))) 

factor = conductivity_factor(sigma)

if st.button('Generar Gráfica V vs Q'):
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 10, 100)
    V_theor = B * D * v * factor * 1000 
    Q = A * v 
    
    # MODO OSCURO PARA MATPLOTLIB
    plt.style.use('dark_background')
    
    fig, ax = plt.subplots()
    
    # Elegir un color de línea que resalte en modo oscuro
    line_color = '#00ffcc' # Un cian neón
    if B < 0.4: line_color = '#ff3333' # Rojo neón
    elif B > 0.7: line_color = '#3399ff' # Azul brillante

    ax.plot(Q, V_theor, color=line_color, linewidth=2)
    ax.set_xlabel('Caudal Q (m³/s)', color='white')
    ax.set_ylabel('Voltaje V (mV)', color='white')
    ax.set_title(f'V vs Q (B={B}T, D={D}m)', color='white')
    
    # Hacer que el fondo de la figura sea transparente para que se vea el fondo de la playa
    fig.patch.set_alpha(0.0)
    ax.set_facecolor(range=(0,0,0,0.2)) # Fondo del eje ligeramente oscuro
    
    st.pyplot(fig)



st.info('La gráfica y los controles se han adaptado al modo nocturno.')
