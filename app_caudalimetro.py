import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time


# 1. Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="Simulador Adriana",
    initial_sidebar_state="collapsed"
)

URL_GIF = "https://github.com/AdrianaTM99/caudalimetro_simulacion/raw/main/caudalimetro%20con%20rayitas_3.gif"

if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if not st.session_state.splash_done:
    splash = st.empty()

    splash.markdown(f"""
    <style>
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: scale(0.95); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}
    </style>

    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: url('https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg');
        background-size: cover;
        background-position: center;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        z-index: 9999;
    ">
        <div style="text-align:center; animation: fadeIn 1.5s ease-in-out;">
            <img src="{URL_GIF}" style="width:320px; max-width:70vw; opacity:0.95;">
            <div style="margin-top:20px; font-size:1.3rem; color:white; font-family:'Poppins', sans-serif; letter-spacing:1px;">
                Inicializando simulador...
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(3)

    # 🔥 Limpia el placeholder antes de recargar
    splash.empty()

    st.session_state.splash_done = True
    st.rerun()



# Detectar si es pantalla pequeña (aprox móvil)
is_mobile = st.session_state.get("is_mobile", False)

# Inicializar estado de gráfica
if "grafica_interactiva" not in st.session_state:
    st.session_state.grafica_interactiva = False



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
    padding: 35px 0 10px 0;
    text-align: center;
    z-index: 1000;
    border-bottom: 2px solid #00d4ff;
}
/* TEXTO DEL TÍTULO */
.main-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00d4ff, #ff8c00 );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
/* SUBTÍTULO */
.subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: 1.5rem;
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
/* ===== FORZAR NÚMEROS EN BLANCO ===== */
div[data-testid="stNumberInput"] input,
div[data-testid="stNumberInput"] input[type="number"],
div[data-testid="stNumberInput"] input[type="text"] {
    color: white !important;
    -webkit-text-fill-color: white !important;
    caret-color: white !important;
    font-weight: 600 !important;
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
/* ===== AUMENTAR TEXTO CENTRAL (EXCEPTO TÍTULO) ===== */
.block-container p,
.block-container label,
.block-container div[data-testid="stMarkdownContainer"] p,
.block-container li,
.block-container span {
    font-size: 1.2rem !important;
}
/* RESPONSIVE TÍTULO */
@media (max-width: 900px) {
    .main-title {
        font-size: 1.2rem !important;
    }
    .subtitle {
        font-size:0.85rem !important;
    }
    .block-container {
        padding: 100px 1rem 3rem 1rem !important;
    }
    /* ===== AUMENTAR TEXTO CENTRAL (EXCEPTO TÍTULO) ===== */
    .block-container p,
    .block-container label,
    .block-container div[data-testid="stMarkdownContainer"] p,
    .block-container li,
    .block-container span {
        font-size: 1.2rem !important;
    }
    .title-bar {
        margin-top: 30px !important;
    }
}
/* ===== AJUSTE GRÁFICA EN MÓVIL ===== */
@media (max-width: 900px) {
    div[data-testid="stPlotlyChart"] {
        height: 320px !important;
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

# --- LÓGICA DE UNIDADES (sin GIF) ---
sistema = st.radio(
    "Selecciona el Sistema de Unidades:",
    ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"),
    horizontal=True
)

with col_gif:
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; align-items:center; height:100%;">
            <img src="{URL_GIF}" style="width:180px; opacity:0.95;">
        </div>
        """,
        unsafe_allow_html=True
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

    with st.expander("🔬 Conductividades de Fluidos Comunes", expanded=False):
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
        "DN15": 0.015,
        "DN25": 0.025,
        "DN50": 0.050,
        "DN100": 0.1,
        "DN200": 0.2,
        "DN500": 0.5,
    }

    with st.expander("🔵 Diámetros Nominales", expanded=False):
        tabla = f"| DN | Diámetro ({u_d}) |\n"
        tabla += "|----|---------------|\n"
        for dn, valor_mm in diametros.items():
            valor_conv = valor_mm * conv_diam
            tabla += f"| {dn} | {valor_conv:.3f} |\n"
        st.markdown(tabla)

    # -------- VELOCIDADES --------
    velocidades = {
        "Agua potable": (1, 3),
        "Industria química": (1, 5),
        "Lodos": (0.5, 2),
        "Alimentos": (1, 4),
    }
    unidad_vel = "m/s" if sistema.startswith("Métrico") else "ft/s"

    with st.expander("🌊 Velocidades Recomendadas", expanded=False):
        tabla = f"| Aplicación | Velocidad Recomendada ({unidad_vel}) |\n"
        tabla += "|-------------|----------------------|\n"
        for app, (min_v, max_v) in velocidades.items():
            min_conv = min_v * conv_vel
            max_conv = max_v * conv_vel
            tabla += f"| {app} | {min_conv:.2f} – {max_conv:.2f} |\n"
        st.markdown(tabla)

# --- PARÁMETROS ---
st.markdown(f"#### Configuración de Parámetros ({sistema})")

B_val = st.number_input(
    f'B: Campo Magnético ({u_b})',
    float(b_min), float(b_max), float(b_def)
)

B_user = st.slider(
    'Ajustar B',
    float(b_min), float(b_max), float(B_val),
    key="B_slider"
)

st.write("")

sig_val = st.number_input(
    f'σ: Conductividad ({u_sig})',
    float(sig_min), float(sig_max), float(sig_def)
)

sigma_user = st.slider(
    'Ajustar σ',
    float(sig_min), float(sig_max), float(sig_val),
    key="sig_slider"
)

st.write("")

