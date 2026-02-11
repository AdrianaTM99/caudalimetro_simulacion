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

# 2. CSS Maestro para el bloque central de 1/3
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de pantalla completa */
    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
            url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    /* EL BLOQUE CENTRAL (Tarjeta) */
    .main-card {
        background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(0, 212, 255, 0.4);
        box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.8);
        margin-top: 20px;
    }

    /* Pantalla de carga centrada */
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
        width: 260px;
    }
    
    .fixed-header {
        position: fixed; top: 0; left: 0; width: 100vw;
        background-color: rgba(0, 0, 0, 0.9); backdrop-filter: blur(10px);
        z-index: 999; border-bottom: 1px solid rgba(0, 212, 255, 0.3);
        display: flex; justify-content: center; height: 60px;
    }
    .fixed-header h1 { font-size: 1.4rem !important; margin: auto; color: white !important; }

    .equation-container {
        background: rgba(0, 212, 255, 0.15); border: 1px solid #00d4ff;
        border-radius: 12px; padding: 15px; margin: 15px 0; text-align: center;
    }
    .equation-text { font-size: 2rem !important; color: #00d4ff; font-weight: 700; }

    /* Forzar que Streamlit no rellene los bordes */
    [data-testid="stHorizontalBlock"] { gap: 0rem; }
    
    header[data-testid="stHeader"] { visibility: hidden; }
    p, label { color: white !important; }
    </style>

    <div class="fixed-header">
        <h1>Simulación de Caudalímetro Electromagnético</h1>
    </div>
    """, unsafe_allow_html=True)

# --- CREACIÓN DE LA ESTRUCTURA DE 1/3 ---
# Creamos 3 columnas. La del medio será nuestra app.
espaciador_izq, col_central, espaciador_der = st.columns([1, 1.2, 1])

with col_central:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # --- 3. SELECCIÓN DE UNIDADES ---
    st.write("### Configuración")
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

    # --- 5. PARÁMETROS EN COLUMNA ---
    st.markdown(f"**Campo Magnético B ({u_b})**")
    B_user = st.slider('B_slider', b_min, b_max, b_def, label_visibility="collapsed")

    st.markdown(f"**Conductividad σ ({u_sig})**")
    sigma_user = st.slider('Sig_slider', sig_min, sig_max, sig_def, label_visibility="collapsed")

    st.markdown(f"**Diámetro D ({u_d})**")
    D_user = st.slider('D_slider', d_min, d_max, d_def, label_visibility="collapsed")

    error_factor = st.slider('Ajuste del Sistema (K)', 0.80, 1.20, 1.00, 0.01)

    if 'generado' not in st.session_state:
        st.session_state.generado = False

    # --- 6. PROCESAMIENTO ---
    if st.button('🚀 Calcular Curva'):
        placeholder = st.empty()
        with placeholder.container():
            st.markdown(f"""
                <div class="loading-overlay">
                    <img src="{URL_GIF}" width="150">
                    <p style="color:#00d4ff; font-weight:bold; margin-top:10px;">Procesando...</p>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1.5)
        placeholder.empty()
            
        # Cálculos
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
        st.write("---")
        fig, ax = plt.subplots(figsize=(6, 4))
        plt.style.use('dark_background')
        ax.plot(st.session_state.Q_plot, st.session_state.V_mv, color='#00d4ff', linewidth=2)
        ax.set_xlabel(f'Q ({u_q})', fontsize=8)
        ax.set_ylabel('V (mV)', fontsize=8)
        ax.tick_params(labelsize=7)
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        st.pyplot(fig)

        st.markdown(f"""
            <div class="equation-container">
                <div class="equation-text">V = {st.session_state.m_eq:.4f} · Q</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="background-color: rgba(26, 82, 118, 0.3); padding: 15px; border-radius: 10px; border: 1px solid #00d4ff;">', unsafe_allow_html=True)
        st.write("#### Predicción")
        q_in = st.number_input(f"Caudal ({u_q}):", value=1.0)
        st.write(f"**Voltaje: {q_in * st.session_state.m_eq:.4f} mV**")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("##")
    st.caption("Adriana Teixeira Mendoza - UCV 2026")
    st.markdown('</div>', unsafe_allow_html=True)

# --- SIDEBAR (Para no saturar el centro) ---
with st.sidebar:
    st.markdown("### Referencias Técnicas")
    st.info(f"Conductividad Agua Destilada: {val_dest} {u_sig}")
    st.info(f"Conductividad Agua Potable: {val_pot} {u_sig}")
