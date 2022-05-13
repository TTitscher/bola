from . import _cpp
import numpy as np
import math


def rsa(
    radii,
    l=(
        1.0,
        1.0,
        1.0,
    ),
    n_tries=10000,
    seed=6174,
    ret_tries=False,
    progress=True,
):
    b = _cpp.Cube(*l)
    spheres, tries = _cpp.rsa(radii, b, seed, n_tries, progress)

    if ret_tries:
        return spheres, tries
    else:
        return spheres

def maxwell_boltzmann_velocities(num, temperature=273.15, seed=6174):
    mb = _cpp.MaxwellBoltzmann(6174)
    vs = np.empty((num, 3))
    for v in vs:
        v = mb(temperature)
    return vs

def edmd(box, spheres, velocity=None, growth_rate=0.1, mass=1.):
    N = len(spheres)
    if velocity is None:
        velocity = maxwell_boltzmann_velocities(N)
    else:
        assert velocity.shape == (N, 3)

    if isinstance(growth_rate, float):
        growth_rate = np.full(N, growth_rate)
    else:
        assert len(growth_rate) == N

    if isinstance(mass, float):
        mass = np.full(N, mass)
    else:
        assert len(mass) == N

    sim = _cpp.Simulation(box, spheres, velocity, growth_rate, mass)
    return sim

def stats_string(sim):

    def human_format(number):
        """
        thanks to https://stackoverflow.com/a/45478574
        """
        units = ['', 'K', 'M', 'G', 'T', 'P']
        k = 1000.0
        magnitude = int(math.floor(math.log(number, k)))
        return '{:5.2f}{}'.format(number / k**magnitude, units[magnitude])

    info = "{:.4%} | ".format(sim.stats.pf)
    info += human_format(sim.stats.n_events) + " events | "
    info += "{:.2E} | ".format(sim.stats.collisionrate)
    info += "{:5.3f}s ".format(sim.t())
    return info

def show(spheres, box):
    from . import visu

    try:
        l = box.l
    except AttributeError:
        l = box

    v = visu.SphereVisualizer(len(spheres))
    v.add_box(*l)

    v.update_data(spheres[:, :3], spheres[:, 3])
    v.show()

