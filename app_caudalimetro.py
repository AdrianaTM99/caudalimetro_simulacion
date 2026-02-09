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

# 2. CSS PARA EL MARCO NEGRO VERTICAL (RECTÁNGULO DEFINIDO)
st.markdown("""
    <style>
    /* Fondo de la página (el mar) */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* EL MARCO O RECTÁNGULO NEGRO VERTICAL */
    .main .block-container {
        max-width: 700px; /* Reducido para que parezca más un rectángulo vertical */
        padding: 3rem;
        background-color: rgba(0, 0, 0, 0.88); /* Negro casi total para que no sea transparente */
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        backdrop-filter: blur(20px);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 1);
        margin: auto; /* Centra el rectángulo */
        margin-top: 50px;
        margin-bottom: 50px;
    }

    /* Texto blanco con sombra para máxima lectura */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 1) !important;
    }

    /* Sliders Azules */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: #ffffff !important;
    }

    /* Botón Profesional */
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

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---

st.title('Simulación de Caudalímetro Electromagnético')
st.markdown('### Adriana Teixeira Mendoza')
st.write("---")

st.markdown("#### Parámetros del Sistema")

# Columnas para las entradas
col1, col2, col3 = st.columns(3)

with col1:
    B_val = st.number_input('B (T)', 0.1, 1.0, 0.5, 0.1)
    B = st.slider('B_slider', 0.1, 1.0, float(B_val), 0.1, label_visibility="collapsed")

with col2:
    sigma_val = st.number_input('σ (µS/cm)', 1, 5000, 1000, 100)
    sigma = st.slider('σ_slider', 1, 5000, int(sigma_val), 100, label_visibility="collapsed")

with col3:
    D_val = st.number_input('D (m)', 0.005, 0.050, 0.0127, 0.001, format="%.4f")
    D = st.slider('D_slider', 0.005, 0.050, float(D_val), 0.001, label_visibility="collapsed")

def get_factor(s):
    return 1 / (1 + np.exp(-0.01 * (s - 5))) 

factor = get_factor(sigma)

st.write("")

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
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=9)
    ax.set_ylabel('Voltaje V (mV)', fontsize=9)
    ax.set_title('Calibración V vs Q', fontsize=11)
    ax.grid(True, alpha=0.1)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)
    
    st.markdown("#### Ecuación:")
    st.latex(rf"V_{{(mV)}} = {m:.2f} \cdot Q_{{(m^3/s)}}")
    st.success(f"Sensibilidad: {m:.2f} mV / (m³/s)")

st.write("---")



st.caption("Fórmula: $V = B \cdot D \cdot v \cdot k$ | Adriana Teixeira 2026")
