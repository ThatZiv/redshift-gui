import os
from setuptools import setup

setup(
    name = "redshift-gui",
    version = "0.1",
    author = "thatziv",
    description = "A GUI for Redshift",
    packages=['src'],
    package_dir={'src': 'src'},
    install_requires = [line.strip() for line in open('requirements.txt')],
)