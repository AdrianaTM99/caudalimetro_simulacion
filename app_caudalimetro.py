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

# 2. CSS para Fondo del Mar y Panel de Contraste Reforzado
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

    /* PANEL CENTRAL: Negro con opacidad alta para evitar transparencia excesiva */
    .main .block-container {
        max-width: 850px;
        padding: 3rem;
        background-color: rgba(0, 0, 0, 0.85); /* 85% de opacidad para que no sea transparente */
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        backdrop-filter: blur(20px); /* Desenfoque fuerte del mar de fondo */
        box-shadow: 0 20px 60px rgba(0, 0, 0, 1);
        margin-top: 30px;
        margin-bottom: 30px;
    }

    /* Estilo para los textos y etiquetas */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 1); /* Sombra para resaltar texto */
    }

    /* Color de los Sliders a Azul */
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
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: translateY(-2px);
    }

    /* Barra superior invisible */
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

# Configuración de entrada dual (Número + Slider)
col1, col2, col3 = st.columns(3)

with col1:
    B_in = st.number_input('B: Campo Magnético (T)', 0.1, 1.0, 0.5, 0.1)
    B = st.slider('Ajuste B', 0.1, 1.0, float(B_in), 0.1, label_visibility="collapsed")

with col2:
    sigma_in = st.number_input('σ: Conductividad (µS/cm)', 1, 5000, 1000, 100)
    sigma = st.slider('Ajuste σ', 1, 5000, int(sigma_in), 100, label_visibility="collapsed")

with col3:
    D_in = st.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")
    D = st.slider('Ajuste D', 0.005, 0.050, float(D_in), 0.001, label_visibility="collapsed")

# Lógica física
def get_factor(s):
    return 1 / (1 + np.exp(-0.01 * (s - 5))) 

factor = get_factor(sigma)

st.write("")

if st.button('🚀 Generar curva de calibración'):
    # Cálculos de la curva
    A = np.pi * (D / 2)**2
    v_range = np.linspace(0.1, 5.0, 100)
    Q = A * v_range
    V = B * D * v_range * factor * 1000 # Resultado en mV
    
    # Pendiente m
    m = (B * D * factor * 1000) / A
    
    # Gráfica en modo oscuro total
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(Q, V, color='#00d4ff', linewidth=3, label='Respuesta V vs Q')
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=12)
    ax.set_ylabel('Voltaje V (mV)', fontsize=12)
    ax.set_title('Curva de Calibración Resultante', fontsize=14, pad=20)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    # Integración estética con el panel
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    st.pyplot(fig)
    
    # Resultado matemático
    st.markdown("### Ecuación de la Curva Calculada:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}} + 0")
    
    st.success(f"Simulación exitosa. Sensibilidad: {m:.2f} mV / (m³/s)")

st.write("---")
st.caption("Fórmula aplicada: $V = B \cdot D \cdot v \cdot k$ | Ley de Inducción de Faraday.")
