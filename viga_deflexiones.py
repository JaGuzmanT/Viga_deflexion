import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# Limpiando la terminal 
os.system('cls')

# Configuración de la página
st.set_page_config(page_title="Calculadora de Deflexiones de Vigas",
				layout="wide",
				page_icon="🏗️",
				initial_sidebar_state="auto")


# Configuration del sidebar con logo e información de la empresa
with st.sidebar.container():
	# Mostrar el logo (usando manejo de errores para evitar problemas de codificación)
	try:
		st.image(image="Images/logo_siiia_w.png")
	except Exception as e:
		st.write("**INGENIERÍA ESTRUCTURAL**")
		st.info("Logo no disponible")
	
	# Información de la empresa
	st.title("INGENIERÍA ESTRUCTURAL")
	st.markdown("**Especialistas en análisis y diseño de estructuras**")
	st.divider()    
	st.markdown("### Acerca de Nosotros")
	st.markdown("### Servicios")
	st.markdown("✓ Cálculo de estructuras")
	st.markdown("✓ Diseño de elementos estructurales")
	st.markdown("✓ Análisis de deflexiones")
	st.markdown("✓ Consultoría técnica")
	st.divider()
	st.markdown("### Contacto")
	st.markdown("🌏 [siiia.com.mx](https://siiia.com.mx)")
	st.markdown("📧 contacto@siiia.com.mx")
	st.markdown("📱 +52 443 439 2310")

# Título y descripción
st.title(":green[Calculadora de Deflexiones de Vigas de Concreto] 🏗️")
st.markdown("Esta aplicación calcula las deflexiones de una viga de concreto doblemente apoyada bajo carga uniforme.")

# Crear dos columnas: una para entradas y otra para resultados
col1, col2 = st.columns([1, 1.5])

# Columna de entradas
with col1:
	st.subheader("Parámetros de Entrada")
	
	# Módulo de elasticidad (E)
	E = st.number_input(
		"Módulo de Elasticidad (E) en MPa",
		min_value=1000.0,
		max_value=50000.0,
		value=25000.0,
		step=1000.0,
		help="Módulo de elasticidad del concreto en MPa"
	)
	
	# Dimensiones de la viga
	st.subheader("Dimensiones de la Viga")
	b = st.number_input("Ancho (b) en cm", min_value=10.0, max_value=100.0, value=30.0, step=5.0)
	h = st.number_input("Altura (h) en cm", min_value=10.0, max_value=200.0, value=50.0, step=5.0)
	L = st.number_input("Longitud (L) en m", min_value=1.0, max_value=20.0, value=6.0, step=0.5)
	
	# Cálculo automático del momento de inercia o entrada manual
	calcular_I = st.checkbox("Calcular automáticamente el momento de inercia", value=True)
	
	if calcular_I:
		# Momento de inercia para sección rectangular: I = (b*h^3)/12
		I = (b * (h**3)) / 12  # en cm^4
		st.info(f"Momento de Inercia calculado: {I:.2f} cm⁴")
	else:
		I = st.number_input(
			"Momento de Inercia (I) en cm⁴",
			min_value=1000.0,
			max_value=100000000.0,
			value=312500.0,
			step=10000.0,
			help="Momento de inercia de la sección transversal"
		)
	
	# Carga uniforme
	q = st.number_input(
		"Carga Uniforme (q) en kN/m",
		min_value=0.1,
		max_value=100.0,
		value=10.0,
		step=0.5,
		help="Carga uniformemente distribuida a lo largo de la viga"
	)
	
	# Número de puntos para mostrar deflexiones
	num_puntos = st.number_input(
		"Número de puntos para mostrar deflexiones",
		min_value=3,
		max_value=20,
		value=5,
		step=1,
		help="Cantidad de puntos equidistantes para calcular y mostrar las deflexiones"
	)

