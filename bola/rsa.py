import _cpp


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


if __name__ == "__main__":
    import numpy as np

    phi = 0.3
    N = 1000
    r = np.ones(N) * (phi * 3 / (4 * N * np.pi)) ** (1 / 3)

    print(4 / 3 * np.pi * np.sum(r ** 3))
    spheres, tries = rsa(r, n_tries=100000, ret_tries=True)
    print("Average number of tries:", np.sum(tries) / len(r))
