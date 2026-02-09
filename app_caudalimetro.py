import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time # Necesario para controlar el tiempo de la animación

# 1. Configuración de la página con ICONO personalizado
st.set_page_config(
    layout="wide", 
    page_title="Simulador Adriana",
    page_icon="https://raw.githubusercontent.com/AdrianaTM99/caudalimetro_simulacion/main/ICONO_CAUDALIMETRO.png"
)

# Enlace RAW de tu animación GIF
URL_GIF = "https://raw.githubusercontent.com/AdrianaTM99/caudalimetro_simulacion/main/caudalimetro%20v3.1.png"

# 2. CSS Maestro (Control total de diseño)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* FONDO OSCURO 75% */
    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
            url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    /* ELIMINAR NARANJA (Forzar azul en Radio y Expander) */
    div[data-baseweb="radio"] div[aria-checked="true"] { background-color: #00d4ff !important; border-color: #00d4ff !important; }
    
    /* ENCABEZADO FIJO */
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

    /* ECUACIÓN GIGANTE */
    .equation-container {
        background: rgba(0, 212, 255, 0.1);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 30px;
        margin: 40px auto;
        text-align: center;
        max-width: 850px;
    }

    .equation-text {
        font-size: 3.5rem !important;
        color: #00d4ff;
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
    }

    /* BOTONES Y SLIDERS */
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    .stButton > button {
        width: 100%; background-color: #1a5276 !important; color: white !important;
        border: 1px solid #00d4ff; border-radius: 8px; font-weight: bold;
    }

    /* ESTILO DE TABLA */
    .sidebar-table {
        width: 100%; border-collapse: collapse; font-size: 0.9rem; color: white;
    }
    .sidebar-table th { color: #00d4ff; border-bottom: 1px solid #00d4ff; text-align: left; padding: 8px; }
    .sidebar-table td { padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); }

    header[data-testid="stHeader"] { visibility: hidden; }
    .stApp { background: transparent !important; }
    p, label { font-size: 1.1rem !important; color: white !important; }
    
    /* Centrar la animación */
    .stImage { display: flex; justify-content: center; margin: 20px 0; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
            <h3>Por: Adriana Teixeira Mendoza</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. SELECCIÓN DE UNIDADES ---
st.write("##") 
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

if sistema == "Métrico (T, μS/cm, m)":
    u_b, u_sig, u_d, u_q = "T", "μS/cm", "m", "m³/s"
    b_min, b_max, b_def = 0.1, 1.5, 0.5
    sig_min, sig_max, sig_def = 1.0, 5000.0, 1000.0
    d_min, d_max, d_def = 0.005, 0.500, 0.0127
    conv_q = 1.0
    val_dest, val_pot, val_mar, val_leche = "0.5 - 5", "50 - 800", "52,000", "4,000 - 6,000"
else:
    u_b, u_sig, u_d, u_q = "G", "μmhos/in", "in", "GPM"
    b_min, b_max, b_def = 1000.0, 15000.0, 5000.0
    sig_min, sig_max, sig_def = 2.5, 12700.0, 2540.0
    d_min, d_max, d_def = 0.2, 20.0, 0.5
    conv_q = 15850.3
    val_dest, val_pot, val_mar, val_leche = "1.27 - 12.7", "127 - 2032", "132,080", "10,160 - 15,240"

# --- 4. SIDEBAR CON TABLA DESPLEGABLE ---
with st.sidebar:
    st.markdown("### Referencias Técnicas")
    with st.expander("📊 Ver Tabla de Conductividades", expanded=False):
        st.markdown(f"""
            <table class="sidebar-table">
                <tr><th>Fluido</th><th>{u_sig}</th></tr>
                <tr><td>Agua Destilada</td><td>{val_dest}</td></tr>
                <tr><td>Agua Potable</td><td>{val_pot}</td></tr>
                <tr><td>Agua de Mar</td><td>{val_mar}</td></tr>
                <tr><td>Leche</td><td>{val_leche}</td></tr>
            </table>
        """, unsafe_allow_html=True)

st.write("---")

# --- 5. PARÁMETROS ---
st.markdown(f"#### Configuración de Parámetros ({sistema})")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B_val = st.number_input(f'B: Campo Magnético ({u_b})', float(b_min), float(b_max), float(b_def))
    B_user = st.slider(f'S_B', float(b_min), float(b_max), float(B_val), label_visibility="collapsed")
with col2:
    sig_val = st.number_input(f'σ: Conductividad ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
    sigma_user = st.slider(f'S_Sig', float(sig_min), float(sig_max), float(sig_val), label_visibility="collapsed")
with col3:
    D_val = st.number_input(f'D: Diámetro ({u_d})', float(d_min), float(d_max), float(d_def), format="%.4f")
    D_user = st.slider(f'S_D', float(d_min), float(d_max), float(D_val), label_visibility="collapsed")

error_factor = st.slider('Ajuste de Error del Sistema (K)', 0.80, 1.20, 1.00, 0.01)

if 'generado' not in st.session_state:
    st.session_state.generado = False

# --- 6. PROCESAMIENTO CON ANIMACIÓN ---
if st.button('🚀 Generar curva de calibración'):
    # Inicia el bloque de carga
    with st.spinner('Procesando datos del caudalímetro...'):
        # Muestra tu GIF centrado
        st.image(URL_GIF, width=250)
        
        # Simulamos un pequeño retraso para que la animación sea visible
        time.sleep(1.5)
        
        # Realizamos los cálculos mientras la animación está presente
        if sistema == "Americano (G, mhos/in, in)":
            B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
        else:
            B_si, D_si, sigma_si = B_user, D_user, sigma_user

        A_m2 = np.pi * (D_si / 2)**2
        v_vec = np.linspace(0.1, 5.0, 100)
        f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
        V_mv = (B_si * D_si * v_vec * f_cond * 1000) * error_factor
        Q_plot = (A_m2 * v_vec) * conv_q
        m_eq = V_mv[-1] / Q_plot[-1]
        
        # Guardamos en el estado de la sesión para mantener los resultados
        st.session_state.m_eq = m_eq
        st.session_state.Q_plot = Q_plot
        st.session_state.V_mv = V_mv
        st.session_state.generado = True

# --- 7. MOSTRAR RESULTADOS ---
if st.session_state.generado:
    m_eq = st.session_state.m_eq
    Q_plot = st.session_state.Q_plot
    V_mv = st.session_state.V_mv

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown(f"""
        <div class="equation-container">
            <div class="equation-text">
                V<sub>(mV)</sub> = {m_eq:.4f} · Q<sub>({u_q})</sub>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="calc-box">', unsafe_allow_html=True)
    st.markdown('<span class="calc-header-text">Calculadora de Predicción</span>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        q_input = st.number_input(f"Ingresa Caudal (Q) en {u_q}:", value=1.0, format="%.4f", key="q_in")
        st.write(f"**Resultado: {q_input * m_eq:.4f} mV**")
    with col_b:
        v_input = st.number_input(f"Ingresa Voltaje (V) en mV:", value=1.0, format="%.4f", key="v_in")
        st.write(f"**Resultado: {v_input / m_eq if m_eq != 0 else 0:.4f} {u_q}**")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza 2026")
