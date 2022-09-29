# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

name = "flaskapp"
version = {}

with open(F"{name}/version.py") as fp:
    exec(fp.read(), version)

setup(
    name=name,
    packages=find_packages(),
    author=version["author"],
    description="Sample Flask application",
    version=version["version"],
    install_requires=version["install_requires"],
    package_data=version["package_data"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
