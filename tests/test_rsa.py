import bola.psd
from bola.packing import rsa
import numpy as np

def test_grading():
    L = 50.
    phi = 0.6

    gc = bola.psd.GradingCurves.fuller()
    radii = bola.psd.sample_grading_curve(gc, L**3 * phi)
    spheres = rsa(radii, (L, L, L))

    assert spheres is not None
    assert len(spheres) == len(radii)

