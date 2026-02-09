import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS con Fuente Roboto, Mayor Ancho y Opacidad Ajustada
st.markdown("""
    <style>
    /* Importar fuente Roboto */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de pantalla completo */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Limpiar fondos por defecto */
    [data-testid="stHeader"], .stApp {
        background: rgba(0,0,0,0);
    }

    /* FRANJA NEGRA: Más ancha (1000px), menos transparente (0.6) y sin blur */
    .block-container {
        font-family: 'Roboto', sans-serif;
        background-color: rgba(0, 0, 0, 0.6); /* Opacidad al 60% */
        padding: 4rem !important;
        max-width: 1000px; /* Más ancho */
        min-height: 100vh;
        margin: 0 auto;
        color: white !important;
        backdrop-filter: none !important;
    }

    /* Tamaño de letras aumentado */
    h1 { font-size: 3rem !important; font-weight: 700 !important; }
    h3 { font-size: 2rem !important; }
    h4 { font-size: 1.5rem !important; }
    p, label, .stMarkdown { 
        font-size: 1.2rem !important; 
        color: white !important;
    }

    /* Estilo para los inputs y sliders */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.3rem !important;
        font-weight: bold !important;
    }

    /* Botón más grande y llamativo */
    .stButton > button {
        width: 100%;
        background-color: #00bfff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 1rem;
        font-size: 1.4rem;
        font-weight: bold;
        transition: 0.3s;
        margin-top: 20px;
    }
    .stButton > button:hover {
        background-color: #008fcc;
        box-shadow: 0px 0px 20px rgba(0, 191, 255, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---

st.title('Simulación de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")



st.markdown("#### Parámetros del Sistema")
# Aumentamos el espacio entre columnas
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B = st.number_input('B: Campo Magnético (T)', 0.1, 1.0, 0.5, 0.1)
with col2:
    sigma = st.number_input('σ: Conductividad (μS/cm)', 1, 5000, 1000, 100)
with col3:
    D = st.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")

def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min)))

factor = conductivity_factor(sigma)

st.write("")

if st.button('🚀 Generar curva de calibración'):
    # Cálculos
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    Q = A * v
    V_mv = B * D * v * factor * 1000
    m = (B * D * factor * 1000) / A

    # Gráfica más grande
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6)) # Aumentamos tamaño de la figura
    ax.plot(Q, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=12, fontname='Roboto')
    ax.set_ylabel('Voltaje V (mV)', fontsize=12, fontname='Roboto')
    ax.set_title('Calibración V vs Q', fontsize=16, fontname='Roboto', pad=20)
    ax.grid(True, alpha=0.1)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')

    st.pyplot(fig)

    st.markdown("#### Ecuación de la Recta:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}}")
    st.success(f"Sensibilidad: {m:.2f} mV / (m³/s)")

st.write("---")
st.caption("Fórmula base: ε = B ⋅ D ⋅ v ⋅ f(σ) | Adriana Teixeira 2026")
