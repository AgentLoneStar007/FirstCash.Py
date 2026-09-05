#!/bin/bash

# Remove the distribution directory
echo --- Removing existing builds of library...
rm -drf dist/

# Activate the virtual environment
echo --- Activating virtual environment...
source .venv/bin/activate || return

# Uninstall existing FirstCash.py library
echo --- Uninstalling existing build of library...
pip uninstall -y firstcash

# Build latest version of library
echo --- Building latest version of library...
python -m build || return

# Install it from the distribution directory
echo --- Installing latest version...
pip install dist/*.whl --force-reinstall

echo --- Done!
