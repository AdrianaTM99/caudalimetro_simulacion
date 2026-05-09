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
if "realismo_on" not in st.session_state:
    st.session_state.realismo_on = True
if "seed_ruido" not in st.session_state:
    st.session_state.seed_ruido = 1234
if "mostrar_ideal" not in st.session_state:
    st.session_state.mostrar_ideal = True
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

    # Limpia el placeholder antes de recargar
    splash.empty()

    st.session_state.splash_done = True
    st.rerun()



# Detectar si es pantalla pequeña (aprox móvil)
is_mobile = st.session_state.get("is_mobile", False)

# Inicializar estado de gráfica
if "grafica_interactiva" not in st.session_state:
    st.session_state.grafica_interactiva = False

if "mostrar_eval" not in st.session_state:
    st.session_state.mostrar_eval = False

# 2. CSS Maestro con efecto de desenfoque SOLO en el centro



st.markdown("""
<style>

/* Botones un poco más “premium” */
div.stButton > button {
    border: 1px solid rgba(0,212,255,0.65) !important;
    border-radius: 12px !important;
    padding: 0.6rem 0.9rem !important;
    font-weight: 700 !important;
}
div.stButton > button:hover {
    box-shadow: 0 0 12px rgba(0,212,255,0.25) !important;
    transform: translateY(-1px);
}
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
[data-testid="stAppViewContainer"] {
    background-image: url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
/* IMPORTANDO FUENTE BONITA */
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

/* FORZAR NÚMEROS EN BLANCO  */
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
/* AUMENTAR TEXTO CENTRAL (EXCEPTO TÍTULO)  */
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
    /* AUMENTAR TEXTO CENTRAL (EXCEPTO TÍTULO) */
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
/*AJUSTE GRÁFICA EN MÓVIL*/
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




# ESTILO DE SIDEBAR DESPLEGABLE
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

/* ECUACIÓN GRANDE Y CENTRADA */
.equation-box{
    display:flex;
    justify-content:center;
    align-items:center;
    margin: 18px 0 8px 0;
    padding: 18px 16px;
    border: 2px solid #00d4ff;
    border-radius: 14px;
    background: rgba(0,0,0,0.55);
    box-shadow: 0 0 18px rgba(0,212,255,0.20);
}

.equation-large{
    font-size: 2.2rem;
    font-weight: 800;
    text-align:center;
    line-height: 1.3;
}

@media (max-width: 900px){
  .equation-large{ font-size: 1.45rem; }
}

</style>
""", unsafe_allow_html=True)

with st.expander("ℹ️ ¿Cómo funciona el simulador?", expanded=False):
    st.markdown("""
Este simulador modela la respuesta de un **caudalímetro electromagnético** a partir de variables de diseño y operación:

1. Elija el sistema de unidades a trabajar.
2. Defina las variables de diseño: Campo magnético **B**, la conductividad del fluido **σ**,  el diámetro interno **D** y el rango de velocidades a estudiar.
3. **Barrido de velocidades:** se genera un conjunto de velocidades entre **v_min** y **v_max** (previamente elegidos) para simular condiciones de operación.
4. **Cálculo de caudal:** El simulador calcula el caudal por continuidad: **Q = A·v**, donde **A = π·(D/2)²**.
5. **Modelo de señal inducida:** Se estima el voltaje inducido como:
   - Tendencia base: **V ∝ B·D·v**
   - Se incluye un factor **f(σ)** que representa la mejora de medición al aumentar la conductividad.
   - Se incorpora un **factor de error** para simular desviaciones sistemáticas.
6. **Ajuste lineal (calibración):** Con los puntos simulados se ajusta una recta **V = m·Q + b** y se reporta **R²**.
Nota: Puede consultar la bibliuoteca tecnica para Más información sobre las variables de diseño (despliegue arriba a la izquierda para acceder)  

**Salida del simulador:** curva V–Q, ecuación de calibración y tabla de puntos evaluados.
**El sistema de unidades se selecciona en el siguiente bloque.**
    """)


