"""Explicit canonical compilation at the prepared Root-props boundary.

This helper does not admit or identify a source. The caller must already own
the admitted canonical snapshot, renderer lock, validated runtime tools and
settled generated registries. Native file inputs must not call this helper.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

from astrid.core.rendering.remotion_runtime import RemotionRuntimeTools, probe_context


def compile_canonical_root_props(
    props: Mapping[str, Any],
    *,
    project_dir: Path,
    runtime_tools: RemotionRuntimeTools,
) -> dict[str, Any]:
    """Attach the public compiler's serialized result without changing authored data.

    Use once after preparing the actual assets and resolved theme, before
    writing --props and notifying the capture scene observer. There is no
    fallback to native outgoing semantics if compilation is unavailable.
    """
    if "compiledTransitions" in props:
        raise ValueError("canonical Root props have already been compiled")
    project = project_dir.resolve(strict=True)
    helper = (project / "canonical-transitions.mjs").resolve(strict=True)
    helper.relative_to(project)
    if not helper.is_file():
        raise ValueError("canonical compiler adapter is not a file")
    environment = probe_context(environment=os.environ, python_executable=sys.executable)["node_env"]
    if "ASTRID_PACKS_PATH" in os.environ:
        environment["ASTRID_PACKS_PATH"] = os.environ["ASTRID_PACKS_PATH"]
    result = subprocess.run(
        [str(runtime_tools.node_executable), str(helper), str(project)],
        input=json.dumps(dict(props), allow_nan=False),
        cwd=project,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "canonical transition compilation unavailable")
    compiled = json.loads(result.stdout)
    if not isinstance(compiled, dict) or set(compiled) != {"fps", "tracks"}:
        raise ValueError("invalid canonical transition compiler response")
    return {**props, "compiledTransitions": compiled}
