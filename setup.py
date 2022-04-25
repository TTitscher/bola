import setuptools
import site
import sys

# https://github.com/googlefonts/fontmake/commit/164b24fd57c062297bf68b21c8ae88bc676f090b
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

__version__ = "0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bola",
    version=__version__,
    author="Thomas Titscher",
    author_email="thomas.titscher@gmail.com",
    description="Sphere stuff",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    zip_safe=False,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["tabulate", "numpy", "loguru", "scipy", "vtk"],
    extras_require={  # Optional
        "dev": ["black"],
        "test": ["pytest", "pytest-cov", "flake8"],
    },
)
