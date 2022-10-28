#!/usr/bin/env python

import setuptools

VER = "0.0.1"

reqs = ["numpy",
        "h5py",
        "matplotlib>=3.6",
        "LarpixParser @ git+https://github.com/DanielMDouglas/larpix_readout_parser.git",
        "tk"]

setuptools.setup(
    name="NDeventDisplay",
    version=VER,
    author="Daniel D. and others",
    author_email="dougl215@slac.stanford.edu",
    description="A package for visualizing ND events in the LArPix format",
    url="https://github.com/DanielMDouglas/NDeventDisplay",
    packages=setuptools.find_packages(),
    install_requires=reqs,
    package_data={"NDeventDisplay": ["config/*.yaml"]},
    scripts=["bin/NDeventDisplay"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    python_requires='>=3.2',
)
