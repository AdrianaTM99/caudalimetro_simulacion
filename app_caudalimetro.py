import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="Simulador Adriana",
    initial_sidebar_state="collapsed"
)

# ENLACE RAW
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# =====================================================
# 🔹 CSS MAESTRO (BOTÓN VISIBLE + CENTRADO FIJO)
# =====================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* --- FONDO --- */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* --- CAPA OSCURA CENTRAL (CONTENEDOR) --- */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 50%; transform: translateX(-50%);
        width: 100%; max-width: 1150px; height: 100vh;
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(5px);
        z-index: 0;
    }

    /* --- SIDEBAR FLOTANTE (NO EMPUJA EL CONTENIDO) --- */
    section[data-testid="stSidebar"] {
        position: fixed !important;
        left: 0; top: 0; bottom: 0;
        width: 350px !important;
        background-color: rgba(0, 0, 0, 0.98) !important;
        border-right: 2px solid #00d4ff !important;
        z-index: 99999 !important; /* Muy alto, pero menos que el botón */
        transition: transform 0.3s ease-in-out;
    }

    /* --- EL BOTÓN DE DESPLIEGUE (LA SOLUCIÓN) --- */
    [data-testid="stSidebarCollapseButton"] {
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        z-index: 1000000 !important; /* ENCIMA DE TODO */
        color: #00d4ff !important;
        background-color: rgba(0,0,0,0.9) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        transition: all 0.3s ease;
        display: flex !important;
        align-items: center;
        justify-content: center;
    }

    [data-testid="stSidebarCollapseButton"]:hover {
        box-shadow: 0 0 10px #00d4ff;
        transform: scale(1.1);
    }

    /* --- EVITAR QUE EL CONTENIDO SE MUEVA --- */
    /* Aunque el sidebar se abra, el margen izquierdo se mantiene en 0 */
    [data-testid="stSidebar"][aria-expanded="true"] + section {
        margin-left: 0 !important;
    }

    /* --- CONTENIDO CENTRAL --- */
    .block-container {
        position: relative;
        z-index: 1;
        font-family: 'Roboto', sans-serif;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding-top: 130px !important; /* Espacio para el título */
        color: white !important;
    }

    /* --- HEADER FIJO --- */
    .fixed-header {
        position: fixed; top: 0; left: 0; width: 100%;
        height: 100px;
        z-index: 900; /* Menor que el sidebar y el botón */
        display: flex; justify-content: center; align-items: center;
        pointer-events: none;
    }

    .header-content {
        pointer-events: auto;
        width: 100%; max-width: 1100px;
        background-color: rgba(0, 0, 0, 0.9);
        padding: 15px; text-align: center;
        border-bottom: 2px solid #00d4ff;
        border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;
    }

    /* --- ESTILOS GENERALES --- */
    h1, h2, h3, p, label, .stMarkdown { color: white !important; }
    
    .equation-box {
        background: rgba(0, 0, 0, 0.5); border: 2px solid #00d4ff;
        border-radius: 15px; padding: 20px; text-align: center; margin-top: 20px;
    }
    
    .equation-large {
        font-size: 2.5rem !important; color: #00d4ff; font-weight: bold;
    }

    /* Overlay de carga */
    .loading-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.95); z-index: 999999;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }

    /* Ocultar header nativo de Streamlit */
    header[data-testid="stHeader"] { display: none !important; }

</style>

<div class="fixed-header">
    <div class="header-content">
        <h1 style="margin:0; font-family: 'Roboto'; font-size: 1.8rem; color: #00d4ff;">Simulación de Caudalímetro Electromagnético</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# CONTENIDO DE LA SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True) # Espacio para el botón
    st.markdown("<h2 style='color:#00d4ff;'>📘 Biblioteca Técnica</h2>", unsafe_allow_html=True)

    with st.expander("🔬 Conductividades (μS/cm)", expanded=True):
        st.markdown("""
        | Fluido | Valor |
        |---|---|
        | Agua destilada | 0.5 – 5 |
        | Agua potable | 50 – 1500 |
        | Agua de mar | 50,000 |
        | Leche | 4000 – 6000 |
        | Ácidos | 100,000 |
        """)

    with st.expander("🔵 Diámetros (DN)", expanded=True):
        st.markdown("""
        | DN | mm | Uso |
        |---|---|---|
        | DN15 | 15 | Lab |
        | DN50 | 50 | Agua |
        | DN200 | 200 | PTAR |
        """)

# =========================
# LÓGICA PRINCIPAL
# =========================

# --- UNIDADES ---
sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

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

# --- PARÁMETROS ---
st.markdown(f"#### Configuración de Parámetros ({sistema})")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    B_val = st.number_input(f'B: Campo Magnético ({u_b})', float(b_min), float(b_max), float(b_def))
    B_user = st.slider(f'Ajustar B', float(b_min), float(b_max), float(B_val), key="B_slider", label_visibility="collapsed")

with col2:
    sig_val = st.number_input(f'σ: Conductividad ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
    sigma_user = st.slider(f'Ajustar σ', float(sig_min), float(sig_max), float(sig_val), key="sig_slider", label_visibility="collapsed")

with col3:
    D_val = st.number_input(f'D: Diámetro ({u_d})', float(d_min), float(d_max), float(d_def), format="%.4f")
    D_user = st.slider(f'Ajustar D', float(d_min), float(d_max), float(D_val), key="D_slider", label_visibility="collapsed")

st.write("---")

# --- FACTOR DE ERROR ---
if 'edit_error' not in st.session_state:
    st.session_state.edit_error = False

c_err1, c_err2 = st.columns([1, 3]) 
with c_err1:
    if st.button('🔄 Factor de Error'):
        st.session_state.edit_error = not st.session_state.edit_error

with c_err2:
    error_factor = st.slider('Ajuste de Error (Factor K)', 0.80, 1.20, 1.00, 0.01) if st.session_state.edit_error else 1.00

# --- CÁLCULOS Y GRÁFICA ---
if sistema == "Americano (G, mhos/in, in)":
    B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
else:
    B_si, D_si, sigma_si = B_user, D_user, sigma_user

if st.button('🚀 Generar curva de calibración'):

    # Pantalla de carga
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
            <div class="loading-overlay">
                <img src="{URL_GIF}" width="450">
                <p style="color:#00d4ff; font-weight:bold; margin-top:10px; font-size:1.5rem;">
                Simulando Inducción Magnética...
                </p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
    placeholder.empty()

    # Ecuaciones
    A_m2 = np.pi * (D_si / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5))) # Factor de atenuación por conductividad
    
    # Ley de Faraday: V = B * D * v * k
    V_mv = (B_si * D_si * v * f_cond * 1000) * error_factor
    Q_plot = (A_m2 * v) * conv_q
    
    # Pendiente (m)
    m_eq = V_mv[-1] / Q_plot[-1] if Q_plot[-1] != 0 else 0

    # Gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje Inducido V (mV)')
    ax.grid(True, alpha=0.2, color="#00d4ff")
    
    # Fondo transparente para integración
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')

    st.pyplot(fig)

    # Resultado numérico
    st.markdown(f"""
        <div class="equation-box">
            <div class="equation-large">
                V = {m_eq:.4f} · Q
            </div>
            <p style="margin-top:10px; color:#ccc;">(Relación lineal característica del caudalímetro)</p>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
