import numpy as np
import random
import sympy as sp
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# Class Coulomb convertor
class CoulombConverter:
    def __init__(self):
        self.k = 8.9875517923e9

    def getConstant(self):
        return self.k

    def coulombToNewton(self, coulombs):
        force = self.k * coulombs / (1**2)
        return force

    def newtonToCoulomb(self, newtons):
        coulombs = newtons * (1**2) / self.k
        return coulombs

    def microToCoulomb(self, micro):
        return micro / 1e6

    def coulombToMicro(self, coulomb):
        return coulomb * 1e6

# Class vector
class Vector:
  def __init__(self, start: tuple, end: tuple):
    self.start = start
    self.end = end
    self.vector = np.array([self.end[0], self.end[1]]) - np.array([self.start[0], self.start[1]])

  def getVector(self):
    return self.vector

  def getTupleVector(self):
    return tuple(self.vector)

  def getMagnitude(self):
    return np.linalg.norm(self.vector)

  def getDirection(self):
    if self.vector[0] == 0:
      return 0
    return np.arctan(self.vector[1]/self.vector[0])

  def getXVector(self):
    direction = self.getDirection()
    magnitude = self.getMagnitude()
    start = self.start
    end = (magnitude*np.cos(direction),0)
    return Vector(start, end)

  def getYVector(self):
    direction = self.getDirection()
    magnitude = self.getMagnitude()
    start = self.start
    end = (0,magnitude*np.sin(direction))
    return Vector(start, end)

  def copy(self):
    return np.array([self.vector[0], self.vector[1]])

  def getUr(self):
    return self.copy()/self.getMagnitude()

  def __repr__(self) -> str:
    return str(self.getTupleVector())

# Class Charge
class Charge:
  def __init__(self, value, x, y):
    self.value = value
    self.x = x
    self.y = y

  def _getSign(self, value):
    if value < 0:
      return -1
    return 1

  def getValue(self):
    return self.value

  def getX(self):
    return self.x

  def getY(self):
    return self.y

  def getPoint(self):
    return (self.x,self.y)

  def getDistance(self, c2):
    return np.sqrt((self.x - c2.x)** 2 + (self.y - c2.y) ** 2)

  def getCoulombLaw(self, c2):
    k = 9*(10**9)
    r = Vector(self.getPoint(), c2.getPoint())
    magnitude = r.getMagnitude()
    direction = r.getDirection()
    ur = r.getUr()
    xSign = self._getSign(magnitude * np.cos(direction))
    ySign = self._getSign(magnitude * np.sin(direction))
    forceVector = k * abs(self.value * c2.value) * ur
    forceVector /= (magnitude)**2
    forceVector[0] *= xSign
    forceVector[1] *= ySign
    return forceVector

  def __repr__(self) -> str:
    return str(f"{self.getPoint()} - [{self.value}]")

# Depends functions
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

ax.set_xlim(xLimits)
ax.set_ylim(yLimits)
ax.plot(negativesLineX, negativesLineY)
ax.plot(positivesLineX, positivesLineY)
point = ax.scatter(charge.getX(), charge.getY())
vector = ax.quiver(charge.getX(), charge.getY(), 0, 0, angles='xy', scale_units='xy', scale=1, color='r')

# ChatGPT help us with it
proj_x = ax.plot([], [], 'g--')[0]
proj_y = ax.plot([], [], 'b--')[0]

def animate(frame):
  global E_x, E_y
  global m
  global v0_x, v0_y
  global interval
  global position
  time = (frame * interval) / 1000

  force_x = getForce(charge.getValue(), E_x)
  force_y = getForce(charge.getValue(), E_y)

  acceleration_x = force_x / m
  acceleration_y = force_y / m

  v_x = getVelocity(v0_x, acceleration_x, time)
  v_y = getVelocity(v0_y, acceleration_y, time)

  x = position[0] + (v0_x * time) + (0.5 * acceleration_x * (time ** 2))
  y = position[1] + (v0_y * time) + (0.5 * acceleration_y * (time ** 2))
  
  scalar = 1e15
  
  fx = x / scalar
  fy = y / scalar
  
  point.set_offsets((fx, fy))
  vector.set_offsets((fx, fy))
  vector.set_UVC(v_x/scalar, v_y/scalar)
  
  # ChatGPT help us with it
  proj_x.set_data([fx, fx + (v_x / 1e15)], [fy, fy])
  proj_y.set_data([fx, fx], [fy, fy + (v_y / 1e15)])

  print(f"({time}) ({fx},{fy})")
  return point, vector, proj_x, proj_y


ani = animation.FuncAnimation(fig, animate, frames=500*5, interval=interval, blit=True)

plt.show()


