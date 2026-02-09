import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS Maestro (Imagen de fondo 50% más oscura)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Imagen de fondo con superposición oscura del 50% */
    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), /* Capa negra al 50% */
            url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover; 
        background-position: center; 
        background-attachment: fixed;
    }

    /* Contenedor transparente */
    .block-container {
        font-family: 'Roboto', sans-serif; 
        max-width: 1200px !important; 
        margin: 0 auto !important; 
        padding: 100px 2rem 4rem 2rem !important;
        color: white !important;
        background-color: transparent;
    }

    .fixed-header {
        position: fixed; top: 0; left: 0; width: 100vw;
        background-color: rgba(0, 0, 0, 0.6); backdrop-filter: blur(8px);
        z-index: 999; border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex; justify-content: center;
    }

    .header-content {
        width: 100%; max-width: 1100px; padding: 10px 2rem;
        display: flex; justify-content: space-between; align-items: center;
    }

    header[data-testid="stHeader"] { visibility: hidden; }
    .stApp { background: transparent !important; }

    .fixed-header h1 { font-size: 1.8rem !important; margin: 0; color: white; }
    .fixed-header h3 { font-size: 1.1rem !important; margin: 0; color: white; }

    /* ESTILO DE SLIDERS CIAN */
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; border: 2px solid white !important; }

    /* Botones Azul Cobalto */
    .stButton > button {
        width: 100%; background-color: #1a5276 !important; color: white !important;
        border-radius: 8px; font-weight: bold; border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .calc-box {
        background-color: rgba(26, 82, 118, 0.4);
        padding: 25px; border-radius: 12px; border: 1px solid #00d4ff; 
        margin-top: 20px; max-width: 800px;
        backdrop-filter: blur(5px);
    }

    .calc-header-text {
        color: white; font-size: 1.6rem; font-weight: 700;
        margin-bottom: 15px; text-align: left; display: block;
    }

    p, label { font-size: 1.1rem !important; color: white !important; text-shadow: 1px 1px 2px black; }

    /* Estilo de Tabla en Sidebar */
    .sidebar-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
        margin-top: 15px;
    }
    .sidebar-table th { color: #00d4ff; border-bottom: 1px solid #00d4ff; text-align: left; padding: 8px; }
    .sidebar-table td { padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); color: white; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
            <h3>Por: Adriana Teixeira Mendoza</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. SELECCIÓN DE UNIDADES ---
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

# --- 4. SIDEBAR CON TABLA DINÁMICA ---
with st.sidebar:
    st.markdown("### Referencias Técnicas")
    ver_conductividades = st.toggle("Ver Conductividades Nominales")
    if ver_conductividades:
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

error_factor = st.slider('Ajuste de Error del Sistema', 0.80, 1.20, 1.00, 0.01)

if 'generado' not in st.session_state:
    st.session_state.generado = False

if st.button('🚀 Generar curva de calibración'):
    st.session_state.generado = True

# --- 6. RESULTADOS ---
if st.session_state.generado:
    # Lógica de cálculo (conversión a SI para el cálculo interno)
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

    # Placeholder para imagen si la tienes: 

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.latex(rf"V_{{(mV)}} = {m_eq:.4f} \cdot Q_{{({u_q})}}")

    st.markdown('<div class="calc-box">', unsafe_allow_html=True)
    st.markdown('<span class="calc-header-text">Calculadora de Predicción</span>', unsafe_allow_html=True)
    
    q_input = st.number_input(f"Ingresa Caudal (Q) en {u_q}:", value=0.0, format="%.4f", key="q_in")
    v_output = q_input * m_eq
    st.markdown(f"**Resultado: Voltaje (V) = {v_output:.4f} mV**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("---")
    
    v_input = st.number_input(f"Ingresa Voltaje (V) en mV:", value=0.0, format="%.4f", key="v_in")
    q_output = v_input / m_eq if m_eq != 0 else 0
    st.markdown(f"**Resultado: Caudal (Q) = {q_output:.4f} {u_q}**")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza 2026")
