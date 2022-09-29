# Python Flask minimal host

A very (non-)minimal structure for a Flask application.

This repository is aimed at providing a baseline for starting a Flask application.

It is conceived in such a way that an application is assumed to be an installable Python package.

Configuration is provided through [`.flaskenv`](.flaskenv) file.

**NOTE:** in *real world* never commit `.flaskenv`, add it to [`.gitignore`](.gitignore).

Generate project wheel with `python setup.py bdist_wheel` or install directly with `pip install .`.

Run locally with `python wsgi.py` or `flask run` (from any directory if it has been installed).
