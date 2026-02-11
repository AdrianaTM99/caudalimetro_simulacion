import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time 

# 1. Configuración de la página
st.set_page_config(
    layout="wide", 
    page_title="Simulador Adriana",
    page_icon="https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20v3.1.png"
)

# Enlace RAW
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS Maestro con Contenedor Central
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo general */
    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
            url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    /* BLOQUE CENTRAL NEGRO TRASLÚCIDO */
    .main-card {
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(15px);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        max-width: 800px;
        margin: 100px auto 40px auto; /* Centrado en PC */
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* Pantalla de carga */
    .loading-overlay {
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        text-align: center;
        background: rgba(0, 0, 0, 0.95);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #00d4ff;
        width: 280px;
    }
    .loading-overlay img { width: 180px; height: auto; }

    /* Header */
    .fixed-header {
        position: fixed; top: 0; left: 0; width: 100vw;
        background-color: rgba(0, 0, 0, 0.9); backdrop-filter: blur(10px);
        z-index: 999; border-bottom: 1px solid rgba(0, 212, 255, 0.3);
        display: flex; justify-content: center; height: 70px;
    }
    .fixed-header h1 { 
        font-size: 1.6rem !important; margin: auto; color: white !important; 
        font-family: 'Roboto', sans-serif; 
    }

    .equation-container {
        background: rgba(0, 212, 255, 0.1); border: 1px solid #00d4ff;
        border-radius: 15px; padding: 20px; margin: 20px 0;
        text-align: center;
    }
    .equation-text {
        font-size: 2.5rem !important; color: #00d4ff;
        font-family: 'Roboto', sans-serif; font-weight: 700;
    }

    /* Ajustes para móviles */
    @media (max-width: 768px) {
        .main-card { margin: 80px 15px 20px 15px; padding: 20px; }
        .equation-text { font-size: 1.5rem !important; }
        .fixed-header h1 { font-size: 1.1rem !important; padding: 0 10px; text-align: center; }
    }

    div[data-baseweb="radio"] div[aria-checked="true"] { background-color: #00d4ff !important; border-color: #00d4ff !important; }
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    .stButton > button {
        width: 100%; background-color: #1a5276 !important; color: white !important;
        border: 1px solid #00d4ff; border-radius: 8px; font-weight: bold; height: 3em;
    }

    header[data-testid="stHeader"] { visibility: hidden; }
    p, label { font-size: 1rem !important; color: white !important; }
    </style>

    <div class="fixed-header">
        <h1>Simulación de Caudalímetro Electromagnético</h1>
    </div>
    """, unsafe_allow_html=True)

# Inicio del bloque traslúcido
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# --- 3. SELECCIÓN DE UNIDADES ---
sistema = st.radio("Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

if sistema == "Métrico (T, μS/cm, m)":
    u_b, u_sig, u_d, u_q = "T", "μS/cm", "m", "m³/s"
    b_min, b_max, b_def, sig_min, sig_max, sig_def, d_min, d_max, d_def, conv_q = 0.1, 1.5, 0.5, 1.0, 5000.0, 1000.0, 0.005, 0.500, 0.0127, 1.0
else:
    u_b, u_sig, u_d, u_q = "G", "μmhos/in", "in", "GPM"
    b_min, b_max, b_def, sig_min, sig_max, sig_def, d_min, d_max, d_def, conv_q = 1000.0, 15000.0, 5000.0, 2.5, 12700.0, 2540.0, 0.2, 20.0, 0.5, 15850.3

st.write("---")

# --- 5. PARÁMETROS (Uno debajo del otro para PC) ---
st.markdown(f"#### Parámetros de Entrada")

B_val = st.number_input(f'Campo Magnético B ({u_b})', float(b_min), float(b_max), float(b_def))
B_user = st.slider('B_slider', float(b_min), float(b_max), float(B_val), label_visibility="collapsed")

sig_val = st.number_input(f'Conductividad σ ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
sigma_user = st.slider('Sig_slider', float(sig_min), float(sig_max), float(sig_val), label_visibility="collapsed")

D_val = st.number_input(f'Diámetro D ({u_d})', float(d_min), float(d_max), float(d_def), format="%.4f")
D_user = st.slider('D_slider', float(d_min), float(d_max), float(D_val), label_visibility="collapsed")

error_factor = st.slider('Factor de Ajuste (K)', 0.80, 1.20, 1.00, 0.01)

if 'generado' not in st.session_state:
    st.session_state.generado = False

# --- 6. PROCESAMIENTO ---
if st.button('🚀 Generar curva de calibración'):
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
            <div class="loading-overlay">
                <img src="{URL_GIF}">
                <p style="color:#00d4ff; font-weight:bold; margin-top:10px; font-size:0.9rem;">Calculando flujo...</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2.0)
    placeholder.empty()
        
    if sistema == "Americano (G, mhos/in, in)":
        B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
    else:
        B_si, D_si, sigma_si = B_user, D_user, sigma_user

    A_m2 = np.pi * (D_si / 2)**2
    v_vec = np.linspace(0.1, 5.0, 100)
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
    V_mv = (B_si * D_si * v_vec * f_cond * 1000) * error_factor
    Q_plot = (A_m2 * v_vec) * conv_q
    
    st.session_state.m_eq = V_mv[-1] / Q_plot[-1]
    st.session_state.Q_plot = Q_plot
    st.session_state.V_mv = V_mv
    st.session_state.generado = True

# --- 7. RESULTADOS ---
if st.session_state.generado:
    st.write("---")
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.style.use('dark_background')
    ax.plot(st.session_state.Q_plot, st.session_state.V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    ax.grid(True, alpha=0.1)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    

    st.markdown(f"""
        <div class="equation-container">
            <div class="equation-text">V = {st.session_state.m_eq:.4f} · Q</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background-color: rgba(26, 82, 118, 0.3); padding: 20px; border-radius: 12px; border: 1px solid #00d4ff;">', unsafe_allow_html=True)
    st.write("#### Calculadora de Predicción")
    q_in = st.number_input(f"Ingresar Caudal ({u_q}):", value=1.0, format="%.4f")
    st.write(f"**Voltaje Resultante: {q_in * st.session_state.m_eq:.4f} mV**")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("##")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")

# Cierre del bloque traslúcido
st.markdown('</div>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### Referencias Técnicas")
    with st.expander("📊 Ver Conductividades"):
        st.markdown(f"""
            <table style="width:100%; color:white; font-size:0.85rem;">
                <tr><th style="border-bottom:1px solid #00d4ff;">Fluido</th><th>{u_sig}</th></tr>
                <tr><td>Agua Destilada</td><td>{val_dest if 'val_dest' in locals() else '1.27-12.7'}</td></tr>
                <tr><td>Agua Potable</td><td>{val_pot if 'val_pot' in locals() else '127-2032'}</td></tr>
            </table>
        """, unsafe_allow_html=True)
