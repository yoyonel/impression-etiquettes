#!/usr/bin/python3

from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

with open("LICENSE", "r") as license_file:
    license = license_file.read()

setup(
    name='imprimeti',
    version='1.0',
    author='Romuald Dugied',
    author_email = 'romuald.dugied@gmail.com',
    url='https://github.com/RomualdDugied/impression-etiquettes',
    description='Logiciel impression etiquette',
    long_description=long_description,
    long_description_content_type='text/mardown',
    license='GNU GPLv3',
    packages=find_packages(),    
)
