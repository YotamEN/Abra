from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Abra',
    version="1.0",
    author='Yotam Even-Nir',
    description='Abra: Advanced System Design course final project',
    long_description=long_description,
    packages=find_packages(),
    install_requires=['click', 'flask'],
    tests_require=['pytest', 'pytest-cov']
)
