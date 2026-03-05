from setuptools import setup, find_packages

setup(
    name='gotpsi_sequentialcard',
    version='0.1.0',
    description='Python library for utilities for analyzing the gotpsi sequential card test',
    author='Avanti Shrikumar',
    url='https://github.com/AvantiShri/gotpsi_sequentialcard',
    packages=find_packages(exclude=['tests*']),
    install_requires=[],
    extras_require={}
)