# LÓGICA DE UNIDADES (manteniendo columnas, sin GIF)
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
    b_min, b_max, b_def = 0.01, 0.6, 0.1
    sig_min, sig_max, sig_def = 1.0, 5000.0, 1000.0
    d_min, d_max, d_def = 0.005, 0.500, 0.0127
    conv_q = 1.0
else:
    u_b, u_sig, u_d, u_q = "G", "μmhos/in", "in", "GPM"
    conv_cond = 2.54
    conv_diam = 39.3701
    conv_vel = 3.28084
    # Rangos americanos
    b_min, b_max, b_def = 1000.0, 15000.0, 5000.0
    sig_min, sig_max, sig_def = 2.5, 12700.0, 2540.0
    d_min, d_max, d_def = 0.2, 20.0, 0.5
    conv_q = 15850.3


# SIDEBAR DINÁMICA CON CONVERSIÓN

with st.sidebar:
    st.markdown("## Biblioteca Técnica")

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
    
    # CONDUCTIVIDADES 
    # SIEMPRE EN S/m 
    conductividades_SI = {
        "Agua destilada": (5e-6, 5e-5),
        "Agua potable": (5e-3, 0.15),
        "Agua de mar": (5.0, 5.0),
        "Leche": (0.4, 0.6),
        "Sangre": (0.7, 0.7),
        "Soluciones salinas": (1.0, 8.0),
        "Ácidos diluidos": (1.0, 10.0),
    }

    with st.expander("Conductividades de Fluidos Comunes", expanded=False):
        st.markdown(f"""
        Las magnitudes mostradas se convierten automáticamente según el sistema de unidades seleccionado. """)
        filas = []
        # FACTOR SEGÚN SISTEMA
        if sistema.startswith("Métrico"):
            factor_cond = 1e4        # S/m → μS/cm
        else:
            factor_cond = 25400      # S/m → μmhos/in
        
        for fluido, (min_v, max_v) in conductividades_SI.items():
            min_conv = min_v * factor_cond
            max_conv = max_v * factor_cond
            valor = f"{min_conv:.1f}" if min_v == max_v else f"{min_conv:.1f} – {max_conv:.1f}"
            filas.append({"Fluido": fluido, f"Conductividad ({u_sig})": valor})

        df_cond = pd.DataFrame(filas)
        st.table(df_cond)

        # “Más info” dentro del mismo bloque desplegable
        with st.expander("Más información", expanded=False):
            st.markdown(f"""

 La conductividad eléctrica **σ** determina la amplitud de la señal inducida y la estabilidad del sistema, influyendo en la eficiencia de la medicion""")

    # DIÁMETROS
    diametros = {
        "DN15": 0.015,
        "DN25": 0.025,
        "DN50": 0.050,
        "DN100": 0.100,
        "DN200": 0.200,
        "DN500": 0.500,
    }

    with st.expander("Diámetros Nominales", expanded=False):
        filas = []
        for dn, valor_m in diametros.items():
            valor_conv = valor_m * conv_diam
            filas.append({"DN": dn, f"Diámetro ({u_d})": f"{valor_conv:.4f}"})
        df_dn = pd.DataFrame(filas)
        st.table(df_dn)

        with st.expander("Más información", expanded=False):
            st.markdown(f"""
En un caudalímetro electromagnético, el diámetro interno influye directamente en:
- Área de seccion transversal (**A = π·(D/2)²**) → Cambia el caudal para una misma velocidad.
- Voltaje inducido (tendencia **V ∝ B·D·v**) → diámetros mayores elevan la señal inducida para igual B y v.
            """)

    # VELOCIDADES (AHORA SÍ DENTRO DEL SIDEBAR)
    velocidades = [
    {
        "aplicacion": "Agua potable",
        "D_min": 0.025,
        "D_max": 0.300,
        "v_min": 1.0,
        "v_max": 3.0,
        "nota": "Rango típico para evitar sedimentación y buena señal."
    },
    {
        "aplicacion": "Industria química",
        "D_min": 0.010,
        "D_max": 0.200,
        "v_min": 1.0,
        "v_max": 5.0,
        "nota": "Depende del proceso y materiales."
    },
    {
        "aplicacion": "Lodos",
        "D_min": 0.050,
        "D_max": 0.500,
        "v_min": 0.5,
        "v_max": 2.5,
        "nota": "Evitar abrasión y acumulación."
    },
    {
        "aplicacion": "Alimentos",
        "D_min": 0.015,
        "D_max": 0.150,
        "v_min": 1.0,
        "v_max": 4.0,
        "nota": "Compromiso entre higiene y medición."
    },
    ]
    unidad_vel = "m/s" if sistema.startswith("Métrico") else "ft/s"
    
    unidad_vel = "m/s" if sistema.startswith("Métrico") else "ft/s"
    unidad_d = u_d
    
    with st.expander("Velocidades recomendadas según diámetro", expanded=False):
    
        filas = []
    
        for item in velocidades:
            vmin = item["v_min"] * conv_vel
            vmax = item["v_max"] * conv_vel
    
            Dmin = item["D_min"] * conv_diam
            Dmax = item["D_max"] * conv_diam
    
            filas.append({
                "Aplicación": item["aplicacion"],
                f"D_min ({unidad_d})": f"{Dmin:.3f}",
                f"D_max ({unidad_d})": f"{Dmax:.3f}",
                f"v_min ({unidad_vel})": f"{vmin:.2f}",
                f"v_max ({unidad_vel})": f"{vmax:.2f}",
                "Observación": item["nota"],
            })
    
        df_vel = pd.DataFrame(filas)
        st.table(df_vel)
    
        with st.expander("Más información", expanded=False):
            st.markdown("""
        - **Velocidades muy bajas**: Suelen empeorar la relación señal/ruido (SNR) y la repetibilidad.
        - **Velocidades muy altas**: Aumentan abrasión (si hay sólidos), esfuerzos mecánicos y desgaste.
                    
                    """)
    st.markdown("---")


    with st.expander('información sobre el **modo realista**', expanded=False):
            st.markdown("""Una vez activado, este modo simula el comportamiento de un caudalímetro electromagnético *real* incluyendo efectos típicos de instrumentación y electrónica.
         **Modo de uso:**
        1. En el panel principal, active el **“Modo realista”**.
        2. Ajusta los parámetros (ruido, offset, deriva, no linealidad, cuantización, saturación e instalación).
        3. Pulsa **“Generar curva de calibración”** para recalcular.
        4. Si activas **“Mostrar curva ideal”**, verás dos curvas:
           - **Ideal**: modelo físico sin imperfecciones.
           - **Realista**: señal medida con errores y limitaciones.
        **Interpretación:**
        - Ruido/offset/deriva afectan el “cero” y la dispersión.
        - No linealidad introduce curvatura (la recta ya no ajusta perfecto).
        - Cuantización simula resolución ADC.
        - Saturación recorta la señal a un máximo.
        - Instalación simula errores por perfiles de flujo/tramos rectos.
                    
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
st.markdown("---")
with st.expander("Realismo del instrumento", expanded=False):
    st.session_state.realismo_on = st.toggle("Activar realismo", value=st.session_state.realismo_on)
    
    # Mostrar también la curva ideal para comparar
    st.session_state.mostrar_ideal = st.toggle("Mostrar curva ideal (comparación)", value=st.session_state.mostrar_ideal)
    
    ruido_mV = st.slider("Ruido base (mV RMS)", 0.0, 5.0, 0.15, 0.01)
    offset_mV = st.slider("Offset / cero (mV)", -5.0, 5.0, 0.10, 0.01)
    deriva_mV = st.slider("Deriva del cero en el barrido (mV)", 0.0, 5.0, 0.20, 0.01)
    
    alpha_nl = st.slider("No linealidad (α)", 0.0, 0.15, 0.02, 0.005)
    
    qstep_mV = st.select_slider(
        "Cuantización ADC (paso mV)",
        options=[0.0, 0.001, 0.005, 0.01, 0.02, 0.05],
        value=0.005
    )
    
    sat_mV = st.slider("Saturación |V| máx (mV)", 50.0, 2000.0, 800.0, 10.0)
    inst_pct = st.slider("Efecto instalación (±% lectura)", 0.0, 5.0, 0.5, 0.1)
    
# Guardamos para usarlos luego (fuera del sidebar también los necesitas)
st.session_state["ruido_mV"] = ruido_mV
st.session_state["offset_mV"] = offset_mV
st.session_state["deriva_mV"] = deriva_mV
st.session_state["alpha_nl"] = alpha_nl
st.session_state["qstep_mV"] = qstep_mV
st.session_state["sat_mV"] = sat_mV
st.session_state["inst_pct"] = inst_pct
with c_err3:
    st.caption(f"Por defecto: **1.00** · En uso ahora: **{error_factor:.2f}**")
st.write("---")
# CÁLCULOS
# CONVERSIÓN A SI (T, m, S/m) 
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

def aplicar_realismo(V_mv_ideal, Q_plot, sigma_si, seed,
                     ruido_mV, offset_mV, deriva_mV,
                     alpha_nl, qstep_mV, sat_mV, inst_pct):
    """
    Aplica efectos típicos de un caudalímetro (y su electrónica):
    - offset (cero), deriva lenta, instalación (ganancia), no-linealidad suave,
      ruido dependiente de conductividad, cuantización ADC y saturación.
    """
    rng = np.random.default_rng(int(seed))
    V = V_mv_ideal.copy()

    # 1) Offset (cero)
    V += offset_mV

    # 2) Deriva lenta (cambia el cero durante el barrido)
    V += np.linspace(0.0, deriva_mV, len(V))

    # 3) Instalación: error multiplicativo constante (perfil / swirl / tramos rectos)
    inst_factor = 1.0 + rng.uniform(-inst_pct, inst_pct) / 100.0
    V *= inst_factor

    # 4) No-linealidad suave (curvatura)
    Qmax = float(np.max(np.abs(Q_plot))) if np.max(np.abs(Q_plot)) > 0 else 1.0
    V *= (1.0 + alpha_nl * (Q_plot / Qmax) ** 2)

    # 5) Ruido: empeora si sigma es baja (peor SNR)
    sigma_ref = 0.02  # S/m (~200 μS/cm)
    penal = np.clip((sigma_ref / max(sigma_si, 1e-9)) ** 0.35, 1.0, 5.0)
    ruido_std = ruido_mV * penal
    V += rng.normal(0.0, ruido_std, size=len(V))

    # 6) Cuantización ADC
    if qstep_mV and qstep_mV > 0:
        V = np.round(V / qstep_mV) * qstep_mV

    # 7) Saturación
    V = np.clip(V, -sat_mV, sat_mV)

    return V

if st.session_state.mostrar_grafica:
  
    # CÁLCULOS
  
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

    # 1) Caudal
    Q_m3s = A_m2 * v
    Q_plot = Q_m3s if sistema.startswith("Métrico") else Q_m3s * 15850.3
    
    # 2) Voltaje ideal (modelo físico)
    V_mv_ideal = (B_si * D_si * v * f_cond * 1000) * error_factor
    
    # 3) Voltaje realista (si activado)
    if st.session_state.realismo_on:
        V_mv = aplicar_realismo(
            V_mv_ideal=V_mv_ideal,
            Q_plot=Q_plot,
            sigma_si=sigma_si,
            seed=st.session_state.seed_ruido,
            ruido_mV=st.session_state["ruido_mV"],
            offset_mV=st.session_state["offset_mV"],
            deriva_mV=st.session_state["deriva_mV"],
            alpha_nl=st.session_state["alpha_nl"],
            qstep_mV=st.session_state["qstep_mV"],
            sat_mV=st.session_state["sat_mV"],
            inst_pct=st.session_state["inst_pct"],
        )
    else:
        V_mv = V_mv_ideal

    # Etiqueta y conversión de velocidad para tabla
    u_v = "m/s" if sistema.startswith("Métrico") else "ft/s"
    v_tabla = v if sistema.startswith("Métrico") else v * 3.28084  # m/s -> ft/s
    
    df = pd.DataFrame({
        f"v ({u_v})": v_tabla,
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

   
    # GRÁFICA

    fig = go.Figure()

    # Datos realistas (los que usas para calibrar)
    fig.add_trace(go.Scatter(
        x=Q_plot,
        y=V_mv,
        mode='markers',
        name="Datos simulados (realista)"
    ))

    # Curva ideal (opcional comparación)
    if st.session_state.mostrar_ideal:
        fig.add_trace(go.Scatter(
            x=Q_plot,
            y=V_mv_ideal,
            mode='lines',
            name="Modelo ideal",
            line=dict(width=2, dash="dot")
        ))

    # Ajuste lineal sobre datos realistas
    coef = np.polyfit(Q_plot, V_mv, 1)
    m_eq = coef[0]
    b_eq = coef[1]

    Q_line = np.linspace(Q_plot.min()*1.2, Q_plot.max()*1.2, 400)
    V_line = m_eq * Q_line + b_eq

    fig.add_trace(go.Scatter(
        x=Q_line,
        y=V_line,
        mode='lines',
        line=dict(color='#00d4ff', width=4),
        name="Calibración lineal (ajuste)"
    ))

    fig.update_layout(
        template="plotly_dark",
        height=380,
        margin=dict(l=40, r=20, t=25, b=25),
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

    # BOTÓN DE INTERACCIÓN
   
    if st.button("🖱️ Interactuar / Fijar gráfica", use_container_width=True):
        st.session_state.grafica_interactiva = not st.session_state.grafica_interactiva

    estado = "Interactiva" if st.session_state.grafica_interactiva else "Estática"
    st.caption(f"Estado de gráfica: **{estado}**")

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"staticPlot": not st.session_state.grafica_interactiva}
    )

  
    # ECUACIÓN MOSTRADA
  
    st.markdown(f"""
    <div class="equation-box">
        <div class="equation-large">
            V<sub>(mV)</sub> = {m_eq:.4f} · Q<sub>({u_q})</sub> + {b_eq:.4f}
        </div>
    </div>
    """, unsafe_allow_html=True)

 
    # EVALUAR PUNTOS (toggle)
  
    col_btn, col_hint = st.columns([1.2, 3.8])
    with col_btn:
        if st.button("Evaluar puntos", use_container_width=True):
            st.session_state.mostrar_eval = not st.session_state.mostrar_eval
    with col_hint:
        st.caption("Despliega un panel para calcular V a partir de Q o Q a partir de V usando la ecuación ajustada.")

    if st.session_state.mostrar_eval:
        st.markdown("### Evaluación con ecuación de calibración")

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
**Nota:** Esta evaluación usa la ecuación lineal ajustada **V = m·Q + b**.
Si evalúas muy fuera del rango simulado, es extrapolación y puede no representar el comportamiento real del instrumento.
            """)

    st.caption(f"Calibración lineal: m = {m_eq:.4f} · b = {b_eq:.4f} · R² = {R2:.6f}")

    st.markdown("### Puntos evaluados")
    with st.expander("Mostrar tabla de puntos evaluados", expanded=False):
        st.table(df.head(30))
        st.caption("Mostrando 30 filas. Descarga CSV/Excel para ver todo.")

    

    def dataframe_to_excel_bytes(dataframe: pd.DataFrame) -> bytes:
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            dataframe.to_excel(writer, index=False, sheet_name="Datos")
        return output.getvalue()

    excel_bytes = dataframe_to_excel_bytes(df)
    st.download_button(
        label="Descargar puntos (Excel)",
        data=excel_bytes,
        file_name="puntos_caudalimetro.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar puntos (CSV)",
        data=csv_data,
        file_name="puntos_caudalimetro.csv",
        mime="text/csv"
    )
    st.write("---")
    st.caption("Adriana Teixeira Mendoza - Universidad Central de Venezuela - 2026")
























