# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import Extension


def main():
    """ Main function to build spam extension. """
    name = "spam"
    extension = Extension(name, ["src/spam.c"])

    setup(
        name=name,
        version="1.0.0",
        description="Samply Python C-module",
        author="Walter Dal'Maz Silva",
        author_email="walter.dalmazsilva.manager@gmail.com",
        ext_modules=[
            extension
        ]
    )


if __name__ == "__main__":
    main()
