import os
from setuptools import setup

full_version = '0.1.0'


import pathlib
import pkg_resources

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

# print(install_requires)

with open('README.md') as f:
    readme = f.read()

setup(
    name="algo_trader_cli",
    version=full_version,
    author="Seenu Reddy",
    author_email='srinivasulur55.s@gmail.com',
    description="Algo Trader Cli tool",
    long_description=readme,
    keywords="",
    license='LICENSE',
    url="",
    include_package_data=True,
    packages=['algo_trader_cli'],
    install_requires=install_requires,
    test_suite='tests',
    entry_points = {
        'console_scripts': ['algocli=algo_trader_cli.cli:cli',]
    }
)