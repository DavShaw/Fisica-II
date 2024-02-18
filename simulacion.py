import vpython as vpy

# Vectores de posición
circle_position = vpy.vector(10,-10,0)
center_position = vpy.vector(10,-10,0)
sphere_position = vpy.vector(10,-2,0)

# Frame principal 
frame = vpy.canvas()

# Circulo que contendra el circulito (fingiendo lo mismo del video)
circle = vpy.cylinder(radius=12, color=vpy.color.red, pos = circle_position, length = 2)

# Circulo que estara contenido en el otro circulo grande
sphere = vpy.sphere(radius=1.6, color=vpy.color.blue, pos = sphere_position)

# Circulo para simular visualmente un punto
center = vpy.sphere(radius=0.5, color=vpy.color.black, pos = center_position)

# Cambiar fondo a blanco
frame.background = vpy.color.white

#----------------------------------------------------------------

# Atributos del resorte y la esfera bajo de el
k = 1.0
m = 0.5
rest_length = 8.9
g = 9.8

# Configurar resorte
spring = vpy.helix(pos=vpy.vector(0, 0, 0), axis=vpy.vector(0, 1, 0), radius=0.5, coils=20, thickness=0.1)
ball = vpy.sphere(pos=vpy.vector(0, -rest_length, 0), radius=1.6, color=vpy.color.blue)

# Configurar esfera
ball.v = vpy.vector(0, 12, 0)
ball.p = ball.v * m
dt = 0.01


# Bucle principal
while True:
    vpy.rate(60)
    '''
    Esto sino lo doy para documentar en inglés:
    este método de la clase sphere lo que hace es permitir un movimiento circular al rededor de
    objeto referencial dado (en este caso un vector, que llame center_position).
    axis nos permite definir un vector, el cual sera el vector directo de este giro
    Por ultimo, angle, simplemente el angulo de rotación en radianes
    '''
    sphere.rotate(angle=vpy.radians(0.5), axis=vpy.vector(1,0,0), origin=center_position)

    # Animar resorte y esfera pegada a el

    spring.axis = ball.pos - spring.pos
    spring_force = -k * (vpy.mag(spring.axis) - rest_length) * vpy.norm(spring.axis)
    
    total_force = vpy.vector(0, -m * g, 0) + spring_force
    
    ball.p += total_force * dt
    ball.v = ball.p / m
    ball.pos += ball.v * dt