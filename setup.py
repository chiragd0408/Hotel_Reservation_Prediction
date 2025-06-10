from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS-Projects-1",
    version="0.1",
    author="Chirag",
    package = find_packages(),
    install_requires = requirements,
)