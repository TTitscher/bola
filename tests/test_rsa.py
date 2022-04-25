import bola.psd
from bola.rsa import rsa

def test_grading():
    L = 50.
    phi = 0.6

    gc = bola.psd.GradingCurves.fuller()
    radii = bola.psd.sample_grading_curve(gc, L**3 * phi)
    spheres, ntries = rsa(radii, L)

    assert spheres is not None
    assert len(spheres) == len(radii)

