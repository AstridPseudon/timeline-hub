from __future__ import annotations

import os
import sys

from tests.wheel_builder import can_build_wheels


def _fake_site(root, *, wheel):
    setuptools = root / "setuptools"
    setuptools.mkdir()
    (setuptools / "__init__.py").write_text("")
    (setuptools / "build_meta.py").write_text("")
    (setuptools / "command").mkdir()
    (setuptools / "command" / "__init__.py").write_text("")
    if wheel:
        package = root / "wheel"
        package.mkdir()
        (package / "__init__.py").write_text("")
        (package / "bdist_wheel.py").write_text("")
    return {**os.environ, "PYTHONPATH": str(root)}


def test_interpreter_with_build_meta_but_no_bdist_wheel_is_rejected(tmp_path):
    assert not can_build_wheels(sys.executable, env=_fake_site(tmp_path, wheel=False))


def test_interpreter_with_wheel_package_is_accepted(tmp_path):
    assert can_build_wheels(sys.executable, env=_fake_site(tmp_path, wheel=True))
