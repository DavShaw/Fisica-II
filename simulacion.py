import vpython as vpy

# Positions 
circle_position = vpy.vector(0,0,0)
center_position = vpy.vector(0,0,0)
sphere_position = vpy.vector(0,7,0)

# This is the main frame of the simulation
frame = vpy.canvas()

# My circle object
circle = vpy.cylinder(radius=10, color=vpy.color.red, pos = circle_position, length = 2)

# My sphere object
sphere = vpy.sphere(radius=1.6, color=vpy.color.blue, pos = sphere_position)

# My center object
center = vpy.sphere(radius=0.5, color=vpy.color.black, pos = center_position)

# My space color
frame.background = vpy.color.white

# Main loop
while True:
    vpy.rate(30)
    '''
    Esto sino lo doy para documentar en inglés:
    este método de la clase sphere lo que hace es permitir un movimiento circular al rededor de
    objeto referencial dado (en este caso un vector, que llame center_position).
    axis nos permite definir un vector, el cual sera el vector directo de este giro
    Por ultimo, angle, simplemente el angulo de rotación en radianes
    '''
    sphere.rotate(angle=vpy.radians(5), axis=vpy.vector(1,0,0), origin=center_position)
