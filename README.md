<h1 align="center">
<img src="https://raw.githubusercontent.com/TTitscher/bola/main/logo/bola.svg" width="300">
</h1><br>

Collection of sphere packing and meshing algorithms.

# Installation

~~~sh
pip3 install bola
~~~

The `c++` code requires the math library `Eigen3` to be installed and a dependency of the python `gmsh` package is `libglu`. So, you may need to run (debian/ubuntu-based):

~~~sh
sudo apt update
sudo apt -y install libeigen3-dev libglu1
~~~

Alternatively, you can follow the steps of the [CI](./.github/workflows/ci.yml#L21-35).

# Examples
