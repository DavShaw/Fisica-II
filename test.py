import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Datos
E = 1e5  # Valor del campo eléctrico (N/C)
q = -1.6e-19  # Valor de la carga (Coulombs)
m = 9.11e-31  # Masa de la carga (kg)
x0, y0 = 5,5  # Coordenadas de origen de la carga (metros)
v0 = 0  # Velocidad inicial (m/s)

# Tiempo de simulación
t_max = 1e-8  # Tiempo total de simulación (s)
dt = 1e-11  # Paso de tiempo (s)
t = np.arange(0, t_max, dt)

# Aceleración constante
a = (q * E) / m

# Posición en cada punto de tiempo
x = x0 + v0 * t + 0.5 * a * t**2

# Crear la figura
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, t_max)
ax.set_ylim(0, max(x))
line, = ax.plot([], [], 'ro')

# Configurar el gráfico
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Posición (m)')
ax.set_title('Movimiento de una partícula cargada en un campo eléctrico')
ax.grid(True)

# Función de inicialización para la animación
def init():
    line.set_data([], [])
    return line,

# Función de actualización para la animación
def update(frame):
    line.set_data(t[:frame], x[:frame])
    return line,

# Crear la animación
ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=20)

plt.show()
