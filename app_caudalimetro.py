import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
import pandas as pd
from io import BytesIO
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

# --- LÓGICA DE UNIDADES (manteniendo columnas, sin GIF) ---
col_radio, col_gif = st.columns([3,1])

with col_radio:
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

    # CSS para evitar que el texto se vaya largo y cree scroll horizontal en tablas
    st.markdown("""
    <style>
    [data-testid="stTable"] table {
        width: 100% !important;
    }
    [data-testid="stTable"] td,
    [data-testid="stTable"] th {
        white-space: normal !important;
        word-break: break-word !important;
    }
    </style>
    """, unsafe_allow_html=True)

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
        st.markdown(f"""
        **Criterio técnico:** la conductividad eléctrica **σ** determina la amplitud de la señal inducida y la estabilidad del sistema.
        Para operación industrial se recomienda trabajar por encima de un umbral mínimo (depende del transmisor y del ruido),
        y considerar que σ varía con **temperatura, concentración iónica y composición del fluido**.  
        Unidades mostradas: **{u_sig}** (conversión automática según el sistema seleccionado).
        """)
        filas = []
        for fluido, (min_v, max_v) in conductividades.items():
            min_conv = min_v * conv_cond
            max_conv = max_v * conv_cond
            valor = f"{min_conv:.1f}" if min_v == max_v else f"{min_conv:.1f} – {max_conv:.1f}"
            filas.append({"Fluido": fluido, f"Conductividad ({u_sig})": valor})

        df_cond = pd.DataFrame(filas)
        st.table(df_cond)

        # “Más info” dentro del mismo bloque desplegable
        with st.expander("📌 Más información (criterio técnico)", expanded=False):
            st.markdown(f"""
**Importancia en caudalímetros electromagnéticos:**  
La conductividad del fluido condiciona la **calidad de la señal inducida** y, por tanto, la estabilidad de la medición.
En fluidos con conductividad baja aumenta la **incertidumbre** y el sistema puede requerir:
- Mayor **campo magnético B** o mejor electrónica de adquisición (SNR).
- Tratamiento de ruido y filtrado.
- Validación de un **umbral mínimo de σ** para garantizar repetibilidad.

Las magnitudes mostradas están en **{u_sig}** y se convierten automáticamente según el sistema seleccionado.
            """)

    # -------- DIÁMETROS --------
    diametros = {
        "DN15": 0.015,
        "DN25": 0.025,
        "DN50": 0.050,
        "DN100": 0.100,
        "DN200": 0.200,
        "DN500": 0.500,
    }

    with st.expander("🔵 Diámetros Nominales", expanded=False):
        st.markdown(f"""
        **Criterio técnico:** el diámetro interno **D** afecta el área (**A = π·D²/4**) y la relación señal–caudal.
        En caudalímetros electromagnéticos, la tendencia es **V ∝ B·D·v**: a mayor **D**, mayor señal inducida para igual B y v.
        La selección de DN también condiciona **pérdidas de carga**, rango de caudal y requisitos de instalación.
        Unidades mostradas: **{u_d}** (conversión automática).
        """)
        filas = []
        for dn, valor_m in diametros.items():
            valor_conv = valor_m * conv_diam
            filas.append({"DN": dn, f"Diámetro ({u_d})": f"{valor_conv:.4f}"})
        df_dn = pd.DataFrame(filas)
        st.table(df_dn)

        with st.expander("📌 Nota (uso en diseño)", expanded=False):
            st.markdown(f"""
En un caudalímetro electromagnético, el diámetro interno influye directamente en:
- Área transversal (**A = π·(D/2)²**) → cambia el caudal para una misma velocidad.
- Voltaje inducido (tendencia **V ∝ B·D·v**) → diámetros mayores elevan la señal inducida para igual B y v.
- Requisitos de instalación (tramos rectos, perturbaciones) y pérdidas de carga.
            """)

    # -------- VELOCIDADES (AHORA SÍ DENTRO DEL SIDEBAR) --------
    velocidades = {
        "Agua potable":      {"vmin": 1.0, "vmax": 3.0, "nota": "Rango típico para buena SNR y menor riesgo de sedimentación."},
        "Industria química": {"vmin": 1.0, "vmax": 5.0, "nota": "Variabilidad alta del proceso; validar compatibilidad de materiales."},
        "Lodos":             {"vmin": 0.5, "vmax": 2.0, "nota": "Se limita para reducir abrasión y depósitos; operación más estable."},
        "Alimentos":         {"vmin": 1.0, "vmax": 4.0, "nota": "Compromiso entre estabilidad de señal y criterios sanitarios."},
    }
    unidad_vel = "m/s" if sistema.startswith("Métrico") else "ft/s"

    with st.expander("🌊 Velocidades recomendadas (criterio técnico)", expanded=False):
        st.markdown("""
**Criterio técnico:** rangos orientativos para mantener señal estable, evitar ruido a baja velocidad
y reducir riesgos de sedimentación/abrasión. El valor final depende de instalación, régimen de flujo y proceso.
        """)

        filas = []
        for app, info in velocidades.items():
            vmin = info["vmin"] * conv_vel
            vmax = info["vmax"] * conv_vel
            filas.append({
                "Aplicación": app,
                f"v_min ({unidad_vel})": f"{vmin:.2f}",
                f"v_max ({unidad_vel})": f"{vmax:.2f}",
                "Observación": info["nota"],
            })
        df_vel = pd.DataFrame(filas)
        st.table(df_vel)

        with st.expander("📌 Más información (interpretación)", expanded=False):
            st.markdown("""
- **Velocidades muy bajas**: suelen empeorar la relación señal/ruido (SNR) y la repetibilidad.
- **Velocidades muy altas**: aumentan abrasión (si hay sólidos), esfuerzos mecánicos y desgaste.
- La instalación (codos, válvulas, bombas) puede introducir asimetrías de perfil → conviene validar en campo.
            """)
