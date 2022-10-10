# Python download requirements

Simple script to port a Python 3.10 environment in a machine without network access.

Pre-selected packages are intended for general scientific computation and data science.

In a computer with internet access run `run.ps1` to create `deps/` with all packages.

Copy `deps/` directory to target machine where same Python version is installed for installation.

In target machine run the following to install all packages:

```bash
pip install -r requirements-prod.txt --no-index --find-links deps
```

All should be fine by now!
