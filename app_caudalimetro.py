import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 1. El título grande
st.title('Simulación Interactiva de Caudalímetro Electromagnético')

# 2. El autor en texto normal (con negrita) o pequeño
st.markdown('**Por:** Adriana Teixeira Mendoza') 

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
    V_theor = B * D * v * factor * 1000  # Resultado en mV
    Q = A * v  # m³/s

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

