import numpy as np
import random
import sympy as sp
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from depends import Charge, Vector, CoulombConverter


# Needed functions
def generateCharges(n, randomValue = True, valueInterval=(0.1, 5), xInterval=(-80, 80), yInterval=(-50, 50)):
    charges = []
    converter = CoulombConverter()

    min_value, max_value = valueInterval
    min_x, max_x = xInterval
    min_y, max_y = yInterval

    for _ in range(n):
        value = random.uniform(min_value, max_value)
        value = converter.microToCoulomb(value)
        x = round(random.uniform(min_x, max_x),2)
        y = round(random.uniform(min_y, max_y),2)
        charge = Charge(value, x, y)
        charges.append(charge)
    return charges

def getVelocityFunction(a):
  t = sp.symbols('t')
  function = a * t
  return function

def getAceleration(mass, fy: list):
  a = sp.symbols('a')
  f = mass * a
  sumf = sum(fy)
  # sumf = f so...
  equation = sp.Eq(f,sumf)
  return sp.solve(equation,a)[0]

def generateChargesCoordenates(start, end, delta, y = 0):
  i = start
  coords = []
  while True:
    if i >= end:
      break
    coords.append((i,y))
    i += delta
  return coords

def generateChargeValue(n):
  convert = CoulombConverter()
  values = []
  for v in range(n):
    value = random.randint(0,10)
    if value == 0:
      value += 0.1
    value = convert.microToCoulomb(value)
    values.append(value)
  return values

def getForcesVectors(charges, q0):
  forcesVectors = []
  for c in charges:
    x1 = c.getX()
    y1 = c.getY()
    x2 = c.getCoulombLaw(q0)[0]
    y2 = c.getCoulombLaw(q0)[1]
    vector = Vector((x1,y1), (x2,y2))
    forcesVectors.append(vector)
  return forcesVectors

def getVelocity(a, v0, t):
  return v0 + (-a*t)

def getPosition(p0, v0, a, t):
  return p0 + v0*t + (1/2)*t*t*-a

# I got some help from Claude3
def functionOf(textFunction, variable, evaluatefor):
    var = sp.symbols(variable)
    func = sp.sympify(textFunction)
    result = func.subs(var, evaluatefor)
    return result

# Limits for plot
xLimits, yLimits = (-15,15), (-15,15)

# Limits for charges (positives)
intervalForCharges = (-5,5)
start, stop = intervalForCharges

# Generate the negatives line
negativesLineY = [functionOf("0","x",i) for i in range(start, stop)]
negativesLineX = [i for i in range(start, stop)]

# Generate the positives line
positivesLineY = [functionOf("-5","x",i) for i in range(start, stop)]
positivesLineX = [i for i in range(start, stop)]

# Generate charges coords - values - mass and more stuff
chargesCoords = generateChargesCoordenates(start, stop, 0.5, -5)
chargesValues = generateChargeValue(len(chargesCoords))
chargesValues = [2*10**(-6)]*len(chargesCoords)
charges = [Charge(chargesValues[i], chargesCoords[i][0], chargesCoords[i][1]) for i in range(len(chargesCoords))]

puntualChargeCoords = (0,0)
# Mass got from internet
puntualChargeMass = 9.109e-31
puntualCharge = Charge(-2, puntualChargeCoords[0], puntualChargeCoords[1])

chargesCoordsX = [x[0] for x in chargesCoords]
chargesCoordsY = [y[1] for y in chargesCoords]

xPosition = puntualChargeCoords[0]
yPosition = puntualChargeCoords[1]


# Let's move the charge!
fig, ax = plt.subplots()
ax.set_xlim(xLimits)
ax.set_ylim(yLimits)

ax.plot(negativesLineX, negativesLineY, 'r')
ax.plot(positivesLineX, positivesLineY, 'g')
ax.scatter(chargesCoordsX, chargesCoordsY)
posText = ax.text(0.05, 0.95, '', transform=ax.transAxes, ha='left', fontsize=10)
acelerationText = ax.text(0.05, 0.90, '', transform=ax.transAxes, ha='left', fontsize=10)
velocityText = ax.text(0.05, 0.85, '', transform=ax.transAxes, ha='left', fontsize=10)

interval = 10
lastxVelocity = 0
lastyVelocity = 0

def animate(frame):
  global xPosition, yPosition, interval, lastxVelocity, lastyVelocity, totalPost

  time = (frame*interval)/1000

  if time == 0:
    lastxVelocity = 0
    lastyVelocity = 0

  # Get vectors
  forcesVectors = getForcesVectors(charges, puntualCharge)
  forcesyVectors = [v.getYVector() for v in forcesVectors]
  forcesxVectors = [v.getXVector() for v in forcesVectors]
  forcesxSum = [v.getMagnitude() for v in forcesxVectors]
  forcesySum = [v.getMagnitude() for v in forcesyVectors]

  # Get aceleraction (Using 2nd newton's law [F = MA])
  xAceleration, yAceleration = getAceleration(puntualChargeMass, forcesxSum), getAceleration(puntualChargeMass, forcesySum)

  # Get velocity (Using MRUA eq) (x) (y)
  vx, vy = getVelocity(xAceleration, lastxVelocity, time), getVelocity(yAceleration, lastyVelocity, time)

  # Get position (Using MRUA eq) (x) (y)
  xPosition, yPosition = getPosition(xPosition, vx, xAceleration, time), getPosition(yPosition, vy, yAceleration, time)

  scalar = 1e35

  fx, fy = xPosition/scalar, yPosition/scalar

  point = ax.scatter(fx, fy, color='blue')
  posText.set_text(f"Pos (x,y) = ({(xPosition)}, {(yPosition)})")
  velocityText.set_text(f"Vel (x,y) = ({(vx)}, {(vy)})")
  acelerationText.set_text(f"Acel (x,y) = ({(xAceleration)}, {(yAceleration)})")
  return point, posText, velocityText, acelerationText

# ChatGPT helps us here
ani = animation.FuncAnimation(fig, animate, frames=100000, interval=interval, blit=True)

plt.show()


