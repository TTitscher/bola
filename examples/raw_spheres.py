from bola import psd
from bola.packing import show, rsa

import numpy as np

def main():
    gc = psd.GradingCurves.fuller(2, 16, 0.5)
    box = (32, 32, 32)
    radii = psd.sample_grading_curve(gc, V=0.6 * np.prod(box))
    show(radii)

    spheres = rsa(radii, box)
    show(spheres, box, filename="out.jpg")

if __name__ == "__main__":
    main()
