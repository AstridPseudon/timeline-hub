"""Pick an interpreter that can build wheels offline with --no-build-isolation."""

from __future__ import annotations

import subprocess
import sys

# setuptools >= 70.1 ships bdist_wheel itself; older ones need the `wheel`
# package. Importing setuptools.build_meta alone is not enough: pip then fails
# with "invalid command 'bdist_wheel'".
BUILD_PROBE = (
    "import setuptools.build_meta\n"
    "try:\n"
    "    import setuptools.command.bdist_wheel\n"
    "except ImportError:\n"
    "    import wheel.bdist_wheel\n"
)
CANDIDATES = (sys.executable, "python3.11", "python3.12", "python3.13", "python3", "python")


def can_build_wheels(candidate, *, env=None) -> bool:
    try:
        probe = subprocess.run([candidate, "-c", BUILD_PROBE], capture_output=True, check=False, env=env)
    except OSError:
        return False
    return probe.returncode == 0


def find_wheel_builder():
    return next((candidate for candidate in CANDIDATES if can_build_wheels(candidate)), None)
