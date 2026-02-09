import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Código CSS ajustado: Fondo al ras de pantalla (full screen), contenedor negro menos opaco (0.5 para transparencia)
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/fotos-premium/hermosa-playa-nocturna-rocas-via-lactea_104785-856.jpg");  # URL de tu imagen
        background-size: cover;  # Cubre toda la pantalla
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-blend-mode: overlay;  # Mezcla para no saturar
        opacity: 0.8;  # Ajusta opacity para claridad
        display: flex;  # Para centrar contenido vertical/horizontal
        flex-direction: column;
        justify-content: center;  # Centra vertical
        align-items: center;  # Centra horizontal
        min-height: 100vh;  # Full height
    }
    .stApp > header { background-color: transparent; }  # Barra superior transparente
    .main-content {  # Clase para contenedor centrado
        width: 80%;  # Ancho del contenido central (ajusta)
        max-width: 800px;  # Máximo para no estirar
        padding: 20px;  # Espacio interno
        background-color: rgba(0, 0, 0, 0.5);  # Negro menos opaco (transparencia 50%)
        border-radius: 10px;  # Bordes redondeados
    }
    </style>
    """, unsafe_allow_html=True)

# Contenedor centrado para contenido
with st.container():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)  # Inicia contenedor

    # Título de la app
    st.title('Simulación Interactiva de Caudalímetro Electromagnético')

    # Sliders amigables para el usuario
    B = st.slider('Intensidad del Campo Magnético B (T)', min_value=0.1, max_value=1.0, value=0.5, step=0.1, help='Ajusta el valor de B, típico 0.5 T para imanes N35')
    sigma = st.slider('Conductividad del Fluido σ (µS/cm)', min_value=1, max_value=5000, value=1000, step=100, help='Conductividad típica: baja <5, media ~1000, alta >5000')
    D = st.slider('Diámetro Interno D (m)', min_value=0.005, max_value=0.02, value=0.0127, step=0.001, help='Diámetro de tubería PVC ½" ≈0.0127 m')

    # Función para factor de conductividad (sigmoide)
    def conductivity_factor(sigma, sigma_min=5, k=0.01):
        return 1 / (1 + np.exp(-k * (sigma - sigma_min))) 

    factor = conductivity_factor(sigma)

    # Botón para generar gráfica
    if st.button('Generar Gráfica V vs Q'):
        A = np.pi * (D / 2)**2
        v = np.linspace(0.1, 10, 100)
        V_theor = B * D * v * factor * 1000 # Resultado en mV
        Q = A * v # m³/s
        # Definir color según B
        if B < 0.4:
            color = 'red'
        elif B < 0.7:
            color = 'green'
        else:
            color = 'blue'
        fig, ax = plt.subplots()
        ax.plot(Q, V_theor, color=color)
        ax.set_xlabel('Caudal Q (m³/s)')
        ax.set_ylabel('Voltaje V (mV)')
        ax.set_title(f'V vs Q (B={B}T, σ={sigma}µS/cm, D={D}m)')
        ax.grid(True)
        # Mostrar gráfica en la app
        st.pyplot(fig)

    # Texto explicativo
    st.info('Ajusta los sliders y presiona el botón para ver la gráfica. El color cambia según B: rojo (bajo), verde (medio), azul (alto).')

    st.markdown("</div>", unsafe_allow_html=True)  # Cierra contenedor
