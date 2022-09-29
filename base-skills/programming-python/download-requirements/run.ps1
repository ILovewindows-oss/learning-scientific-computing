# Ensure up-to-date pip.
python -m pip install --upgrade pip

# First install locally.
pip install -r requirements-dev.txt

# Dump environment to file.
pip freeze > requirements-prod.txt

# Download all packages.
pip download -d deps -r requirements-prod.txt
