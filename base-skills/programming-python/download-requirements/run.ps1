# Ensure up-to-date pip.
python -m pip install --upgrade pip

# First install locally.
pip install -r requirements-dev.txt

# Dump environment to file.
pip freeze > requirements-prod.txt

# Download all packages.
pip download -d deps -r requirements-prod.txt

# Create a local portable python
python -m majordome.mkpyenv

# Install everything (not working because of future)
embed/python/python.exe -m pip install -r requirements-prod.txt
