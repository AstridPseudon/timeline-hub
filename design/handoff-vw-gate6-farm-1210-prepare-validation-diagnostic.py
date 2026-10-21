#!/usr/bin/env python3
"""Run the frozen host validation transaction without starting a host or Runtime."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path


AGENT = Path("/home/user/work/wt/agt-pin-d0a5072b")
RUNTIME = Path("/home/user/work/wt/rt-pin-8f105c26")
REMOTION = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage/remotion")
WORKER = Path(__file__).resolve().parent
PYTHON = "/home/user/work/venv-agent/bin/python"
SCHEMA = "/home/user/work/venv-agent/lib/python3.11/site-packages"
NODE = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _file_state(path: Path) -> tuple[int, int, int, str]:
    facts = path.stat()
    return facts.st_size, facts.st_mtime_ns, facts.st_ctime_ns, _digest(path)


def main() -> int:
    sys.path.insert(0, str(AGENT))
    from astrid.core.rendering.remotion_runtime import (  # noqa: PLC0415
        RemotionValidationError,
        _registry_context,
        probe_context,
    )
    from astrid.sdk import host_bootstrap  # noqa: PLC0415
    from astrid.packs.rendering.rendering.renderers.remotion import run  # noqa: PLC0415

    if os.environ.get("GIT_CONFIG_COUNT") or os.environ.get("PYTHONNOUSERSITE"):
        raise RuntimeError("diagnostic must receive the clean explicit environment")
    tmpdir = Path(tempfile.mkdtemp(prefix="gate6-validation-tmp-", dir=os.environ["TMPDIR"]))
    output = Path(tempfile.mkdtemp(prefix="gate6-validation-output-", dir=str(WORKER)))
    project_files = [*run._registry_output_paths(REMOTION), REMOTION / run._REGISTRY_STATE_PATH]
    before = {str(path): _file_state(path) for path in project_files if path.is_file()}
    try:
        # Preserve both known negative witnesses with the frozen validator.
        startup_negative = dict(os.environ)
        startup_negative["PYTHONNOUSERSITE"] = "1"
        try:
            probe_context(environment=startup_negative, python_executable=PYTHON)
        except RemotionValidationError:
            print("negative-PYTHONNOUSERSITE=PASS")
        else:
            raise RuntimeError("PYTHONNOUSERSITE negative witness was accepted")

        git_negative = dict(os.environ)
        git_negative.update({
            "GIT_CONFIG_COUNT": "3",
            "GIT_CONFIG_KEY_0": "credential.interactive",
            "GIT_CONFIG_KEY_1": "url.https://github.com/.insteadOf",
            "GIT_CONFIG_KEY_2": "url.https://github.com/.insteadOf",
            "GIT_CONFIG_VALUE_0": "false",
            "GIT_CONFIG_VALUE_1": "git@github.com:",
            "GIT_CONFIG_VALUE_2": "ssh://git@github.com/",
        })
        try:
            _registry_context(git_negative, generator=False)
        except RemotionValidationError:
            print("negative-GIT_CONFIG=PASS")
        else:
            raise RuntimeError("GIT_CONFIG_* negative witness was accepted")

        # This is the same environment construction used before the host child:
        # host_bootstrap copies the explicit launch env, adds source/dependencies,
        # and then invokes the supported full prepare/validate entrypoint.
        host_env = host_bootstrap._host_render_environment(AGENT)
        print(json.dumps({
            "host_environment_keys": sorted(host_env),
            "forbidden_keys_after_projection": sorted(
                key for key in host_env if key.startswith("GIT_") or key.startswith("PYTHON")
                and key not in {"PYTHONDONTWRITEBYTECODE", "PYTHONUNBUFFERED", "PYTHONPATH"}
            ),
        }))
        launch_id = host_bootstrap._prepare_render_validation(
            AGENT,
            host_env,
            output,
            PYTHON,
            (AGENT / "astrid" / "packs",),
        )
        if not launch_id or len(launch_id) != 32:
            raise RuntimeError("full validation did not return a fresh launch id")
        after = {str(path): _file_state(path) for path in project_files if path.is_file()}
        if before != after:
            raise RuntimeError("immutable Remotion registry files changed during validation")
        print(json.dumps({
            "full_prepare_render_validation": "PASS",
            "runtime_started": False,
            "helper_started": False,
            "browser_started": False,
            "returned_reference_keys": sorted(host_env),
            "private_output_files": sorted(
                str(path.relative_to(output)) for path in output.rglob("*") if path.is_file()
            ),
            "tuple": {
                "app": "0d4323913b92c4e0e3830bf14ec7f35d981475ca/5a1e0e85d0f336f642426b91ccf3b3f1984ebd14",
                "agent": "d0a5072bbe7b7ce9489f43aa0a81027ec400343b",
                "runtime": "8f105c26e3b62f9c2683f717a9773a12bc775a8e",
                "composition": "5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8/13e375534fffd704305eced5686699d2c8c9c948",
                "node": "20.19.4/43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490",
                "runtime_graph": "4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c/21455",
            },
        }))
        return 0
    finally:
        shutil.rmtree(output, ignore_errors=True)
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
