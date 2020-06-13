#!/usr/bin/env python3
import setuptools
import v4l2ctl


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="v4l2ctl",
    version=v4l2ctl.__version__,
    license="European Union Public Licence 1.2 (EUPL 1.2)",
    author=v4l2ctl.__author__,
    author_email="mich.m.israel@gmail.com",
    description="Python package to control V4l2 drivers",
    platforms=["Linux"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelIsrael/v4l2ctl",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
)
