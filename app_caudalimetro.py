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

# 2. CSS Mejorado: Fondo negro translúcido integral y protección de contraste
st.markdown("""
    <style>
    /* 1. Fondo general de la aplicación */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* 2. RECUADRO NEGRO INTEGRAL: Envuelve toda la información */
    .main {
        background-color: rgba(0, 0, 0, 0.5); /* Oscurece un poco más el fondo general */
    }

    .main .block-container {
        max-width: 850px;
        padding: 3rem;
        background-color: rgba(0, 0, 0, 0.85); /* Negro sólido al 85% */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px); /* Desenfoque profundo para legibilidad */
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
        margin-top: 50px;
        margin-bottom: 50px;
    }

    /* 3. Estilo de textos */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
    }

    /* 4. Sliders Azules Profesionales */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: #ffffff !important;
    }

    /* 5. Botón de Acción */
    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 15px;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: scale(1.01);
    }

    /* Quitar la barra blanca superior */
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

# Organización en columnas para limpieza visual
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

# Lógica matemática (Ley de Faraday)
def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min))) 

factor = conductivity_factor(sigma)

st.write("")

if st.button('🚀 Generar curva de calibración'):
    # Física del proceso
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5, 100) 
    Q = A * v 
    V_theor = B * D * v * factor * 1000 # mV
    
    # Pendiente m
    pendiente = (B * D * factor * 1000) / A
    
    # Gráfica en modo oscuro integrado
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.plot(Q, V_theor, color='#00d4ff', linewidth=3, label='Señal inducida')
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=10)
    ax.set_ylabel('Voltaje V (mV)', fontsize=10)
    ax.set_title(f'Curva de Calibración Resultante', fontsize=12, pad=15)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    # Transparencia para que se vea el panel negro detrás
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    st.pyplot(fig)
    
    # Ecuación matemática
    st.markdown("### Ecuación de la Curva Calculada:")
    st.latex(rf"V_{{(mV)}} = {pendiente:.2f} \cdot Q_{{(m^3/s)}} + 0")
    
    st.success(f"Sensibilidad calculada: {pendiente:.2f} mV / (m³/s)")



st.write("---")
st.caption("Fórmula base: $V = B \cdot D \cdot v \cdot k$ | Basado en la Ley de Inducción de Faraday.")
