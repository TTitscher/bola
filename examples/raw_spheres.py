from bola import psd
from bola import packing
from bola import mesh
import copy

import numpy as np


def main():
    gc = psd.GradingCurves.fuller(4.0, 16.0, 0.5)
    box = (32.0, 32.0, 32.0)
    radii = psd.sample_grading_curve(gc, V=0.5 * np.prod(box))

    spheres = packing.rsa(radii, box)

    sim = packing.edmd(box, spheres, growth_rate=0.1)
    packing.show(radii, filename="gc.jpg")
    packing.show(spheres, box, filename="rsa.jpg")

    while sim.t() < 10.0:
        sim.process(100 * len(radii))
        sim.synchronize(True)
        print(packing.stats_string(sim), flush=True)

    new_spheres = sim.spheres()
    new_spheres[:, 3] = spheres[:, 3]
    packing.show(spheres, box, filename="edmd.jpg")

    mesh.create(
        box,
        spheres,
        mesh.GmshOptions(
            mesh_size_matrix=0.5, mesh_size_aggregates=0.5, out="mesh.xdmf", zslice=16.0
        ),
        show=True,
    )


if __name__ == "__main__":
    main()
