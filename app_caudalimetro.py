import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Pro Adriana")

# 2. CSS Maestro: Franja Negra con DESENFOQUE, PERSISTENCIA y TÍTULO IZQUIERDA
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de imagen base */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* CAPA NEGRA DESENFOCADA E INFINITA */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 1100px;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.45); 
        backdrop-filter: blur(8px);
        z-index: -1;
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

    h1 { font-size: 3rem !important; font-weight: 700 !important; text-align: left !important; margin-bottom: 0px !important; }
    h3 { font-size: 1.6rem !important; text-align: left !important; font-weight: 300 !important; margin-top: 0px !important; margin-bottom: 2rem !important; }
    h4 { margin-top: 20px; color: #00d4ff !important; }

    /* Sliders Azules */
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; border: 2px solid white !important; }

    /* Botones Azules */
    .stButton > button {
        width: 100%;
        background-color: #00d4ff;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.8rem;
        transition: 0.3s;
    }
    
    .stNumberInput div div input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }

    p, label, .stMarkdown { color: white !important; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE INTERFAZ ---

st.title('Simulación de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')

# 1. Selector de Sistema de Unidades Expandido
sistema = st.selectbox(
    "Selecciona el Sistema de Unidades de Trabajo:",
    ["Métrico (m, m³/s)", "Americano (in, GPM)", "Industrial (mm, L/min)"]
)

# Diccionario de configuración de unidades
# conv_D: relación con el metro | conv_Q: relación con m3/s
if sistema == "Métrico (m, m³/s)":
    u = {"D": "m", "Q": "m³/s", "V": "mV", "conv_D": 1.0, "conv_Q": 1.0}
    d_range = {"min": 0.01, "max": 1.0, "def": 0.05}
elif sistema == "Americano (in, GPM)":
    u = {"D": "in", "Q": "GPM", "V": "mV", "conv_D": 0.0254, "conv_Q": 15850.32}
    d_range = {"min": 0.25, "max": 40.0, "def": 2.0}
else: # Industrial
    u = {"D": "mm", "Q": "L/min", "V": "mV", "conv_D": 0.001, "conv_Q": 60000.0}
    d_range = {"min": 5.0, "max": 1000.0, "def": 50.0}

st.write("---")

# 2. Parámetros de Entrada
st.markdown(f"#### Configuración del Sensor ({sistema})")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B = st.slider('B: Campo Magnético (Tesla)', 0.1, 2.0, 0.5, 0.01)
with col2:
    sigma = st.slider('σ: Conductividad (μS/cm)', 5, 5000, 1000, 10)
with col3:
    D = st.slider(f'D: Diámetro del tubo ({u["D"]})', d_range["min"], d_range["max"], d_range["def"])

# 3. Factor de Error
if 'err_val' not in st.session_state: st.session_state.err_val = 1.0
with st.expander("Ajustes de Calibración (Factor de Error)"):
    st.session_state.err_val = st.slider("Ajuste manual del factor", 0.50, 1.50, st.session_state.err_val, 0.01)

# --- CÁLCULOS FÍSICOS ---
# 
# Convertimos todo a SI para la fórmula de Faraday: V = B * D * v
D_m = D * u["conv_D"]
area_m2 = np.pi * (D_m / 2)**2
f_cond = 1 / (1 + np.exp(-0.01 * (sigma - 5))) # Pérdida por conductividad

# Sensibilidad m en V = m * Q (usando m3/s)
# m = (B * D / Area) * 1000 (para mV)
sens_si = (B * D_m / area_m2) * f_cond * 1000 * st.session_state.err_val

# Ajustamos la sensibilidad al sistema de unidades seleccionado
# Si Q está en GPM, m debe ser: mV / GPM
m_final = sens_si / u["conv_Q"]

# 4. Resultados y Gráfica
if st.button('🚀 Calcular y Generar Análisis'):
    
    # Rango de caudal para graficar (basado en velocidad de hasta 4 m/s)
    q_max_si = 4.0 * area_m2 
    q_max_user = q_max_si * u["conv_Q"]
    q_rango = np.linspace(0, q_max_user, 100)
    v_rango = m_final * q_rango

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(q_rango, v_rango, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u["Q"]})')
    ax.set_ylabel(f'Voltaje V ({u["V"]})')
    ax.set_title(f'Curva de Calibración en {u["Q"]}', fontsize=14, pad=20)
    ax.grid(True, alpha=0.1)
    
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown("#### Ecuación de Calibración Resultante:")
    st.latex(rf"V_{{({u['V']})}} = {m_final:.6f} \cdot Q_{{({u['Q']})}}")

    st.write("---")
    
    # 5. Calculadora Interactiva
    st.markdown(f"#### 💡 Calculadora de Conversión Instantánea")
    st.info(f"Valores calculados para un tubo de {D} {u['D']} con B = {B} T")
    
    c1, c2 = st.columns(2)
    with c1:
        q_calc = st.number_input(f"Si el Caudal es ({u['Q']}):", value=0.0)
        st.write(f"➡️ Voltaje inducido: **{(q_calc * m_final):.4f} {u['V']}**")
    with c2:
        v_calc = st.number_input(f"Si el Voltaje es ({u['V']}):", value=0.0)
        q_res = (v_calc / m_final) if m_final != 0 else 0
        st.write(f"➡️ Caudal estimado: **{q_res:.4f} {u['Q']}**")

st.write("---")
st.caption(f"Simulador Adriana Teixeira 2026 | Sistema activo: {sistema}")
