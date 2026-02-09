import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Simulador Adriana")

# 2. CSS Maestro (Eliminación de fondo naranja y forzado de azul/negro)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Fondo de imagen base FIJO */
    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(
                to right, 
                transparent 0%, 
                transparent calc(50% - 550px), 
                rgba(0, 0, 0, 0.5) calc(50% - 550px), 
                rgba(0, 0, 0, 0.5) calc(50% + 550px), 
                transparent calc(50% + 550px), 
                transparent 100%
            ),
            url("https://static.vecteezy.com/system/resources/previews/003/586/335/non_2x/surface-of-the-sea-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* RECUADRO FIJO DE EXTREMO A EXTREMO */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        background-color: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(4px);
        z-index: 999;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: center;
    }

    .header-content {
        width: 100%;
        max-width: 1100px;
        padding: 10px 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    header[data-testid="stHeader"] { visibility: hidden; }
    .stApp { background: transparent !important; }

    .block-container {
        font-family: 'Roboto', sans-serif;
        max-width: 1100px !important;
        margin: 0 auto !important;
        padding: 100px 2rem 4rem 2rem !important;
        color: white !important;
    }

    .fixed-header h1 { font-size: 1.8rem !important; font-weight: 700 !important; margin: 0; color: white; }
    .fixed-header h3 { font-size: 1.1rem !important; font-weight: 300 !important; margin: 0; color: white; }

    /* --- ELIMINAR NARANJA Y PONER AZUL/NEGRO EN RADIO BUTTONS --- */
    /* Círculo base: fondo negro y borde azul */
    div[data-testid="stRadio"] [data-baseweb="radio"] div:first-child {
        background-color: black !important;
        border-color: #00d4ff !important;
    }
    
    /* Cuando está seleccionado: mantener fondo negro (no naranja) y punto azul */
    div[data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] div:first-child {
        background-color: black !important; 
        border-color: #00d4ff !important;
    }

    /* El punto pequeño interno: azul brillante */
    div[data-testid="stRadio"] [data-baseweb="radio"] div div {
        background-color: #00d4ff !important;
    }

    /* Hover: resaltar borde */
    div[data-testid="stRadio"] label:hover div:first-child {
        border-color: #ffffff !important;
    }

    /* Sliders y Botones */
    div[data-testid="stSlider"] > div > div > div > div { background-color: #00d4ff !important; }
    div[data-testid="stSlider"] [role="slider"] { background-color: #00d4ff !important; border: 2px solid white !important; }

    .stButton > button {
        width: 100%;
        background-color: #00d4ff;
        color: white;
        border-radius: 8px;
        padding: 1rem;
        font-size: 1.4rem;
        font-weight: bold;
        border: none;
    }

    p, label, .stMarkdown { font-size: 1.1rem !important; color: white !important; }
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <h1>Simulación de Caudalímetro Electromagnético</h1>
            <h3>Por: Adriana Teixeira Mendoza</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE UNIDADES COMPLETA ---
sistema = st.radio("Sistema de Unidades Global:", ("Métrico (T, μS/cm, m)", "Americano (G, mhos/in, in)"), horizontal=True)

if sistema == "Métrico (T, μS/cm, m)":
    u_b, u_sig, u_d, u_q = "T", "μS/cm", "m", "m³/s"
    b_min, b_max, b_def = 0.1, 1.5, 0.5
    sig_min, sig_max, sig_def = 1, 5000, 1000
    d_min, d_max, d_def = 0.005, 0.500, 0.0127
    conv_q = 1.0
else:
    u_b, u_sig, u_d, u_q = "G", "μmhos/in", "in", "GPM"
    b_min,
