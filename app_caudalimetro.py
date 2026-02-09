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

    /* CAPA NEGRA DESENFOCADA E INFINITA (No se mueve al deslizar) */
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
        backdrop-filter: blur(8px); /* Desenfoque sutil */
        z-index: -1;
    }

    /* Limpieza de la interfaz de Streamlit */
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

    /* Estilos de Texto y Títulos a la Izquierda */
    h1 { font-size: 3rem !important; font-weight: 700 !important; text-align: left !important; margin-bottom: 0px !important; }
    h3 { font-size: 1.6rem !important; text-align: left !important; font-weight: 300 !important; margin-top: 0px !important; margin-bottom: 2rem !important; }
    h4 { margin-top: 20px; color: #00d4ff !important; }

    /* Sliders Azules Bonitos (#00D4FF) */
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
    .stButton > button:hover {
        background-color: #00bfff;
        box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.5);
    }
    
    /* Estilo para los inputs numéricos */
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

# 1. Selector de Sistema de Unidades
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (m, m³/s)", "Americano (in, GPM)"), horizontal=True)

# Configuración dinámica de unidades y factores
if sistema == "Métrico (m, m³/s)":
    u = {"D": "m", "Q": "m³/s", "V": "mV", "conv_Q": 1.0}
    d_vals = {"min": 0.005, "max": 0.5, "def": 0.0127}
else:
    u = {"D": "in", "Q": "GPM", "V": "mV", "conv_Q": 15850.3} # 1 m3/s = 15850.3 GPM
    d_vals = {"min": 0.2, "max": 20.0, "def": 0.5}

st.write("---")

# 2. Parámetros de Entrada con Sliders Azules
st.markdown(f"#### Parámetros de Configuración ({sistema})")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B = st.slider('B: Campo Magnético (Tesla)', 0.1, 1.5, 0.5, 0.01)
with col2:
    sigma = st.slider('σ: Conductividad (μS/cm)', 5, 5000, 1000, 10)
with col3:
    # Vinculamos el slider al sistema de unidades
    D = st.slider(f'D: Diámetro del tubo ({u["D"]})', d_vals["min"], d_vals["max"], d_vals["def"])

# 3. Factor de Error
if 'err_val' not in st.session_state: st.session_state.err_val = 1.0

with st.expander("Ajustes de Error (Factor de Corrección)"):
    c_e1, c_e2 = st.columns([3, 1])
    with c_e1:
        st.session_state.err_val = st.slider("Factor de error manual", 0.80, 1.20, st.session_state.err_val, 0.01)
    with c_e2:
        if st.button("Restablecer"):
            st.session_state.err_val = 1.0

# --- CÁLCULOS FÍSICOS (Ley de Faraday) ---
# 
# Convertimos D a metros para la física interna
D_m = D if u["D"] == "m" else D * 0.0254
area_m2 = np.pi * (D_m / 2)**2
# Factor de conductividad (pérdidas en fluidos poco conductivos)
f_cond = 1 / (1 + np.exp(-0.01 * (sigma - 5)))

# Pendiente en SI (Voltaje / m3/s)
# V = B * D * v -> v = Q/A -> V = (B * D / A) * Q
m_si = (B * D_m * (1/area_m2) * f_cond * 1000) * st.session_state.err_val

# Pendiente final ajustada al sistema (si es GPM, m_final será menor)
m_final = m_si / u["conv_Q"]

# 4. Resultados y Gráfica
if st.button('🚀 Generar Análisis y Curva de Calibración'):
    
    # Rango de caudal para graficar (basado en velocidad hasta 5 m/s)
    q_max_plot = 5.0 * area_m2 * u["conv_Q"]
    q_rango = np.linspace(0, q_max_plot, 100)
    v_rango = m_final * q_rango

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(q_rango, v_rango, color='#00d4ff', linewidth=3, label='Curva de Calibración')
    ax.set_xlabel(f'Caudal Q ({u["Q"]})', fontsize=11)
    ax.set_ylabel(f'Voltaje V ({u["V"]})', fontsize=11)
    ax.set_title('Respuesta del Sensor: Voltaje vs Caudal', fontsize=14, pad=20)
    ax.grid(True, alpha=0.1)
    
    # Estética de la gráfica
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown("#### Ecuación de Calibración:")
    st.latex(rf"V_{{({u['V']})}} = {m_final:.4f} \cdot Q_{{({u['Q']})}}")

    st.write("---")
    
    # 5. Calculadora Interactiva
    st.markdown(f"#### 💡 Calculadora Interactiva de Variables")
    st.info(f"Ingresa un valor para calcular automáticamente su contraparte usando la sensibilidad de {m_final:.4f}")
    
    c1, c2 = st.columns(2)
    
    with c1:
        q_calc = st.number_input(f"Dato de Caudal ({u['Q']}):", value=0.0, step=0.01)
        v_res = q_calc * m_final
        st.write(f"➡️ El Voltaje inducido es: **{v_res:.4f} {u['V']}**")

    with c2:
        v_calc = st.number_input(f"Dato de Voltaje ({u['V']}):", value=0.0, step=0.01)
        q_res = (v_calc / m_final) if m_final != 0 else 0
        st.write(f"➡️ El Caudal estimado es: **{q_res:.4f} {u['Q']}**")

st.write("---")
st.caption(f"Simulador de Caudalímetro Electromagnético | Adriana Teixeira Mendoza 2026 | Sistema: {sistema}")
