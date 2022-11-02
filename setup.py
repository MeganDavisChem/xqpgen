#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    author="Megan Christina Davis",
    author_email='mdavis22@go.olemiss.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="XQPgen (Excited state QFF Points generator) is a simple python script that takes an input molecule and generates points to run an excited state quartic force field",
    entry_points={
        'console_scripts': [
            'xqpgen=xqpgen.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='xqpgen',
    name='xqpgen',
    packages=find_packages(include=['xqpgen', 'xqpgen.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/MeganDavisChem/xqpgen',
    version='0.1.0',
    zip_safe=False,
)
