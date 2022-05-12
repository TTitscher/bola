import bola
import bola.packing
from bola._cpp import *
import numpy as np

def api():
    box = Cube(10, 10, 10)
    N = 1000
    r = np.full(1000, 0.3)

    spheres = bola.packing.sphere_vector(bola.packing.rsa(r, box.l))
    for s in spheres:
        s.gr = 0.
        s.m = 1.
        s.v = np.random.random(3)

    sim = Simulation(spheres, box)
    sim.process(10000)
    print(sim.stats.n_collisions)
    sim.process(10000)
    print(sim.stats.n_collisions)



def newtons_cradle():
    box = Cube(10, 10, 10)

    # 5 spheres in the middle
    spheres = []
    for i in range(5):
        s = Sphere()
        s.r = 0.5
        s.x = [i + 3, 5, 5]
        spheres.append(s)

    spheres[0].x = [1, 5, 5]
    spheres[0].v = [1, 0, 0]

    bola.packing.show(spheres, box)

    sim = Simulation(spheres, box, )

    pass


if __name__ == "__main__":
    api()
