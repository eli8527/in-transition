execfile("core.py")

import numpy as np
import random
import matplotlib.pyplot as plt
import pyglet

# Models an agent for a specific location for a day
class PoissonArm():
  def __init__(self, lbda):
    self.l = lbda

  def draw(self):
    return np.random.poisson(self.l)

class NormalArm():
  def __init__(self, mu, sigma):
    self.mu = mu
    self.sigma = sigma

  def draw(self):
    return random.gauss(self.mu, self.sigma)


# pos1 = PoissonArm(1000)
# pos2 = PoissonArm(400)
# pos3 = PoissonArm(623)
# pos4 = PoissonArm(400)

pos1 = NormalArm(800, 400)
pos2 = NormalArm(400, 400)
pos3 = NormalArm(623, 400)
pos4 = NormalArm(400, 400)

positionArms = [pos1, pos2, pos3, pos4]
positionCoords = [[20, 20], [45, 50], [20, 10], [50, 20]]

ucb = UCB1([], [])
ucb.initialize(len(positionArms))

plt.axes()

plt.axis('scaled')
plt.show()

for t in range(100):
    chosen_arm = ucb.select_arm()
    print chosen_arm
    reward = positionArms[chosen_arm].draw()
    ucb.update(chosen_arm, reward)
    # draw

print ucb.counts