# Columna de resultados y visualización
with col2:
	st.subheader("Resultados y Visualización")
	
	# Convertir unidades para cálculos
	E_Pa = E * 1e6  # Convertir MPa a Pa
	I_m4 = I * 1e-8  # Convertir cm^4 a m^4
	L_m = L  # Ya está en metros
	q_N_m = q * 1e3  # Convertir kN/m a N/m
	
	# Calcular deflexión máxima en el centro (para viga simplemente apoyada con carga uniforme)
	# Fórmula: y_max = (5*q*L^4)/(384*E*I) con signo negativo para indicar deflexión hacia abajo
	y_max = -1 * (5 * q_N_m * (L_m**4)) / (384 * E_Pa * I_m4)
	
	# Mostrar deflexión máxima (valor absoluto para la métrica, pero mantenemos el signo para cálculos)
	st.metric("Deflexión Máxima", f"{abs(y_max)*1000:.2f} mm")
	
	# Calcular deflexiones a lo largo de la viga
	x_points = np.linspace(0, L_m, 100)
	deflections = []
	
	for x in x_points:
		# Fórmula para deflexión en cualquier punto x de una viga simplemente apoyada con carga uniforme
		# y(x) = (q*x/(24*E*I)) * (L^3 - 2*L*x^2 + x^3) con signo negativo para indicar deflexión hacia abajo
		y = -1 * (q_N_m * x / (24 * E_Pa * I_m4)) * (L_m**3 - 2 * L_m * x**2 + x**3)
		deflections.append(y)
	
	# Escalar deflexiones para visualización
	scale_factor = 1  # Ajustar según sea necesario para visualización
	if max(deflections) > 0:
		scale_factor = L_m / (max(deflections) * 20)  # Escalar para que la deflexión máxima sea visible
	
	scaled_deflections = [d * scale_factor for d in deflections]
	
	# Crear gráfico
	fig, ax = plt.subplots(figsize=(10, 6))
	
	# Dibujar la viga sin deformar (línea recta)
	ax.plot([0, L_m], [0, 0], 'k--', alpha=0.5, label='Viga sin deformar')
	
	# Dibujar la viga deformada
	ax.plot(x_points, scaled_deflections, 'b-', linewidth=2, label='Viga deformada')
	
	# Dibujar los apoyos
	support_height = 0.1 * L_m / 10
	ax.add_patch(Rectangle((0, -support_height), 0.05 * L_m, support_height, color='gray'))
	ax.add_patch(Rectangle((L_m - 0.05 * L_m, -support_height), 0.05 * L_m, support_height, color='gray'))
	
	# Añadir flechas para representar la carga distribuida (apuntando hacia abajo)
	num_arrows = 10
	arrow_positions = np.linspace(0.1 * L_m, 0.9 * L_m, num_arrows)
	arrow_length = 0.1 * L_m / 5
	
	for pos in arrow_positions:
		ax.arrow(pos, arrow_length, 0, -arrow_length * 0.8, head_width=0.02 * L_m, 
				head_length=arrow_length * 0.2, fc='r', ec='r')
	
	# Configurar el gráfico (ajustando los límites para mostrar la deflexión hacia abajo)
	ax.set_xlim(-0.1 * L_m, 1.1 * L_m)
	# Invertimos los límites verticales para que la deflexión se muestre hacia abajo
	ax.set_ylim(min(scaled_deflections) * 1.2, arrow_length * 1.2)
	ax.set_xlabel('Posición a lo largo de la viga (m)')
	ax.set_ylabel('Deflexión (escala exagerada)')
	ax.set_title('Deflexión de la Viga')
	ax.grid(True, linestyle='--', alpha=0.7)
	ax.legend()
	
	# Mostrar el gráfico en Streamlit
	st.pyplot(fig)
	
	# Tabla de deflexiones en puntos específicos
	st.subheader("Deflexiones en Puntos Específicos")
	
	# Calcular deflexiones en puntos específicos según el número de puntos seleccionado por el usuario
	specific_points = np.linspace(0, L_m, num_puntos)
	specific_deflections = []
	
	for x in specific_points:
		if x == 0 or x == L_m:  # En los apoyos, la deflexión es cero
			y = 0
		else:
			# Misma fórmula que antes, con signo negativo para indicar deflexión hacia abajo
			y = -1 * (q_N_m * x / (24 * E_Pa * I_m4)) * (L_m**3 - 2 * L_m * x**2 + x**3)
		specific_deflections.append(y * 1000)  # Convertir a mm para mostrar
	
	# Crear un DataFrame para mostrar los resultados
	import pandas as pd
	df = pd.DataFrame({
		'Posición (m)': [f"{x:.2f}" for x in specific_points],
		'Deflexión (mm)': [f"{y:.3f}" for y in specific_deflections]
	})
	
	st.table(df)

# Información adicional
with st.expander("Información sobre las ecuaciones utilizadas"):
	st.markdown("### Ecuaciones para el cálculo de deflexiones")
	st.markdown("Para una viga simplemente apoyada con carga uniforme, las ecuaciones utilizadas son:")
	
	st.markdown("**Deflexión máxima** (en el centro de la viga):")
	st.latex(r"y_{max} = \frac{5qL^4}{384EI}")
	
	st.markdown("**Deflexión en cualquier punto x**:")
	st.latex(r"y(x) = \frac{q \cdot x}{24EI} (L^3 - 2Lx^2 + x^3)")
	
	st.markdown("Donde:")
	st.markdown(r"- $q$ = carga uniforme (N/m)")
	st.markdown(r"- $L$ = longitud de la viga (m)")
	st.markdown(r"- $E$ = módulo de elasticidad (Pa)")
	st.markdown(r"- $I$ = momento de inercia (m⁴)")
	st.markdown(r"- $x$ = posición a lo largo de la viga (m)")

# Pie de página
st.divider()
col1,col2,col3 = st.columns(3, vertical_alignment="center", gap="medium")
with col2:
	st.markdown("Made with ❤️ by [SIIIA MATH](https://www.siiia.com.mx)")
	st.caption("Calculadora de Deflexiones de Vigas de Concreto | Desarrollado por SIIIA MATH © 2025")