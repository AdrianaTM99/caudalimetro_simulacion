import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página con icono personalizado
URL_ICONO = "https://raw.githubusercontent.com/AdrianaTM99/caudalimetro_simulacion/main/ICONO_CAUDALIMETRO.png"

st.set_page_config(
    layout="centered", 
    page_title="Simulador Caudalímetro Adriana",
    page_icon=URL_ICONO
)

# 2. CSS para el efecto de la imagen: Fondo oscuro y panel central sólido
st.markdown("""
    <style>
    /* Fondo con imagen y capa negra encima para oscurecerla */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* EL PANEL CENTRAL: Fondo negro translúcido pero muy legible (estilo imagen 4) */
    .main .block-container {
        max-width: 800px;
        padding: 2.5rem;
        background-color: rgba(17, 17, 17, 0.9); /* Negro casi sólido */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(15px); /* Desenfoque sutil */
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        margin-top: 30px;
        margin-bottom: 30px;
    }

    /* Forzar texto blanco nítido */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sliders azules como pidió antes */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: white !important;
    }

    /* Estilo del botón azul */
    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px;
        font-weight: bold;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }

    /* Encabezado invisible */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---

st.title('🌊 Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('**Por: Adriana Teixeira Mendoza**')
st.write("---")

st.subheader("Parámetros del Sistema")
st.markdown("Ajusta los valores manualmente o usa los deslizadores:")

# Distribución en columnas para el panel
col1, col2, col3 = st.columns(3)

with col1:
    B_val = st.number_input('B: Campo Magnético (T)', 0.1, 1.0, 0.50, 0.1)
    B = st.slider('Ajuste B', 0.1, 1.0, float(B_val), 0.1, label_visibility="collapsed")

with col2:
    sigma_val = st.number_input('σ: Conductividad (µS/cm)', 1, 5000, 300, 100)
    sigma = st.slider('Ajuste σ', 1, 5000, int(sigma_val), 100, label_visibility="collapsed")

with col3:
    D_val = st.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")
    D = st.slider('Ajuste D', 0.005, 0.050, float(D_val), 0.001, label_visibility="collapsed")

# Lógica física
def calc_factor(s):
    return 1 / (1 + np.exp(-0.01 * (s - 5)))

factor_k = calc_factor(sigma)

st.write("")

if st.button('Generar curva de calibración'):
    # Cálculos físicos
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    Q = A * v
    V_mV = B * D * v * factor_k * 1000
    
    # Pendiente
    m = (B * D * factor_k * 1000) / A
    
    # Gráfica en modo oscuro integrado
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(Q, V_mV, color='#00d4ff', linewidth=3)
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=10)
    ax.set_ylabel('Voltaje V (mV)', fontsize=10)
    ax.set_title('Curva de Calibración: V vs Q', fontsize=12, pad=15)
    ax.grid(True, alpha=0.1, linestyle='--')
    
    # Integración con el panel
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    st.pyplot(fig)

    # Ecuación en formato LaTeX profesional
    st.markdown("### Ecuación de Calibración:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}} + 0")
    
    st.success(f"Sensibilidad: {m:.2f} mV / (m³/s)")


st.write("---")
st.caption("Fórmula base: $V = B \cdot D \cdot v \cdot k$ | Basado en la Ley de Inducción de Faraday.")
