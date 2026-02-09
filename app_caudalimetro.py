import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de página (Debe ir al principio)
st.set_page_config(layout="centered", page_title="Simulador Adriana")

# 2. CSS para fondo TOTAL y marco negro transparente
st.markdown("""
    <style>
    /* Fondo que cubre TODA la pantalla sin recortes */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Quitar el color de fondo de la aplicación para que se vea la imagen */
    [data-testid="stHeader"], .stApp {
        background: rgba(0,0,0,0);
    }

    /* EL MARCO NEGRO VERTICAL (Rectángulo central) */
    .block-container {
        background-color: rgba(0, 0, 0, 0.85); /* Negro sólido al 85% */
        border-radius: 20px;
        padding: 3rem !important;
        max-width: 800px;
        margin-top: 50px;
        margin-bottom: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px); /* Opcional: desenfoque del fondo */
    }

    /* Forzar texto blanco */
    h1, h3, h4, p, label, .stMarkdown, [data-testid="stWidgetLabel"] p {
        color: white !important;
    }

    /* Botón moderno */
    .stButton > button {
        width: 100%;
        background-color: #00bfff;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #008fcc;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Título y autor
st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")

# 4. Parámetros del Sistema
st.markdown("#### Parámetros del Sistema")
col1, col2, col3 = st.columns(3)
with col1:
    B = st.number_input('B: Campo Magnético (T)', 0.1, 1.0, 0.5, 0.1)
with col2:
    sigma = st.number_input('σ: Conductividad (μS/cm)', 1, 5000, 1000, 100)
with col3:
    D = st.number_input('D: Diámetro (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")

def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min)))

factor = conductivity_factor(sigma)

st.write("") # Espacio

if st.button('🚀 Generar curva de calibración'):
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    Q = A * v
    V_mv = B * D * v * factor * 1000

    m = (B * D * factor * 1000) / A

    # Gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(Q, V_mv, color='#00d4ff', linewidth=2.5)
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=10)
    ax.set_ylabel('Voltaje V (mV)', fontsize=10)
    ax.set_title('Calibración V vs Q', fontsize=12)
    ax.grid(True, alpha=0.1)
    
    # Hacer el fondo de la figura transparente para el marco
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')

    st.pyplot(fig)

    st.markdown("#### Ecuación Calculada:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}}")
    st.success(f"Sensibilidad: {m:.2f} mV / (m³/s)")

st.write("---")
st.caption("Fórmula base: ε = B ⋅ D ⋅ v ⋅ f(σ) | Adriana Teixeira 2026")
