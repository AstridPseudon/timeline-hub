from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.errors import OptionError


class CleanBuildPy(build_py):
    """Never package modules left behind by an older source build."""

    def run(self):
        if getattr(self, "editable_mode", False):
            super().run()
            return

        build_root = Path(__file__).resolve().parent / "build"
        build_lib = Path(os.path.abspath(self.build_lib))
        try:
            relative = build_lib.relative_to(build_root)
        except ValueError as exc:
            raise OptionError(
                "Runtime wheel builds may only clear build output under the repository build/ directory"
            ) from exc
        if not relative.parts:
            raise OptionError("refusing to clear the build/ directory itself")
        cursor = build_root
        if cursor.is_symlink():
            raise OptionError("refusing to clear output through a symlinked build/ directory")
        for part in relative.parts:
            cursor /= part
            if cursor.is_symlink():
                raise OptionError("refusing to clear output through a symlinked build path")

        shutil.rmtree(build_lib, ignore_errors=True)
        super().run()


setup(cmdclass={"build_py": CleanBuildPy})
