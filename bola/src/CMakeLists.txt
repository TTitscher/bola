cmake_minimum_required(VERSION 3.5 FATAL_ERROR)
project(edmd2 VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)

find_package(Eigen3 3.2 REQUIRED NO_MODULE)

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -Wall -fPIC")

set(Sources
    Box.cpp
    Simulation.cpp
    SubBox3d.cpp
    Sphere.cpp
    SubBoxes.cpp
    RandomSequentialAddition.cpp
    Heap.cpp)
add_library(EDMD ${Sources})
target_link_libraries(EDMD Eigen3::Eigen)

find_package(pybind11 REQUIRED)
pybind11_add_module(cpp python.cpp)
target_link_libraries(cpp PRIVATE pybind11::module EDMD)

