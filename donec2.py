import numpy as np
import random
import sympy as sp
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from depends import Charge, Vector, CoulombConverter


# Needed functions
def getForce(q,e):
  return abs(q)*e

def getAceleration(force, mass):
  return force/mass

def getVelocity(v0,a,t):
  return v0 + a*t

# I got some help from Claude3
def functionOf(textFunction, variable, evaluatefor):
    var = sp.symbols(variable)
    func = sp.sympify(textFunction)
    result = func.subs(var, evaluatefor)
    return result


# Limits for plot
xLimits, yLimits = (-15,15), (-15,15)

# Charge
charge = Charge((-1.6e-19), 0, 0)

# Interval
campInterval = (-10,10)
start, end = campInterval

# Negative - Positives plates
negativesLineY = [functionOf("3","x",i) for i in range(start, end)]
negativesLineX = [i for i in range(start, end)]

positivesLineY = [functionOf("-3","x",i) for i in range(start, end)]
positivesLineX = [i for i in range(start, end)]

# Data
E_x = 1e4
E_y = 1e4
m = 9.1e-31
v0_x = 0
v0_y = 0
interval = 10
position = (charge.getX(), charge.getY())

fig, ax = plt.subplots()

# Set limits
ax.set_xlim(xLimits)
ax.set_ylim(yLimits)

# Graph plates
ax.plot(negativesLineX, negativesLineY)
ax.plot(positivesLineX, positivesLineY)

# Graph point (Charge)
point = ax.scatter(charge.getX(), charge.getY())

# Graph vector (Force vector) [*ChatGPT help us with it*]
vector = ax.quiver(charge.getX(), charge.getY(), 0, 0, angles='xy', scale_units='xy', scale=1, color='r')

proj_x = ax.plot([], [], 'g--')[0]
proj_y = ax.plot([], [], 'b--')[0]

# Graph text
posText = ax.text(0.05, 0.95, '', transform=ax.transAxes, ha='left', fontsize=10)
acelerationText = ax.text(0.05, 0.90, '', transform=ax.transAxes, ha='left', fontsize=10)
velocityText = ax.text(0.05, 0.85, '', transform=ax.transAxes, ha='left', fontsize=10)

def animate(frame):
  global E_x, E_y, m, v0_x, v0_y, interval, position, posText, acelerationText, velocityText
  time = (frame * interval) / 1000

  # Get force
  force_x, force_y = getForce(charge.getValue(), E_x), getForce(charge.getValue(), E_y)

  # Get aceleration
  acceleration_x, acceleration_y = force_x / m, force_y / m
  acelerationText.set_text(f"(ax,ay) = ({acceleration_x},{acceleration_y})")

  # Get velocity
  v_x, v_y = getVelocity(v0_x, acceleration_x, time), getVelocity(v0_y, acceleration_y, time)
  velocityText.set_text(f"(vy,vy) = ({v_x},{v_y})")

  # Get position
  x = position[0] + (v0_x * time) + (0.5 * acceleration_x * (time ** 2))
  y = position[1] + (v0_y * time) + (0.5 * acceleration_y * (time ** 2))
  posText.set_text(f"(x,y) = ({x},{y})")

  # Scalar for make the simulation
  scalar = 1e15

  fx, fy = x/scalar, y/scalar

  # Update point (charge) and vector
  point.set_offsets((fx, fy))
  vector.set_offsets((fx, fy))
  vector.set_UVC(v_x/scalar, v_y/scalar)

  # ChatGPT help us with it
  proj_x.set_data([fx, fx + (v_x/scalar)], [fy, fy])
  proj_y.set_data([fx, fx], [fy, fy + (v_y/scalar)])
  

  return point, vector, proj_x, proj_y, acelerationText, velocityText, posText


ani = animation.FuncAnimation(fig, animate, frames=500*5, interval=interval, blit=True)

plt.show()

