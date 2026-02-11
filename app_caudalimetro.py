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


# ENLACE RAW CORREGIDO
URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

# 2. CSS Maestro con efecto de desenfoque SOLO en el centro

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

[data-testid="stAppViewContainer"] {
    background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
/* IMPORTAR FUENTE BONITA */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

/* TÍTULO PRINCIPAL */
/* BARRA SUPERIOR DEL TÍTULO */
.title-bar {
    position: fixed;
    top: 0;
    margin-top: 8px;
    left: 0;
    width: 100%;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(3px);
    -webkit-backdrop-filter: blur(3px);

    padding: 30px 0 20px 0;
    text-align: center;
    z-index: 1000;
    border-bottom: 2px solid #00d4ff;
}

/* TEXTO DEL TÍTULO */
.main-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00d4ff, #ff8c00

);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

/* SUBTÍTULO */
.subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: 1.1rem;
    color: #cccccc;
    margin-top: 5px;
}



/* RADIO BUTTON AZUL */
div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
    border: 2px solid #00d4ff !important;
    background-color: #000 !important;
}

div[data-testid="stRadio"] [aria-checked="true"] > div:first-child > div {
    background-color: #00d4ff !important;
}

/* SLIDER AZUL */
div[data-testid="stSlider"] > div > div > div > div {
    background-color: #00d4ff !important;
}

div[data-testid="stSlider"] [role="slider"] {
    background-color: #00d4ff !important;
    border: 2px solid white !important;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 70px;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 1150px;
    height: calc(100vh - 70px);
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(3px);
    -webkit-backdrop-filter: blur(3px);
    z-index: 0;
}

.block-container {
    position: relative;
    z-index: 1;
    font-family: 'Roboto', sans-serif;
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding: 200px 2rem 4rem 2rem !important;
    color: white !important;
}
/* RESPONSIVE TÍTULO */
@media (max-width: 900px) {
    .main-title {
        font-size: 1rem !important;
    }

    .subtitle {
        font-size:0.85rem !important;
    }

    .block-container {
        padding: 170px 1rem 3rem 1rem !important;
    }

    .title-bar {
        margin-top: 25px !important;
    }
}


</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-bar">
    <div class="main-title">
        Simulador de Caudalímetro Electromagnético
    </div>
    <div class="subtitle">
        Modelado y calibración digital de flujo industrial
    </div>
</div>
""", unsafe_allow_html=True)


# 🔵 ESTILO DE SIDEBAR DESPLEGABLE
st.markdown("""
<style>

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.6) !important;
    backdrop-filter: blur(3px) !important;
    -webkit-backdrop-filter: blur(3px) !important;

    border-right: 2px solid #00d4ff;
    position: fixed !important;

    /*BAJAMOS LA BARRA DEBAJO DEL HEADER */
    top: 70px !important;
    height: calc(100vh - 70px) !important;

    z-index: 998 !important;
}

/* CONTENIDO NO SE DESPLACE */
[data-testid="stAppViewContainer"] {
    margin-left: 0 !important;
}

/* BOTÓN SIEMPRE VISIBLE */
div[data-testid="collapsedControl"] {
    position: fixed !important;
    top: 18px !important;
    left: 18px !important;
    z-index: 1002 !important;
    background-color: rgba(0,0,0,0.9) !important;
    padding: 8px 12px !important;
    border-radius: 10px !important;
    border: 1px solid #00d4ff !important;
}

</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE UNIDADES ---
sistema = st.radio(
    "Selecciona el Sistema de Unidades:",
    ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"),
    horizontal=True
)

# Definimos conversiones
if sistema == "Métrico (T, μS/cm, m)":
    u_b, u_sig, u_d, u_q = "T", "μS/cm", "m", "m³/s"
    conv_cond = 1
    conv_diam = 1
    conv_vel = 1

    # Rangos métricos
    b_min, b_max, b_def = 0.1, 1.5, 0.5
    sig_min, sig_max, sig_def = 1.0, 5000.0, 1000.0
    d_min, d_max, d_def = 0.005, 0.500, 0.0127
    conv_q = 1.0

else:
    u_b, u_sig, u_d, u_q = "G", "μmhos/in", "in", "GPM"
    conv_cond = 2.54
    conv_diam = 1 / 25.4
    conv_vel = 3.28084

    # Rangos americanos
    b_min, b_max, b_def = 1000.0, 15000.0, 5000.0
    sig_min, sig_max, sig_def = 2.5, 12700.0, 2540.0
    d_min, d_max, d_def = 0.2, 20.0, 0.5
    conv_q = 15850.3



