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

# 2. CSS Maestro Optimizado para Móvil (Responsive)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
            url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    /* Pantalla de carga compacta y adaptable */
    .loading-overlay {
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        text-align: center;
        background: rgba(0, 0, 0, 0.9);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #00d4ff;
        width: 280px; /* Ancho fijo para que no se deforme en móvil */
    }
    
    .loading-overlay img { width: 180px; height: auto; }

    /* Header fijo para PC */
    .fixed-header {
        position: fixed; top: 0; left: 0; width: 100vw;
        background-color: rgba(0, 0, 0, 0.9); backdrop-filter: blur(10px);
        z-index: 999; border-bottom: 1px solid rgba(0, 212, 255, 0.3);
        display: flex; justify-content: center; height: 80px;
    }

    .header-content {
        width: 100%; max-width: 1200px; display: flex; 
        align-items: center; justify-content: center; position: relative; height: 100%;
    }

    .fixed-header h1 { font-size: 1.8rem !important; margin: 0; color: white !important; font-family: 'Roboto', sans-serif; }
    .fixed-header h3 { 
        font-size: 1.1rem !important; margin: 0; color: white !important; 
        position: absolute; right: 2rem; top: 50%; transform: translateY(-50%);
        font-weight: 300;
    }

    .equation-container {
        background: rgba(0, 212, 255, 0.1); border: 2px solid #00d4ff;
        border-radius: 15px; padding: 25px; margin: 20px auto;
        text-align: center; max-width: 850px;
    }

    .equation-text {
        font-size: 3rem !important; color: #00d4ff;
        font-family: 'Roboto', sans-serif; font-weight: 700;
    }

    /* AJUSTES PARA DISPOSITIVOS MÓVILES */
    @media (max-width: 768px) {
        .fixed-header {
            position: relative !important; /* Deja de flotar para dar espacio */
            height: auto !important;
            padding: 20px 10px !important;
        }
        .header-content { flex-direction: column; }
        .fixed-header h3 { position: static !important; transform: none !important; margin-top: 10px !important; }
        .fixed-header h1 { font-size: 1.3rem !important; text-align: center; }
        
        .equation-text { font-size: 1.5rem !important; } /* Ecuación más pequeña en móvil */
        
        .loading-overlay { width: 70% !important; scale: 0.8; }
    }

    div[data-baseweb="radio"] div[aria-checked="true"] { background-color: #00d4ff !important; border-color: #00d4ff !important; }
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    .stButton > button {
        width: 100%; background-color: #1a5276 !important; color: white !important;
        border: 1px solid #00d4ff; border-radius: 8px; font-weight: bold;
    }

    header[data-testid="stHeader"] { visibility: hidden; }
    p, label { font-size: 1.1rem !important; color: white !important; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. SELECCIÓN DE UNIDADES ---
st.write("##") 
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

if sistema == "Métrico (T, μS/cm, m)":
    u_b, u_sig, u_d, u_q = "T", "μS/cm", "m", "m³/s"
    b_min, b_max, b_def, sig_min, sig_max, sig_def, d_min, d_max, d_def, conv_q = 0.1, 1.5, 0.5, 1.0, 5000.0, 1000.0, 0.005, 0.500, 0.0127, 1.0
    val_dest, val_pot, val_mar, val_leche = "0.5 - 5", "50 - 800", "52,000", "4,000 - 6,000"
else:
    u_b, u_sig, u_d, u_q = "G", "μmhos/in", "in", "GPM"
    b_min, b_max, b_def, sig_min, sig_max, sig_def, d_min, d_max, d_def, conv_q = 1000.0, 15000.0, 5000.0, 2.5, 12700.0, 2540.0, 0.2, 20.0, 0.5, 15850.3
    val_dest, val_pot, val_mar, val_leche = "1.27 - 12.7", "127 - 2032", "132,080", "10,160 - 15,240"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### Referencias Técnicas")
    with st.expander("📊 Ver Tabla de Conductividades", expanded=False):
        st.markdown(f"""
            <table style="width:100%; color:white; border-collapse:collapse; font-size:0.9rem;">
                <tr><th style="border-bottom:1px solid #00d4ff; text-align:left;">Fluido</th><th style="border-bottom:1px solid #00d4ff;">{u_sig}</th></tr>
                <tr><td>Agua Destilada</td><td>{val_dest}</td></tr>
                <tr><td>Agua Potable</td><td>{val_pot}</td></tr>
                <tr><td>Agua de Mar</td><td>{val_mar}</td></tr>
                <tr><td>Leche</td><td>{val_leche}</td></tr>
            </table>
        """, unsafe_allow_html=True)

st.write("---")

# --- 5. PARÁMETROS ---
st.markdown(f"#### Parámetros ({sistema})")
col1, col2, col3 = st.columns([1,1,1])

with col1:
    B_val = st.number_input(f'B ({u_b})', float(b_min), float(b_max), float(b_def))
    B_user = st.slider(f'S_B', float(b_min), float(b_max), float(B_val), label_visibility="collapsed")
with col2:
    sig_val = st.number_input(f'σ ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
    sigma_user = st.slider(f'S_Sig', float(sig_min), float(sig_max), float(sig_val), label_visibility="collapsed")
with col3:
    D_val = st.number_input(f'D ({u_d})', float(d_min), float(d_max), float(d_def), format="%.4f")
    D_user = st.slider(f'S_D', float(d_min), float(d_max), float(D_val), label_visibility="collapsed")

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
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.style.use('dark_background')
    ax.plot(st.session_state.Q_plot, st.session_state.V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    ax.grid(True, alpha=0.2)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown(f"""
        <div class="equation-container">
            <div class="equation-text">V<sub>(mV)</sub> = {st.session_state.m_eq:.4f} · Q</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background-color: rgba(26, 82, 118, 0.4); padding: 20px; border-radius: 12px; border: 1px solid #00d4ff;">', unsafe_allow_html=True)
    st.write("### Calculadora de Predicción")
    c_a, c_b = st.columns(2)
    with c_a:
        q_in = st.number_input(f"Q en {u_q}:", value=1.0, format="%.4f")
        st.write(f"**V = {q_in * st.session_state.m_eq:.4f} mV**")
    with c_b:
        v_in = st.number_input(f"V en mV:", value=1.0, format="%.4f")
        st.write(f"**Q = {v_in / st.session_state.m_eq if st.session_state.m_eq != 0 else 0:.4f} {u_q}**")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")


