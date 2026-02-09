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

# 2. CSS para Fondo del Mar Muy Opaco y Panel de Contraste Máximo
st.markdown("""
    <style>
    /* Imagen de fondo con filtro de brillo muy bajo para que sea opaca */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                          url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        filter: brightness(0.6); /* Reduce el brillo general de la imagen */
    }

    /* PANEL CENTRAL: Fondo casi negro sólido para evitar distracciones */
    .main .block-container {
        max-width: 850px;
        padding: 3rem;
        background-color: rgba(10, 10, 10, 0.92); /* Casi negro total */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(25px); /* Desenfoque extremo */
        box-shadow: 0 25px 50px rgba(0, 0, 0, 1);
        margin-top: 30px;
        margin-bottom: 30px;
    }

    /* Estilo para los textos */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 1);
    }

    /* Sliders Azules Profesionales */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: #ffffff !important;
    }

    /* Botón de Generar Curva */
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
        box-shadow: 0px 0px 15px rgba(0, 123, 255, 0.6);
    }

    /* Quitar elementos innecesarios */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO DEL SIMULADOR ---

st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")

st.markdown("#### Parámetros del Sistema (Entrada Manual o Slider)")

# Sistema de entrada dual
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

# Lógica del Factor K
def get_k(s):
    return 1 / (1 + np.exp(-0.01 * (s - 5))) 

factor_k = get_k(sigma)

st.write("")

if st.button('🚀 Generar curva de calibración'):
    # Cálculos
    A = np.pi * (D / 2)**2
    v_vec = np.linspace(0.1, 5.0, 100)
    Q_vec = A * v_vec
    V_vec = B * D * v_vec * factor_k * 1000 # mV
    
    # Pendiente (Ecuación lineal V = mQ)
    m = (B * D * factor_k * 1000) / A
    
    # Gráfica en modo oscuro
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(Q_vec, V_vec, color='#00d4ff', linewidth=3, label='Respuesta del Sensor')
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=11)
    ax.set_ylabel('Voltaje V (mV)', fontsize=11)
    ax.set_title('Curva de Calibración: Voltaje vs Caudal', fontsize=14, pad=20)
    ax.grid(True, alpha=0.15, linestyle='--')
    
    # Quitar marcos de la figura para integración total
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    st.pyplot(fig)
    
    # Ecuación de la curva
    st.markdown("### Ecuación de la Curva Calculada:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}} + 0")
    
    st.success(f"Sensibilidad del sistema: {m:.2f} mV / (m³/s)")

st.write("---")


st.caption("Fórmula: $V = B \cdot D \cdot v \cdot k$ | Basado en la Ley de Faraday.")
