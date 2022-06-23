<h1 align="center">
<img src="https://raw.githubusercontent.com/TTitscher/bola/main/logo/bola.svg" width="300">
</h1><br>

Collection of sphere packing and meshing algorithms.

# Installation

~~~sh
pip3 install bola
~~~

The `c++` code requires the math library [`Eigen3`](https://eigen.tuxfamily.org) to be installed and a dependency of the python [`gmsh`](https://pypi.org/project/gmsh/) package is `libglu`. So, you may need to run (debian/ubuntu-based):

~~~sh
sudo apt update
sudo apt -y install libeigen3-dev libglu1
~~~

Alternatively, you can follow the steps of the [CI](./.github/workflows/ci.yml#L21-L35).

# Examples

Particle size according to `bola.psd.GradingCurve` (sieve lines):
<h1 align="center">
<img src="https://raw.githubusercontent.com/TTitscher/bola/main/examples/gc.jpg" width="300">
</h1><br>

Initial packing using `bola.packing.rsa` (random sequential addition)
<h1 align="center">
<img src="https://raw.githubusercontent.com/TTitscher/bola/main/examples/rsa.jpg" width="300">
</h1><br>

Maximize particle distance using `bola.packing.edmd` (event-driven molecular-dynamics)
<h1 align="center">
<img src="https://raw.githubusercontent.com/TTitscher/bola/main/examples/edmd.jpg" width="300">
</h1><br>

Mesh via gmsh using `bola.mesh`
<h1 align="center">
<img src="https://raw.githubusercontent.com/TTitscher/bola/main/examples/mesh.jpg" width="300">
</h1><br>

