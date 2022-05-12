from . import _cpp
import numpy as np


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

def sphere_vector(spheres):
    v = []
    for sphere in spheres:
        s = _cpp.Sphere()
        s.x = sphere[:3]
        s.r = sphere[3]
        v.append(s)
    return v

def show(spheres, box):
    from . import visu
    N = len(spheres) 

    v = visu.SphereVisualizer(N)
    v.add_box(*box.l)

    x = np.empty((N, 3))
    r = np.empty(N)

    for i in range(N):
        x[i] = spheres[i].x
        r[i] = spheres[i].r

    v.update_data(x, r)
    v.show()

