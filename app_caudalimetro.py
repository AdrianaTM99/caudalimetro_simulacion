import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de página
st.set_page_config(layout="centered", page_title="Simulador Caudalímetro")

# 2. CSS Avanzado para el contenedor de datos y sliders azules
st.markdown("""
    <style>
    /* Fondo total de la pantalla */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://img.freepik.com/foto-gratis/fondo-galaxia-estilo-fantasia_23-2151114299.jpg?semt=ais_hybrid&w=740&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* CONTENEDOR DE DATOS: Fondo negro ligero, bordes y sombra */
    .main .block-container {
        max-width: 850px;
        padding: 3rem;
        background-color: rgba(0, 0, 0, 0.65); /* Fondo negro semi-transparente */
        border: 1px solid rgba(255, 255, 255, 0.1); /* Borde muy fino para dar relieve */
        border-radius: 25px; /* Bordes redondeados */
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8); /* Sombra para separar del fondo */
        margin-top: 50px;
    }

    /* Forzar texto blanco */
    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 1px 1px 2px black; /* Sombra en texto para máxima legibilidad */
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

    /* Barra superior transparente */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Contenido del Programa ---

st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---") # Una línea divisoria elegante

# Sliders
B = st.slider('Intensidad del Campo Magnético B (T)', 0.1, 1.0, 0.5, 0.1)
sigma = st.slider('Conductividad del Fluido σ (µS/cm)', 1, 5000, 1000, 100)
D = st.slider('Diámetro Interno D (m)', 0.005, 0.02, 0.0127, 0.001)

def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min))) 

factor = conductivity_factor(sigma)

# Gráfica
if st.button('Generar Gráfica V vs Q'):
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 10, 100)
    V_theor = B * D * v * factor * 1000 
    Q = A * v 
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    
    # Color cian para que resalte sobre el negro
    ax.plot(Q, V_theor, color='#00d4ff', linewidth=3, label='Respuesta del sensor')
    ax.set_xlabel('Caudal Q (m³/s)')
    ax.set_ylabel('Voltaje V (mV)')
    ax.set_title(f'V vs Q (B={B}T, D={D}m)')
    ax.grid(True, alpha=0.2)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    st.pyplot(fig)

st.info('Los datos ahora están protegidos por un panel para mejorar la visibilidad.')
