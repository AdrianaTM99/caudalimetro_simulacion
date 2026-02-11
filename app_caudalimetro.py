import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time  

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# ENLACE RAW CORREGIDO
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS Maestro (Reforzado)
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

    /* CAPA CENTRAL CON DESENFOQUE */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 1150px; 
        height: 100vh;
        background: rgba(0, 0, 0, 0.6); 
        backdrop-filter: blur(3px); 
        -webkit-backdrop-filter: blur(3px);
        z-index: 0;
    }

    /* Estilo para el Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.9) !important;
        border-right: 2px solid #00d4ff !important;
    }
    
    /* Hacer que el botón de cerrar de la barra lateral sea visible */
    [data-testid="stSidebarNav"] + div {
        color: #00d4ff !important;
    }

    .block-container {
        position: relative;
        z-index: 1;
        font-family: 'Roboto', sans-serif;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 80px 2rem 4rem 2rem !important;
        color: white !important;
    }

    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        background-color: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(10px);
        z-index: 999;
        border-bottom: 1px solid #00d4ff;
        display: flex;
        justify-content: center;
        height: 70px;
    }

    .header-content {
        width: 100%;
        max-width: 1100px;
        padding: 15px 2rem;
        text-align: center;
    }

    header[data-testid="stHeader"] { visibility: hidden; }
    .stApp { background: transparent !important; }

    .fixed-header h1 { font-size: 1.6rem !important; font-weight: 700 !important; margin: 0; color: white; }

    /* Botones personalizados */
    .stButton > button {
        width: 100%;
        background-color: #1a5276 !important;
        color: white !important;
        border: 1px solid #00d4ff !important;
    }

    p, label, .stMarkdown { font-size: 1.1rem !important; color: white !important; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTENIDO ---
fluidos = {
    "Agua Destilada": 0.5,
    "Agua Potable": 500,
    "Agua de Mar": 50000,
    "Leche": 5000,
    "Zumo de Frutas": 3000,
    "Ácido Sulfúrico (30%)": 700000
}

with st.sidebar:
    st.markdown("### 📋 Tabla de Conductividades")
    st.write("Valores de referencia para ajustar σ:")

# --- PANTALLA PRINCIPAL ---
col_btn, _ = st.columns([1, 2])
with col_btn:
    # Este botón ayuda a que el usuario sepa que existe una barra lateral
    if st.button("📋 Ver Tabla de Fluidos"):
        st.info("Desliza tu mouse hacia el borde izquierdo de la pantalla o busca la flecha arriba a la izquierda.")

sistema = st.radio("Selecciona el Sistema de Unidades:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

# Actualizar tabla del sidebar
with st.sidebar:
    if sistema == "Métrico (T, μS/cm, m)":
        unit = "μS/cm"
        tabla = {f: f"{v:,} {unit}" for f, v in fluidos.items()}
    else:
        unit = "μmhos/in"
        tabla = {f: f"{v * 2.54:,} {unit}" for f, v in fluidos.items()}
    st.table(list(tabla.items()))

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

if st.button('🚀 Generar curva de calibración'):
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
            <div style="position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); z-index:9999; text-align:center; background:rgba(0,0,0,0.9); padding:20px; border-radius:20px; border:2px solid #00d4ff;">
                <img src="{URL_GIF}" width="360">
                <p style="color:#00d4ff; font-weight:bold;">Simulando flujo...</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    placeholder.empty()

    A_m2 = np.pi * (D_user / 2)**2 if sistema == "Métrico (T, μS/cm, m)" else np.pi * ((D_user * 0.0254) / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    # Ecuación de Faraday simplificada V = B * D * v
    # En sistema americano convertimos unidades para el cálculo
    B_calc = B_user if sistema == "Métrico (T, μS/cm, m)" else B_user / 10000.0
    D_calc = D_user if sistema == "Métrico (T, μS/cm, m)" else D_user * 0.0254
    
    V_mv = (B_calc * D_calc * v * 1000) 
    Q_plot = (A_m2 * v) * conv_q

    fig, ax = plt.subplots(figsize=(10, 4))
    plt.style.use('dark_background')
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=2)
    ax.set_xlabel(f"Caudal ({u_q})")
    ax.set_ylabel("Voltaje (mV)")
    st.pyplot(fig)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
