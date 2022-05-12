from . import _cpp


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
):
    b = _cpp.Cube(*l)
    spheres, tries = _cpp.rsa(radii, b, seed, n_tries)

    if ret_tries:
        return spheres, tries
    else:
        return spheres
