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

# 2. CSS Maestro Estilo "Imagen" (Borde Neón y Contenedor Compacto)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de pantalla completa sin márgenes blancos */
    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
            url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    /* TARJETA CENTRAL ESTILO IMAGEN */
    .main-card {
        background: rgba(15, 15, 15, 0.9); /* Negro muy oscuro */
        backdrop-filter: blur(10px);
        padding: 35px;
        border-radius: 20px;
        border: 2px solid #00d4ff; /* Borde Neón Cian */
        box-shadow: 0px 0px 20px rgba(0, 212, 255, 0.4);
        margin-top: 20px;
        color: white;
    }

    /* Título dentro de la tarjeta */
    .card-title {
        background: #111;
        padding: 15px;
        border-radius: 10px 10px 0 0;
        border-bottom: 1px solid #333;
        margin: -35px -35px 25px -35px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
    }

    /* Pantalla de carga compacta */
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
        width: 250px;
    }

    /* Botón estilo Neón */
    .stButton > button {
        width: 100%; 
        background-color: #00d4ff !important; 
        color: black !important;
        border: none; 
        border-radius: 10px; 
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        box-shadow: 0px 0px 15px #00d4ff;
        transform: scale(1.02);
    }

    .equation-container {
        background: rgba(0, 0, 0, 0.5); 
        border: 2px solid #00d4ff;
        border-radius: 12px; 
        padding: 20px; 
        margin: 20px 0; 
        text-align: center;
    }
    .equation-text { font-size: 1.8rem !important; color: #00d4ff; font-weight: 700; }

    /* Esconder headers de Streamlit */
    header[data-testid="stHeader"] { visibility: hidden; }
    [data-testid="stSidebar"] { background-color: rgba(0,0,0,0.8) !important; }
    p, label, h3 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ESTRUCTURA DE 1/3 ---
_, col_central, _ = st.columns([1, 1.2, 1])

with col_central:
    # Inicio de la tarjeta
    st.markdown("""
        <div class="main-card">
            <div class="card-title">Simulador de Caudalímetro Electromagnético</div>
    """, unsafe_allow_html=True)
    
    # --- 3. SELECCIÓN DE UNIDADES ---
    st.write("### ## Configuración")
    sistema = st.radio("Sistema de Unidades:", ("Métrico", "Americano"), horizontal=True)

    if sistema == "Métrico":
        u_b, u_sig, u_d, u_q = "T", "μS/cm", "m", "m³/s"
        b_min, b_max, b_def, sig_min, sig_max, sig_def, d_min, d_max, d_def, conv_q = 0.1, 1.5, 0.5, 1.0, 5000.0, 1000.0, 0.005, 0.500, 0.0127, 1.0
        val_dest, val_pot = "0.5 - 5", "50 - 800"
    else:
        u_b, u_sig, u_d, u_q = "G", "μmhos/in", "in", "GPM"
        b_min, b_max, b_def, sig_min, sig_max, sig_def, d_min, d_max, d_def, conv_q = 1000.0, 15000.0, 5000.0, 2.5, 12700.0, 2540.0, 0.2, 20.0, 0.5, 15850.3
        val_dest, val_pot = "1.27 - 12.7", "127 - 2032"

    st.write("---")

    # --- 5. PARÁMETROS ---
    st.markdown(f"**Campo Magnético B ({u_b})**")
    B_user = st.slider('B_slider', b_min, b_max, b_def, label_visibility="collapsed")

    st.markdown(f"**Conductividad σ ({u_sig})**")
    sigma_user = st.slider('Sig_slider', sig_min, sig_max, sig_def, label_visibility="collapsed")

    st.markdown(f"**Diámetro D ({u_d})**")
    D_user = st.slider('D_slider', d_min, d_max, d_def, label_visibility="collapsed")

    st.markdown(f"**Ajuste del Sistema (K)**")
    error_factor = st.slider('K_slider', 0.80, 1.20, 1.00, 0.01, label_visibility="collapsed")

    if 'generado' not in st.session_state:
        st.session_state.generado = False

    # --- 6. BOTÓN ---
    if st.button('🚀 Calcular Curva'):
        placeholder = st.empty()
        with placeholder.container():
            st.markdown(f"""
                <div class="loading-overlay">
                    <img src="{URL_GIF}" width="150">
                    <p style="color:#00d4ff; font-weight:bold; margin-top:10px;">Calculando...</p>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1.5)
        placeholder.empty()
            
        if sistema == "Americano":
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
        st.write("### 7 Resultados ---")
        fig, ax = plt.subplots(figsize=(6, 4))
        plt.style.use('dark_background')
        ax.plot(st.session_state.Q_plot, st.session_state.V_mv, color='#00d4ff', linewidth=2.5)
        ax.set_xlabel(f'Q ({u_q})', fontsize=9)
        ax.set_ylabel('V (mV)', fontsize=9)
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        st.pyplot(fig)

        st.markdown(f"""
            <div class="equation-container">
                <div class="equation-text">V = {st.session_state.m_eq:.4f} · Q</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("##")
    st.caption("Adriana Teixeira Mendoza - UCV 2026")
    st.markdown('</div>', unsafe_allow_html=True) # Cierre de main-card

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### Referencias Técnicas")
    st.info(f"Agua Destilada: {val_dest} {u_sig}")
    st.info(f"Agua Potable: {val_pot} {u_sig}")
