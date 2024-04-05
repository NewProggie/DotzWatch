# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='DotzWatch',
    version='0.1.0',
    description='Simple network monitoring tool',
    long_description=readme,
    author='Kai Wolf',
    author_email='mail@kai-wolf.me',
    url='https://github.com/NewProggie/DotzWatch.git',
    license=license,
    packages=find_packages(exclude=('tests')))
