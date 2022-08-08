# SPDX-FileCopyrightText: 2022 Konrad Weihmann
# SPDX-License-Identifier: BSD-2-Clause

import os
import subprocess

import pytest


def _demo_app_path() -> str:
    return os.path.join(os.path.dirname(__file__), 'demoapp')


def _clean_demoapp() -> None:
    subprocess.check_call(['make', 'clean'], cwd=_demo_app_path())


def pytest_sessionstart(session):
    _clean_demoapp()
    subprocess.check_call(['make'], cwd=_demo_app_path())

    pytest.demoapp_base = _demo_app_path()
    pytest.demoapp_src = os.path.join(pytest.demoapp_base, 'src')
    pytest.demoapp_package = os.path.join(
        pytest.demoapp_base, 'packages', 'pkg1')
    pytest.demoapp_debug = os.path.join(
        pytest.demoapp_base, 'packages', 'pkg1-dbg')


def pytest_sessionfinish(session, exitstatus):
    _clean_demoapp()
