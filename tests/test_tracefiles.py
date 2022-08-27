# SPDX-FileCopyrightText: 2022 Konrad Weihmann
# SPDX-License-Identifier: BSD-2-Clause

import os
from typing import List

import pytest
from tracefiles.__main__ import get_sources, PathWithScanningDepth


def _get_all_files_from_dir(path: str) -> List[str]:
    _dirs = set()
    _files = set()
    for root, dirs, files in os.walk(path):
        for d in dirs:
            _dirs.add(os.path.join(root, d))
        for f in files:
            _files.add(os.path.join(root, f))
    return (_files, _dirs)


def test_tracefiles_no_debug():
    binaries, _ = _get_all_files_from_dir(pytest.demoapp_package)
    sourcedir = pytest.demoapp_src
    assert get_sources([PathWithScanningDepth(sourcedir)], binaries, []) == [
        'sub/folder1/plain', 'template.in']


def test_tracefiles_debug():
    binaries, _ = _get_all_files_from_dir(pytest.demoapp_package)
    _, debugpaths = _get_all_files_from_dir(pytest.demoapp_debug)
    sourcedir = pytest.demoapp_src
    assert get_sources([PathWithScanningDepth(sourcedir)], binaries, debugpaths) == ['external.c',
                                                                                     'external.h',
                                                                                     'main.c', 'sub/folder1/plain', 'template.in']
