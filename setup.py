# pyinstaller -F src/main.py src/gui.py src/redshift.py  --name redshift-gui

import os
from setuptools import setup

setup(
    name = "redshift-gui",
    version = "0.2",
    author = "thatziv",
    description = "A GUI for Redshift",
    packages=['src'],
    package_dir={'src': 'src'},
    install_requires = [line.strip() for line in open('requirements.txt')],
)