D_val = st.number_input(
    f'D: Diámetro ({u_d})',
    float(d_min), float(d_max), float(d_def),
    format="%.4f"
)

D_user = st.slider(
    'Ajustar D',
    float(d_min), float(d_max), float(D_val),
    key="D_slider"
)

st.write("---")

if 'edit_error' not in st.session_state:
    st.session_state.edit_error = False

st.markdown("#### Factor de Error del Sistema")

c_err1, c_err2 = st.columns([1, 3])

with c_err1:
    if st.button('Cambiar Factor'):
        st.session_state.edit_error = not st.session_state.edit_error

with c_err2:
    error_factor = st.slider('Error', 0.80, 1.20, 1.00, 0.01) if st.session_state.edit_error else 1.00

# --- CÁLCULOS ---
# --- CONVERSIÓN A SI (T, m, S/m) ---
if sistema == "Americano (G, mhos/in, in)":
    # B: Gauss -> Tesla
    B_si = B_user * 1e-4
    # D: in -> m
    D_si = D_user * 0.0254
    # σ: (μmhos/in) == (μS/in) -> S/m
    # 1 μS/in = (1e-6 S) / (0.0254 m) = 3.937e-5 S/m
    sigma_si = sigma_user * 3.937e-5
else:
    # B ya en Tesla
    B_si = B_user
    # D ya en metros
    D_si = D_user
    # σ: μS/cm -> S/m  (1 μS/cm = 1e-4 S/m)
    sigma_si = sigma_user * 1e-4

if "mostrar_grafica" not in st.session_state:
    st.session_state.mostrar_grafica = False

if st.button('Generar curva de calibración'):
    st.session_state.mostrar_grafica = True

if st.session_state.mostrar_grafica:
    # =========================
    # CÁLCULOS
    # =========================
    A_m2 = np.pi * (D_si / 2)**2
    v_min = st.slider("v mínima (m/s)", 0.0, 5.0, 0.1, 0.1)
    v_max = st.slider("v máxima (m/s)", 0.1, 10.0, 5.0, 0.1)
    v = np.linspace(v_min, v_max, 100)
    def eficiencia_medicion_por_sigma(sigma_Sm: float, sigma_ref_Sm: float = 0.02, k: float = 6.0) -> float:
        sigma = max(sigma_Sm, 1e-9)
        x = np.log10(sigma / sigma_ref_Sm)
        return 1.0 / (1.0 + np.exp(-k * x))
    f_cond = eficiencia_medicion_por_sigma(sigma_si)
    st.caption(f"Factor por conductividad f(σ) = {f_cond:.4f}")
    V_mv = (B_si * D_si * v * f_cond * 1000) * error_factor
    Q_m3s = A_m2 * v  # SI puro
    Q_plot = Q_m3s if sistema.startswith("Métrico") else Q_m3s * 15850.3  # 1 m³/s = 15850.3 GPM

    # Ajuste lineal completo V = mQ + b
    coef = np.polyfit(Q_plot, V_mv, 1)
    m_eq = coef[0]
    b_eq = coef[1]

    # Línea extendida 
    Q_line = np.linspace(Q_plot.min()*1.2, Q_plot.max()*1.2, 400)
    V_line = m_eq * Q_line + b_eq

    # Predicción usando la recta ajustada
    V_pred = m_eq * Q_plot + b_eq  # si usas intercepto
    # si no usas intercepto: # V_pred = m_eq * Q_plot

    # Cálculo R²
    SS_res = np.sum((V_mv - V_pred)**2)
    SS_tot = np.sum((V_mv - np.mean(V_mv))**2)
    R2 = 1 - SS_res/SS_tot if SS_tot > 0 else 1.0

    # =========================
    # GRÁFICA
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=Q_plot,
        y=V_mv,
        mode='markers',
        name="Datos simulados"
    ))

    fig.add_trace(go.Scatter(
        x=Q_line,
        y=V_line,
        mode='lines',
        line=dict(color='#00d4ff', width=4),
        name="Curva de calibración",
        hovertemplate=
        'Caudal: %{x:.4f} ' + u_q + '<br>' +
        'Voltaje: %{y:.4f} mV<extra></extra>'
    ))

    fig.update_layout(
        template="plotly_dark",
        height=450,
        margin=dict(l=40, r=20, t=40, b=40),
        hovermode="x unified",
        uirevision=True,
        xaxis=dict(
            title=f'Caudal Q ({u_q})',
            range=[-Q_plot.max()*1.2, Q_plot.max()*1.2],  # 👈 zoom inicial controlado
            showgrid=True,
            zeroline=True,
            ticks="outside"
        ),
        yaxis=dict(
            title='Voltaje V (mV)',
            range=[-V_mv.max()*1.2, V_mv.max()*1.2],  # 👈 proporcional
            showgrid=True,
            zeroline=True,
            ticks="outside"
        )
    )

    # =========================
    # BOTÓN DE INTERACCIÓN
    # =========================
    col1, col2 = st.columns([1,4])

    with col1:
        if st.button("📱 Interacción"):
            st.session_state.grafica_interactiva = not st.session_state.grafica_interactiva

    with col2:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"staticPlot": not st.session_state.grafica_interactiva}
        )

    # =========================
    # ECUACIÓN MOSTRADA
    # =========================
    st.markdown(f"""
    <div class="equation-box">
        <div class="equation-large">
            V<sub>(mV)</sub> = {m_eq:.4f} · Q<sub>({u_q})</sub> + {b_eq:.4f}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write(f"Coeficiente de determinación R² = {R2:.6f}")
    st.write("---")
    st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")











