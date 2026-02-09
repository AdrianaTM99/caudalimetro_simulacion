import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de página
st.set_page_config(layout="centered", page_title="Simulador Adriana")

# 2. CSS para Fondo de Mar TOTAL y Franja Negra Translúcida Limpia
st.markdown("""
    <style>
    /* Fondo que cubre TODA la pantalla */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Hacer transparentes los contenedores por defecto de Streamlit */
    [data-testid="stHeader"], .stApp {
        background: rgba(0,0,0,0);
    }

    /* FRANJA NEGRA VERTICAL: Más transparente, sin desenfoque, de borde a borde */
    .block-container {
        background-color: rgba(0, 0, 0, 0.4); /* Negro muy transparente (40%) */
        padding: 3rem !important;
        max-width: 850px;
        min-height: 100vh; /* Ocupa todo el alto de la pantalla */
        margin: 0 auto; 
        color: white !important;
        backdrop-filter: none !important; /* ELIMINADO EL DESENFOQUE */
        box-shadow: none; /* Estética limpia sin sombras pesadas */
    }

    /* Estilo de textos para que resalten sobre la transparencia */
    h1, h3, h4, p, label, .stMarkdown, [data-testid="stWidgetLabel"] p {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 1); /* Sombra suave para leer bien */
    }

    /* Botón azul plano */
    .stButton > button {
        width: 100%;
        background-color: #00bfff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.6rem;
        font-weight: bold;
    }
    
    /* Línea divisoria */
    hr {
        border-color: rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIO DEL CONTENIDO ---

st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")

# Diagrama opcional si lo tienes en local o URL
# 

st.markdown("#### Parámetros del Sistema")
col1, col2, col3 = st.columns(3)

with col1:
    B = st.number_input('B: Campo Magnético (T)', 0.1, 1.0, 0.5, 0.1)
with col2:
    sigma = st.number_input('σ: Conductividad (μS/cm)', 1, 5000, 1000, 100)
with col3:
    D = st.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")

# Cálculo del factor basado en conductividad
def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min)))

factor = conductivity_factor(sigma)

st.write("")

if st.button('🚀 Generar curva de calibración'):
    # Cálculos físicos
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    Q = A * v
    V_mv = B * D * v * factor * 1000
    m = (B * D * factor * 1000) / A

    # Gráfica optimizada para fondo transparente
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(Q, V_mv, color='#00d4ff', linewidth=2.5)
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=10)
    ax.set_ylabel('Voltaje V (mV)', fontsize=10)
    ax.set_title('Calibración V vs Q', fontsize=12)
    ax.grid(True, alpha=0.1)
    
    # Transparencia en la gráfica
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')

    st.pyplot(fig)

    st.markdown("#### Ecuación Calculada:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}}")
    st.success(f"Sensibilidad: {m:.2f} mV / (m³/s)")

st.write("---")
st.caption("Fórmula base: ε = B ⋅ D ⋅ v ⋅ f(σ) | Adriana Teixeira 2026")
