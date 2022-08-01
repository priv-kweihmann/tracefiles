# SPDX-FileCopyrightText: 2022 Konrad Weihmann
# SPDX-License-Identifier: BSD-2-Clause

import subprocess
import setuptools

_long_description = 'See https://github.com/priv-kweihmann/tracefiles for documentation'
_long_description_content_type = 'text/plain'
try:
    _long_description = subprocess.check_output(
        ['pandoc', '--from', 'markdown', '--to', 'markdown', 'README.md']).decode('utf-8')
    _long_description_content_type = 'text/markdown'
except (subprocess.CalledProcessError, FileNotFoundError):
    pass

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='tracefiles',
    version='1.0.0',
    author='Konrad Weihmann',
    author_email='kweihmann@outlook.com',
    description='A utility to find used sources from a binary',
    long_description=_long_description,
    long_description_content_type=_long_description_content_type,
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
        'Programming Language :: Python :: 3'
    ],
)
