#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0', 
    'configparser',
    'numpy',
    'python-dateutil',
    'pytz',
    'requests',
    'tzlocal',
    'Pillow',
    'evdev',
    'rich',
    'pretty_errors',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest>=3',
    'Faker',
    'pytest-mock',
]

setup(
    author="Martin Lanser",
    author_email='martinlanser@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    description="This sciLab app collects and stores data frome the RPI SenseHAT component, OpenWeather API, etc. It is specifically designed to run on the 'pired' unit (RP3 B+).",
    entry_points={
        'console_scripts': [
            'pired=src.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['sensehat','raspberrypi'],
    name='pired',
    packages=find_packages(include=['src', 'src.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mlanser/sciLab-SenseHat',
    version='0.1.0',
    zip_safe=False,
)
