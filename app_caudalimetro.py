import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. CSS para fondo de mar y marco negro transparente
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");  # Fondo de mar oscuro
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .block-container {
        background-color: rgba(0, 0, 0, 0.7);  # Negro transparente para no saturar
        border-radius: 15px;
        padding: 2rem;
        max-width: 800px;
        margin: auto;
        color: white !important;  # Texto blanco
    }
    h1, h3, h4, p, label {
        color: white !important;
    }
    div[data-testid="stSliderLabel"] {
        color: white !important;
    }
    .stButton > button {
        background-color: #00bfff;  # Azul moderno
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stMarkdown {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Título y autor
st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('**Por: Adriana Teixeira Mendoza**')

# 3. Parámetros del Sistema en columnas
st.markdown("#### Parámetros del Sistema")
col1, col2, col3 = st.columns(3)
with col1:
    B = col1.number_input('B: Campo Magnético (T)', 0.1, 1.0, 0.5, 0.1)
with col2:
    sigma = col2.number_input('σ: Conductividad (μS/cm)', 1, 5000, 1000, 100)
with col3:
    D = col3.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")

# Función para factor sigmoide
def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min)))

factor = conductivity_factor(sigma)

# Botón para generar curva
if st.button('Generar curva de calibración'):
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    Q = A * v
    V_mv = B * D * v * factor * 1000

    m = (B * D * factor * 1000) / A

    # Gráfica en modo oscuro
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.plot(Q, V_mv, color='#00d4ff', linewidth=2.5)
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=9)
    ax.set_ylabel('Voltaje V (mV)', fontsize=9)
    ax.set_title('Calibración V vs Q', fontsize=11)
    ax.grid(True, alpha=0.1)

    st.pyplot(fig)

    st.markdown("#### Ecuación:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}}")
    st.success(f"Sensibilidad: {m:.2f} mV / (m³/s)")

# Pie de página
st.write("---")
st.caption("Fórmula base: ε = B ⋅ D ⋅ v ⋅ f(σ) | Adriana Teixeira 2026")