with st.expander("ℹ️ ¿Cómo funciona el simulador?", expanded=False):
    st.markdown(f"""
Este simulador modela la respuesta de un **caudalímetro electromagnético** a partir de variables de diseño y operación:

1. **Entrada de parámetros:** el usuario define el campo magnético **B**, la conductividad del fluido **σ** y el diámetro interno **D**.
2. **Barrido de velocidades:** se genera un conjunto de velocidades entre **v_min** y **v_max** para simular condiciones de operación.
3. **Cálculo de caudal:** se calcula el caudal por continuidad: **Q = A·v**, donde **A = π·(D/2)²**.
4. **Modelo de señal inducida:** se estima el voltaje inducido como:
   - Tendencia base: **V ∝ B·D·v**
   - Se incluye un factor **f(σ)** que representa la mejora de medición al aumentar la conductividad.
   - Se incorpora un **factor de error** para simular desviaciones sistemáticas.
5. **Ajuste lineal (calibración):** con los puntos simulados se ajusta una recta **V = m·Q + b** y se reporta **R²**.

**Salida del simulador:** curva V–Q, ecuación de calibración y tabla de puntos evaluados.
Unidades activas: **{sistema}**.
    """)


st.markdown(f"#### Configuración de Parámetros ({sistema})")

col1, col2, col3 = st.columns(3)

with col1:
    B_user = st.number_input(
        f"B: Campo Magnético ({u_b})",
        min_value=float(b_min),
        max_value=float(b_max),
        value=float(b_def),
        step=0.01 if sistema.startswith("Métrico") else 100.0,
        format="%.4f" if sistema.startswith("Métrico") else "%.1f",
        help="Campo aplicado por las bobinas. A mayor B, mayor voltaje inducido (mejor SNR), pero mayor consumo."
    )

with col2:
    sigma_user = st.number_input(
        f"σ: Conductividad ({u_sig})",
        min_value=float(sig_min),
        max_value=float(sig_max),
        value=float(sig_def),
        step=10.0 if sistema.startswith("Métrico") else 50.0,
        format="%.2f"
    )

with col3:
    D_user = st.number_input(
        f"D: Diámetro ({u_d})",
        min_value=float(d_min),
        max_value=float(d_max),
        value=float(d_def),
        step=0.001 if sistema.startswith("Métrico") else 0.01,
        format="%.4f"
    )




if "edit_error" not in st.session_state:
    st.session_state.edit_error = False

st.markdown("#### Factor de Error del Sistema")

c_err1, c_err2, c_err3 = st.columns([1.1, 1.6, 3.3])

with c_err1:
    st.session_state.edit_error = st.toggle("Ajustar", value=st.session_state.edit_error)

with c_err2:
    if st.session_state.edit_error:
        error_factor = st.number_input(
            "Error (factor)",
            min_value=0.80,
            max_value=1.20,
            value=1.00,
            step=0.01,
            format="%.2f",
            help="Factor multiplicativo para modelar errores sistemáticos de ganancia/calibración."
        )
    else:
        error_factor = 1.00

