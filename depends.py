import numpy as np

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