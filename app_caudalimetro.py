import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Pro Adriana")

# 2. CSS Maestro: Franja Negra Infinita y Persistente
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de imagen FIJO con la FRANJA NEGRA INFINITA */
    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(
                to right, 
                transparent 0%, 
                transparent calc(50% - 550px), 
                rgba(0, 0, 0, 0.5) calc(50% - 550px), 
                rgba(0, 0, 0, 0.5) calc(50% + 550px), 
                transparent calc(50% + 550px), 
                transparent 100%
            ),
            url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .stApp, [data-testid="stHeader"], .block-container {
        background: transparent !important;
    }

    .block-container {
        font-family: 'Roboto', sans-serif;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 4rem 2rem !important;
        color: white !important;
    }

    /* TÍTULO A LA IZQUIERDA */
    h1 { font-size: 3rem !important; font-weight: 700 !important; text-align: left !important; }
    h3 { font-size: 1.6rem !important; text-align: left !important; font-weight: 300 !important; }

    /* SLIDERS AZULES (#00D4FF) */
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; border: 2px solid white !important; }

    /* BOTÓN AZUL */
    .stButton > button {
        width: 100%;
        background-color: #00d4ff;
        color: white;
        border-radius: 8px;
        padding: 0.8rem;
        font-size: 1.2rem;
        font-weight: bold;
        border: none;
    }

    /* Estilo para la calculadora interactiva */
    .stNumberInput input { background-color: rgba(255,255,255,0.1) !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE UNIDADES ---
st.title('Simulación de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')

# Selector de Sistema de Unidades
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Sistema Internacional (m, m³/s)", "Sistema Americano (in, GPM)"), horizontal=True)

st.write("---")

# Definición de variables según sistema
if sistema == "Sistema Internacional (m, m³/s)":
    u_d, u_q, u_v = "m", "m³/s", "mV"
    d_def, d_min, d_max = 0.0127, 0.001, 0.1
    q_label = "Caudal (m³/s)"
else:
    u_d, u_q, u_v = "in", "GPM", "mV"
    d_def, d_min, d_max = 0.5, 0.05, 4.0
    q_label = "Caudal (GPM)"

# --- PARÁMETROS ---
st.markdown("#### Parámetros del Sistema")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B = st.slider('B: Campo Magnético (Tesla)', 0.1, 1.5, 0.5, 0.01)
with col2:
    sigma = st.slider('σ: Conductividad (μS/cm)', 5, 5000, 1000, 10)
with col3:
    D = st.slider(f'D: Diámetro ({u_d})', d_min, d_max, d_def, 0.001 if u_d=="m" else 0.01)

# Factor de Error
with st.expander("Ajustes Avanzados (Factor de Error)"):
    error_factor = st.slider("Factor de corrección manual", 0.80, 1.20, 1.00, 0.01)

# --- CÁLCULOS BASE ---
# Conversión interna a metros para física si es necesario
D_fisico = D if u_d == "m" else D * 0.0254
area_fisica = np.pi * (D_fisico / 2)**2
f_cond = 1 / (1 + np.exp(-0.01 * (sigma - 5)))

# Pendiente de la recta V = m * Q
# m = (B * D * (1/Area) * factor_cond * 1000) * error
m_si = (B * D_fisico * (1/area_fisica) * f_cond * 1000) * error_factor

# Ajuste de m si el usuario usa GPM (1 m3/s = 15850.3 GPM)
m_final = m_si if u_q == "m³/s" else m_si / 15850.3

# --- INTERFAZ DE RESULTADOS ---
if st.button('🚀 Calcular y Generar Ecuación'):
    
    # Gráfica
    v_rango = np.linspace(0.1, 5.0, 50) # velocidad m/s
    q_rango_si = area_fisica * v_rango
    q_plot = q_rango_si if u_q == "m³/s" else q_rango_si * 15850.3
    v_plot = m_final * q_plot

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(q_plot, v_plot, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal ({u_q})')
    ax.set_ylabel(f'Voltaje ({u_v})')
    ax.grid(True, alpha=0.1)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown("#### Ecuación de Calibración Generada:")
    st.latex(rf"V_{{({u_v})}} = {m_final:.4f} \cdot Q_{{({u_q})}}")

    st.write("---")
    
    # --- CALCULADORA INTERACTIVA ---
    st.markdown("#### 💡 Calculadora Rápida")
    st.write("Usa la ecuación generada para hallar valores específicos:")
    
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        q_input = st.number_input(f"Ingresa Caudal ({u_q}) para hallar Voltaje:", value=0.0)
        v_res = m_final * q_input
        st.info(f"Voltaje Resultante: **{v_res:.4f} {u_v}**")

    with calc_col2:
        v_input = st.number_input(f"Ingresa Voltaje ({u_v}) para hallar Caudal:", value=0.0)
        q_res = v_input / m_final if m_final != 0 else 0
        st.success(f"Caudal Resultante: **{q_res:.4f} {u_q}**")

st.write("---")
st.caption(f"Simulador de Caudalímetro Electromagnético | Adriana Teixeira 2026 | Basado en Ley de Faraday")
