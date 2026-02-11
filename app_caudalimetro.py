import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página e Icono
st.set_page_config(
    layout="wide", 
    page_title="Simulador Adriana",
    page_icon="https://raw.githubusercontent.com/AdrianaTM99/caudalimetro_simulacion/main/ICONO_CAUDALIMETRO.png"
)

# 2. CSS Maestro (Control total de colores y posiciones)
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

    /* ELIMINAR NARANJA DE LOS WIDGETS (Radios y Toggles) */
    div[data-baseweb="radio"] div[aria-checked="true"] { background-color: #00d4ff !important; }
    div[data-testid="stWidgetLabel"] p { color: white !important; font-weight: bold !important; }
    
    /* Toggle (Interruptor) en azul */
    div[data-testid="stCheckbox"] div[data-baseweb="checkbox"] div { background-color: #1a5276 !important; }
    div[data-testid="stCheckbox"] div[aria-checked="true"] > div { background-color: #00d4ff !important; }

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

    .fixed-header h1 { font-size: 1.8rem !important; margin: 0; color: white !important; }

    .fixed-header h3 { 
        font-size: 1.1rem !important; margin: 0; color: white !important; 
        position: absolute; right: 2rem; font-weight: 300;
    }

    /* ECUACIÓN GIGANTE */
    .equation-container {
        background: rgba(0, 212, 255, 0.1);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 30px;
        margin: 40px auto;
        text-align: center;
        max-width: 800px;
    }

    .equation-text {
        font-size: 3.5rem !important;
        color: #00d4ff;
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }

    /* SLIDERS Y BOTONES */
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    .stButton > button {
        width: 100%; background-color: #1a5276 !important; color: white !important;
        border: 1px solid #00d4ff; border-radius: 8px;
    }

    header[data-testid="stHeader"] { visibility: hidden; }
    .stApp { background: transparent !important; }
    p, label { font-size: 1.1rem !important; color: white !important; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
            <h3>Por: Adriana Teixeira Mendoza</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. SELECCIÓN DE UNIDADES ---
st.write("##") # Espacio para el header
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

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### Referencias Técnicas")
    ver_tab = st.toggle("Ver Tabla de Conductividades")
    if ver_tab:
        st.markdown(f"""
            <table style="width:100%; color:white; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #00d4ff;"><th>Fluido</th><th>{u_sig}</th></tr>
                <tr><td>Agua Destilada</td><td>{val_dest}</td></tr>
                <tr><td>Agua Potable</td><td>{val_pot}</td></tr>
                <tr><td>Agua de Mar</td><td>{val_mar}</td></tr>
                <tr><td>Leche</td><td>{val_leche}</td></tr>
            </table>
        """, unsafe_allow_html=True)

# --- 5. PARÁMETROS ---
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    B_user = st.slider(f'B: Campo Magnético ({u_b})', float(b_min), float(b_max), float(b_def))
with col2:
    sigma_user = st.slider(f'σ: Conductividad ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
with col3:
    D_user = st.slider(f'D: Diámetro ({u_d})', float(d_min), float(d_max), float(d_def))

if st.button('🚀 Generar curva de calibración'):
    # Cálculos
    if sistema == "Americano (G, mhos/in, in)":
        B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
    else:
        B_si, D_si, sigma_si = B_user, D_user, sigma_user

    A_m2 = np.pi * (D_si / 2)**2
    v_vec = np.linspace(0.1, 5.0, 100)
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
    V_mv = (B_si * D_si * v_vec * f_cond * 1000)
    Q_plot = (A_m2 * v_vec) * conv_q
    m_eq = V_mv[-1] / Q_plot[-1]

    # Gráfico
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    # IMPRESIÓN DE LA ECUACIÓN GIGANTE
    st.markdown(f"""
        <div class="equation-container">
            <div class="equation-text">
                V<sub>(mV)</sub> = {m_eq:.4f} · Q<sub>({u_q})</sub>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Calculadora rápida
    st.markdown('<div style="background:rgba(26, 82, 118, 0.4); padding:20px; border-radius:10px; border:1px solid #00d4ff;">', unsafe_allow_html=True)
    val_q = st.number_input(f"Calcular Voltaje para Q ({u_q}):", value=1.0)
    st.write(f"### Voltaje Resultante: {val_q * m_eq:.4f} mV")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza 2026")
