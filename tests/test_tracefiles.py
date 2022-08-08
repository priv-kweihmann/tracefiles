import logging
from typing import List
import pytest
import os

from tracefiles.__main__ import get_sources


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
    assert get_sources(sourcedir, binaries, []) == [
        'sub/folder1/plain', 'template.in']


def test_tracefiles_debug():
    binaries, _ = _get_all_files_from_dir(pytest.demoapp_package)
    _, debugpaths = _get_all_files_from_dir(pytest.demoapp_debug)
    sourcedir = pytest.demoapp_src
    assert get_sources(sourcedir, binaries, debugpaths) == ['external.c',
                                                            'external.h',
                                                            'main.c', 'sub/folder1/plain', 'template.in']
