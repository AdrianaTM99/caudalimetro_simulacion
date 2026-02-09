import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(
    layout="centered", 
    page_title="Simulador Caudalímetro Adriana",
    page_icon="🌊"
)

# 2. CSS Avanzado: Fondo de Gaimport streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(
    layout="centered", 
    page_title="Simulador Caudalímetro Adriana",
    page_icon="🌊"
)

# 2. CSS para Fondo de Unsplash, Panel de Contraste y Sliders Azules
st.markdown("""
    <style>
    /* Imagen de fondo (Nueva URL de Unsplash) */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1580659986392-440ea995857c?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8bGF1dGFuJTIwbWFsYW18ZW58MHx8MHx8fDA%3D");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* EL PANEL DE CONTRASTE: Negro traslúcido con desenfoque */
    .main .block-container {
        max-width: 850px;
        padding: 3rem;
        background-color: rgba(0, 0, 0, 0.75); /* Negro ligeramente más denso para mejor contraste */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        backdrop-filter: blur(12px); /* Difumina el fondo para que las estrellas/olas no saturen */
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.9);
        margin-top: 40px;
        margin-bottom: 40px;
    }

    /* Forzar texto blanco nítido */
    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 1);
    }

    /* Sliders en color Azul */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: #ffffff !important;
    }

    /* Botón personalizado */
    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border: none;
        color: white;
        transform: scale(1.02);
    }

    /* Barra superior transparente */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO DEL PROGRAMA ---

st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")

# Parámetros de entrada
st.markdown("#### Ajuste de Variables del Sistema")
B = st.slider('Intensidad del Campo Magnético B (T)', 0.1, 1.0, 0.5, 0.1)
sigma = st.slider('Conductividad del Fluido σ (µS/cm)', 1, 5000, 1000, 100)
D = st.slider('Diámetro Interno D (m)', 0.005, 0.02, 0.0127, 0.001)

# Lógica del Factor de Conductividad
def conductivity_factor(sigma, sigma_min=5, k=0.01):
    return 1 / (1 + np.exp(-k * (sigma - sigma_min))) 

factor = conductivity_factor(sigma)

st.write("") # Espacio

# Acción y Gráfica
if st.button('🚀 Generar Simulación de Señal'):
    # Física del problema
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 10, 100) # m/s
    V_theor = B * D * v * factor * 1000 # mV (Ley de Faraday)
    Q = A * v # m³/s
    
    # Configuración visual de la gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Línea de la señal (Azul Cian Neón)
    ax.plot(Q, V_theor, color='#00e5ff', linewidth=3, label='Diferencia de Potencial')
    
    ax.set_xlabel('Caudal Volumétrico Q (m³/s)', fontsize=10)
    ax.set_ylabel('Voltaje Inducido V (mV)', fontsize=10)
    ax.set_title(f'Respuesta en Función del Caudal (B={B}T)', fontsize=12, pad=15)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    # Integración con el fondo del panel
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    st.pyplot(fig)
    
    st.success(f"Simulación lista. Factor de corrección por conductividad: {factor:.4f}")



st.markdown("---")
st.caption("Fórmula base: $V = B \cdot D \cdot v \cdot k$ | Basado en la Ley de Inducción de Faraday.")laxia, Panel Negro Traslúcido y Sliders Azules
st.markdown("""
    <style>
    /* Imagen de fondo total */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://img.freepik.com/foto-gratis/fondo-galaxia-estilo-fantasia_23-2151114299.jpg?semt=ais_hybrid&w=740&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* El panel central: Negro con 70% de opacidad y desenfoque (blur) */
    .main .block-container {
        max-width: 850px;
        padding: 3rem;
        background-color: rgba(0, 0, 0, 0.7); 
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        backdrop-filter: blur(10px); /* Esto evita que el fondo sature los datos */
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
        margin-top: 40px;
        margin-bottom: 40px;
    }

    /* Forzar texto blanco y legible */
    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8);
    }

    /* Cambio de Sliders de Naranja a Azul */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: #ff4b4b"] {
        background-color: #007bff !important;
    }
    
    div[role="slider"] {
        background-color: #007bff !important;
        border-color: #ffffff !important;
    }

    /* Estilo para el botón */
    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }

    /* Barra superior transparente */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIO DEL CONTENIDO DEL PROGRAMA ---

st.title('Simulación Interactiva de Caudalímetro Electromagnético')
st.markdown('### Por: Adriana Teixeira Mendoza')
st.write("---")

# Sección de entrada de datos
st.markdown("#### Parámetros de Configuración")
B = st.slider('Intensidad del Campo Magnético B (T)', min_value=0.1, max_value=1.0, value=0.5, step=0.1)
sigma = st.slider('Conductividad del Fluido σ (µS/cm)', min_value=1, max_value=5000, value=1000, step=100)
D = st.slider('Diámetro Interno D (m)', min_value=0.005, max_value=0.02, value=0.0127, step=0.001)

# Lógica Matemática
def conductivity_factor(sigma, sigma_min=5, k=0.01):
    # Factor de corrección sigmoide según conductividad
    return 1 / (1 + np.exp(-k * (sigma - sigma_min))) 

factor = conductivity_factor(sigma)

# Espaciado
st.write("")

# Botón y generación de resultados
if st.button('Generar Gráfica de Simulación V vs Q'):
    # Cálculos físicos
    A = np.pi * (D / 2)**2
    v = np.linspace(0.1, 10, 100) # Velocidad del fluido de 0.1 a 10 m/s
    V_theor = B * D * v * factor * 1000 # Voltaje inducido en mV
    Q = A * v # Caudal en m³/s
    
    # Configuración de la gráfica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Dibujar la línea (Color Cian neón para resaltar)
    ax.plot(Q, V_theor, color='#00d4ff', linewidth=3, label='Señal inducida (mV)')
    
    # Etiquetas y diseño
    ax.set_xlabel('Caudal Q (m³/s)', fontsize=10)
    ax.set_ylabel('Voltaje V (mV)', fontsize=10)
    ax.set_title(f'Respuesta Dinámica (B={B}T, D={D}m)', fontsize=12, pad=15)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    # Hacer el fondo de la imagen transparente para que se integre al panel negro
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    # Mostrar en Streamlit
    st.pyplot(fig)
    
    # Información adicional técnica
    st.success(f"Simulación completada. Factor de conductividad aplicado: {factor:.4f}")



st.markdown("---")
st.caption("Nota: Esta simulación utiliza la Ley de Faraday para calcular la diferencia de potencial inducida en el fluido conductor.")

