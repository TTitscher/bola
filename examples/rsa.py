import bola.psd
from bola.packing import rsa, show
import numpy as np

def main():
    L = 50.
    phi = 0.6

    gc = bola.psd.GradingCurves.fuller(d_min=0.5)
    radii = bola.psd.sample_grading_curve(gc, L**3 * phi)
    print(len(radii), flush=True)
    spheres = rsa(radii, (L, L, L))

    show(spheres, (L, L, L))

if __name__ == "__main__":
    main()
