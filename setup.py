from setuptools import setup, find_packages
import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

setup(
    name = 'iudex',
    version = '0.1.0',
    author = 'Josh Karpel',
    author_email = 'josh.karpel@gmail.com',
    description = '',
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    url = 'https://github.com/JoshKarpel/iudex',
    classifiers = [
    ],
    packages = find_packages(
        exclude = ['tests'],
    ),
    install_requires = [
    ],
)
