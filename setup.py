# SPDX-FileCopyrightText: 2022 Konrad Weihmann
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='tracefiles',
    version='1.2.0',
    author='Konrad Weihmann',
    author_email='kweihmann@outlook.com',
    description='A utility to find used sources from a binary',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/priv-kweihmann/tracefiles',
    packages=setuptools.find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': [
            'tracefiles = tracefiles.__main__:main',
        ],
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3',
    ],
)
