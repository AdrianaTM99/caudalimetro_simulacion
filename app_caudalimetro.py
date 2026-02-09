import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS Maestro (Encabezado fijo, botones opacos, radio buttons personalizados)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo base con sombreado central */
    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(to right, transparent 0%, transparent calc(50% - 550px), rgba(0,0,0,0.5) calc(50% - 550px), rgba(0,0,0,0.5) calc(50% + 550px), transparent calc(50% + 550px)),
            url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* RECUADRO FIJO DEL TÍTULO (MÁS DELGADO) */
    .fixed-header {
        position: fixed;
        top: 0; left: 0; width: 100vw;
        background-color: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(5px);
        z-index: 999;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: center;
    }

    .header-content {
        width: 100%;
        max-width: 1100px;
        padding: 8px 2rem; /* Franja delgada */
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    header[data-testid="stHeader"] { visibility: hidden; }
    .stApp { background: transparent !important; }

    .block-container {
        font-family: 'Roboto', sans-serif;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 80px 2rem 2rem 2rem !important;
        color: white !important;
    }

    .fixed-header h1 { font-size: 1.6rem !important; font-weight: 700 !important; margin: 0; color: white; }
    .fixed-header h3 { font-size: 1.0rem !important; font-weight: 300 !important; margin: 0; color: white; }

    /* RADIO BUTTONS (FONDO NEGRO, MARCA AZUL) */
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
        border: 2px solid #00d4ff !important;
        background-color: #000000 !important;
    }
    div[data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] > div:first-child > div {
        background-color: #00d4ff !important;
    }

    /* BOTONES AZUL COBALTO OPACO */
    .stButton > button {
        width: 100%;
        background-color: #1a5276 !important;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stButton > button:hover {
        background-color: #21618c !important;
        border-color: #00d4ff !important;
    }

    /* CUADROS DE RESULTADO */
    .stSuccess, .stInfo {
        background-color: rgba(26, 82, 118, 0.4) !important;
        color: white !important;
        border: 1px solid #00d4ff !important;
    }

    p, label { color: white !important; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
            <h3>Por: Adriana Teixeira Mendoza</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. SELECCIÓN DE UNIDADES ---
sistema = st.radio("Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

if sistema == "Métrico (T, μS/cm, m)":
    u_b, u_sig, u_d, u_q = "T", "μS/cm", "m", "m³/s"
    b_min, b_max, b_def = 0.1, 1.5, 0.5
    sig_min, sig_max, sig_def = 1.0, 5000.0, 1000.0
    d_min, d_max, d_def = 0.005, 0.500, 0.0127
    conv_q = 1.0
else:
    u_b, u_sig, u_d, u_q = "G", "μmhos/in", "in", "GPM"
    b_min, b_max, b_def = 1000.0, 15000.0, 5000.0
    sig_min, sig_max, sig_def = 2.5, 12700.0, 2540.0
    d_min, d_max, d_def = 0.2, 20.0, 0.5
    conv_q = 15850.3

st.write("---")

# --- 4. ENTRADA DE PARÁMETROS ---
st.markdown(f"#### Parámetros del Instrumento ({sistema})")
col1, col2, col3 = st.columns(3)
with col1:
    B_user = st.slider(f'B: Campo Magnético ({u_b})', float(b_min), float(b_max), float(b_def))
with col2:
    sigma_user = st.slider(f'σ: Conductividad ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
with col3:
    D_user = st.slider(f'D: Diámetro ({u_d})', float(d_min), float(d_max), float(d_def))

err_factor = st.slider('Ajuste Fino (Factor de Error)', 0.80, 1.20, 1.00, 0.01)

# --- 5. CÁLCULO DE LA ECUACIÓN ---
if sistema == "Americano (G, mhos/in, in)":
    B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
else:
    B_si, D_si, sigma_si = B_user, D_user, sigma_user

A_m2 = np.pi * (D_si / 2)**2
f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
m_eq = (B_si * D_si * f_cond * 1000 * err_factor) / (A_m2 * conv_q)

st.write("---")

# --- 6. CALCULADORA INTERACTIVA ---
st.markdown(f"#### 🧮 Calculadora de Punto de Operación")
calc_col1, calc_col2 = st.columns(2)

with calc_col1:
    q_in = st.number_input(f"Ingresa Caudal (Q) en {u_q}:", value=0.0, format="%.4f")
    v_out = q_in * m_eq
    st.success(f"Voltaje Predictivo: **{v_out:.4f} mV**")

with calc_col2:
    v_in = st.number_input(f"Ingresa Voltaje (V) en mV:", value=0.0, format="%.4f")
    q_out = v_in / m_eq if m_eq != 0 else 0
    st.info(f"Caudal Calculado: **{q_out:.4f} {u_q}**")

# --- 7. GRÁFICA DINÁMICA CON SEÑALIZACIÓN ---
st.write("### Gráfica de Calibración en Tiempo Real")

# Escalar la gráfica según la calculadora
val_q = q_in if q_in > 0 else q_out
val_v = v_out if q_in > 0 else v_in
lim_q = max(val_q, 1.0) * 1.3

q_plot = np.linspace(0, lim_q, 100)
v_plot = q_plot * m_eq



plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(q_plot, v_plot, color='#00d4ff', linewidth=2.5, label='Ecuación de Calibración')

# Dibujar punto y proyecciones si hay un valor ingresado
if val_q > 0:
    ax.scatter(val_q, val_v, color='#ff4b4b', s=120, zorder=5, label='Valor Ingresado')
    ax.axhline(val_v, color='white', linestyle='--', alpha=0.4)
    ax.axvline(val_q, color='white', linestyle='--', alpha=0.4)
    ax.annotate(f'({val_q:.2f}, {val_v:.2f}mV)', (val_q, val_v), xytext=(15, 5), 
                textcoords='offset points', color='#ff4b4b', fontweight='bold')

ax.set_xlabel(f'Caudal Q ({u_q})')
ax.set_ylabel('Voltaje V (mV)')
ax.legend()
ax.grid(True, alpha=0.1)
fig.patch.set_alpha(0.0)
ax.set_facecolor('none')
st.pyplot(fig)

st.latex(rf"V_{{(mV)}} = {m_eq:.4f} \cdot Q_{{({u_q})}}")

st.write("---")
st.caption("Adriana Teixeira Mendoza | Simulación Técnica 2026")
