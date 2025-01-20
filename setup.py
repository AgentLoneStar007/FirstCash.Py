from setuptools import setup, find_packages
import re


# Function to pull the version slug from __init__
def getVersion() -> str:
    with open("firstcash/__init__.py", 'r') as file:
        version_match: re.Match = re.search(
            r'^__version__:?\s*str\s*=\s*["\']([^"\']+)["\']', file.read(), re.M
        )
        if version_match:
            return version_match.group(1)

        raise RuntimeError("Could not find the version slug. Was it set?")


setup(
    name="firstcash.py",
    packages=find_packages(),
    version=getVersion()
)