with c_err3:
    st.caption(f"Por defecto: **1.00** · En uso ahora: **{error_factor:.2f}**")
st.write("---")
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

    c1, c2 = st.columns(2)
    with c1:
        v_min = st.number_input(
            "v mínima (m/s)",
            min_value=0.0,
            max_value=20.0,
            value=0.1,
            step=0.1,
            format="%.2f",
        )

    with c2:
        v_max = st.number_input(
            "v máxima (m/s)",
            min_value=0.0,
            max_value=30.0,
            value=5.0,
            step=0.1,
            format="%.2f",
        )

    if v_max <= v_min:
        st.error("v máxima debe ser mayor que v mínima.")
        st.stop()

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

    df = pd.DataFrame({
        "v (m/s)": v,
        f"Q ({u_q})": Q_plot,
        "V (mV)": V_mv
    })

    # Ajuste lineal completo V = mQ + b
    coef = np.polyfit(Q_plot, V_mv, 1)
    m_eq = coef[0]
    b_eq = coef[1]

    # Línea extendida
    Q_line = np.linspace(Q_plot.min()*1.2, Q_plot.max()*1.2, 400)
    V_line = m_eq * Q_line + b_eq

    # Predicción usando la recta ajustada
    V_pred = m_eq * Q_plot + b_eq

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
            range=[-Q_plot.max()*1.2, Q_plot.max()*1.2],
            showgrid=True,
            zeroline=True,
            ticks="outside"
        ),
        yaxis=dict(
            title='Voltaje V (mV)',
            range=[-V_mv.max()*1.2, V_mv.max()*1.2],
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
        if st.button("Interactuar con la gráfica"):
            st.session_state.grafica_interactiva = not st.session_state.grafica_interactiva

    with col2:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"staticPlot": not st.session_state.grafica_interactiva}
        )

    st.markdown("""
    <style>
    /* Evita scroll horizontal en tablas */
    [data-testid="stTable"] table {
        width: 100% !important;
    }
    [data-testid="stTable"] td, 
    [data-testid="stTable"] th {
        white-space: normal !important;   /* wrap */
        word-break: break-word !important;
    }
    </style>
    """, unsafe_allow_html=True)
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

    st.markdown("### 🧮 Evaluar puntos con la ecuación de calibración")

    modo_eval = st.radio(
        "Selecciona qué deseas calcular:",
        (f"Calcular V a partir de Q ({u_q} → mV)", f"Calcular Q a partir de V (mV → {u_q})"),
        horizontal=True
    )

    cA, cB = st.columns([2, 3])

    with cA:
        if modo_eval.startswith("Calcular V"):
            Q_in = st.number_input(f"Ingrese Q ({u_q})", value=float(np.mean(Q_plot)), format="%.6f")
            V_out = m_eq * Q_in + b_eq
            st.success(f"Resultado: V = **{V_out:.4f} mV**")
        else:
            V_in = st.number_input("Ingrese V (mV)", value=float(np.mean(V_mv)), format="%.6f")
            if abs(m_eq) < 1e-12:
                st.error("No se puede despejar Q porque la pendiente m≈0.")
            else:
                Q_out = (V_in - b_eq) / m_eq
                st.success(f"Resultado: Q = **{Q_out:.6f} {u_q}**")

    with cB:
        st.info("""
    **Nota:** esta evaluación usa la ecuación lineal ajustada **V = m·Q + b**.
    Si el usuario trabaja fuera del rango simulado, el resultado es una extrapolación y puede no ser representativo.
        """)
    
    st.write(f"Coeficiente de determinación R² = {R2:.6f}")
    st.markdown("### 📌 Puntos evaluados")

    with st.expander("Mostrar tabla de puntos evaluados", expanded=False):
        st.table(df.head(30))  # sin pantalla completa
        st.caption("Mostrando 30 filas. Descarga CSV/Excel para ver todo.")

    

    def dataframe_to_excel_bytes(dataframe: pd.DataFrame) -> bytes:
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            dataframe.to_excel(writer, index=False, sheet_name="Datos")
        return output.getvalue()

    excel_bytes = dataframe_to_excel_bytes(df)
    st.download_button(
        label="📥 Descargar puntos (Excel)",
        data=excel_bytes,
        file_name="puntos_caudalimetro.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Descargar puntos (CSV)",
        data=csv_data,
        file_name="puntos_caudalimetro.csv",
        mime="text/csv"
    )
    st.write("---")
    st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")