# ================================
# 📘 SIDEBAR DINÁMICA CON CONVERSIÓN
# ================================
with st.sidebar:

    st.markdown("## 📘 Biblioteca Técnica")

    # -------- CONDUCTIVIDADES --------
    conductividades = {
        "Agua destilada": (0.5, 5),
        "Agua potable": (50, 1500),
        "Agua de mar": (50000, 50000),
        "Leche": (4000, 6000),
        "Sangre": (7000, 7000),
        "Soluciones salinas": (10000, 80000),
        "Ácidos diluidos": (10000, 100000),
    }

    with st.expander("🔬 Conductividades de Fluidos Comunes", expanded=True):

        tabla = f"| Fluido | Conductividad ({u_sig}) |\n"
        tabla += "|---------|----------------|\n"

        for fluido, (min_v, max_v) in conductividades.items():
            min_conv = min_v * conv_cond
            max_conv = max_v * conv_cond

            if min_v == max_v:
                valor = f"{min_conv:.1f}"
            else:
                valor = f"{min_conv:.1f} – {max_conv:.1f}"

            tabla += f"| {fluido} | {valor} |\n"

        st.markdown(tabla)

    # -------- DIÁMETROS --------
    diametros = {
        "DN15": 15,
        "DN25": 25,
        "DN50": 50,
        "DN100": 100,
        "DN200": 200,
        "DN500": 500,
    }

    with st.expander("🔵 Diámetros Nominales", expanded=True):

        tabla = f"| DN | Diámetro ({u_d}) |\n"
        tabla += "|----|---------------|\n"

        for dn, valor_mm in diametros.items():
            valor_conv = valor_mm * conv_diam
            tabla += f"| {dn} | {valor_conv:.2f} |\n"

        st.markdown(tabla)

    # -------- VELOCIDADES --------
    velocidades = {
        "Agua potable": (1, 3),
        "Industria química": (1, 5),
        "Lodos": (0.5, 2),
        "Alimentos": (1, 4),
    }

    unidad_vel = "m/s" if sistema.startswith("Métrico") else "ft/s"

    with st.expander("🌊 Velocidades Recomendadas", expanded=True):

        tabla = f"| Aplicación | Velocidad Recomendada ({unidad_vel}) |\n"
        tabla += "|-------------|----------------------|\n"

        for app, (min_v, max_v) in velocidades.items():
            min_conv = min_v * conv_vel
            max_conv = max_v * conv_vel
            tabla += f"| {app} | {min_conv:.2f} – {max_conv:.2f} |\n"

        st.markdown(tabla)


# --- PARÁMETROS ---
st.markdown(f"#### Configuración de Parámetros ({sistema})")


B_val = st.number_input(f'B: Campo Magnético ({u_b})', float(b_min), float(b_max), float(b_def))
B_user = st.slider('Ajustar B', float(b_min), float(b_max), float(B_val), key="B_slider")

st.write("")

sig_val = st.number_input(f'σ: Conductividad ({u_sig})', float(sig_min), float(sig_max), float(sig_def))
sigma_user = st.slider('Ajustar σ', float(sig_min), float(sig_max), float(sig_val), key="sig_slider")

st.write("")

D_val = st.number_input(f'D: Diámetro ({u_d})', float(d_min), float(d_max), float(d_def), format="%.4f")
D_user = st.slider('Ajustar D', float(d_min), float(d_max), float(D_val), key="D_slider")


st.write("---")

if 'edit_error' not in st.session_state:
    st.session_state.edit_error = False

st.markdown("#### Factor de Error del Sistema")
c_err1, c_err2 = st.columns([1, 3]) 
with c_err1:
    if st.button('🔄 Cambiar Factor'):
        st.session_state.edit_error = not st.session_state.edit_error
with c_err2:
    error_factor = st.slider('Error', 0.80, 1.20, 1.00, 0.01) if st.session_state.edit_error else 1.00

# --- CÁLCULOS ---
if sistema == "Americano (G, mhos/in, in)":
    # Corregido: Usar B_user para B_si
    B_si, D_si, sigma_si = B_user / 10000.0, D_user * 0.0254, sigma_user / 2.54
else:
    B_si, D_si, sigma_si = B_user, D_user, sigma_user

if st.button('🚀 Generar curva de calibración'):
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
            <div class="loading-overlay">
                <img src="{URL_GIF}" width="450">
                <p style="color:#00d4ff; font-weight:bold; margin-top:10px; font-size:1.2rem;">Calculando flujo electromagnético...</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    placeholder.empty()

    A_m2 = np.pi * (D_si / 2)**2
    v = np.linspace(0.1, 5.0, 100)
    f_cond = 1 / (1 + np.exp(-0.01 * (sigma_si - 5)))
    V_mv = (B_si * D_si * v * f_cond * 1000) * error_factor
    Q_plot = (A_m2 * v) * conv_q
    m_eq = V_mv[-1] / Q_plot[-1]

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q_plot, V_mv, color='#00d4ff', linewidth=3)
    ax.set_xlabel(f'Caudal Q ({u_q})')
    ax.set_ylabel('Voltaje V (mV)')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    st.pyplot(fig)

    st.markdown(f"""
        <div class="equation-box">
            <div class="equation-large">
                V<sub>(mV)</sub> = {m_eq:.4f} · Q<sub>({u_q})</sub>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")























