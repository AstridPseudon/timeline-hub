"""Offline controls for working-service-binding.py.

The control reads the already approved recipe and installed decoded templates,
then checks only rendering, preservation, syntax, and refusal behaviour.  It
never evaluates a generated candidate or starts any service.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
SUITES = ORCH / "tests" / "suites.conf"
RECIPE_COMMIT = "ed81088ed8a70c2c2f4a5f5d3be6636e9e17212e"
RECIPE_REPO = Path("/home/user/banodoco/reigh-app")


def module():
    spec = importlib.util.spec_from_file_location("working_service_binding", ROOT / "working-service-binding.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("working-service-binding.py is unavailable")
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def recipe() -> dict:
    local = ROOT / "current-service-inputs.json"
    if local.is_file():
        value = json.loads(local.read_text(encoding="utf-8"))
    else:
        value = json.loads(subprocess.check_output(
            ["git", "-C", str(RECIPE_REPO), "show", f"{RECIPE_COMMIT}:current-service-inputs.json"],
            text=True,
        ))
    # The historical recipe is evidence for the immutable bench inputs only.
    # Source identity is refreshed from the current clean integration roots;
    # the adapter then authenticates it against its frozen D59 tuple.
    for role, checkout in (("app", "/home/user/work/app"), ("agent", "/home/user/work/agent"), ("runtime", "/home/user/work/runtime")):
        head = subprocess.check_output(["git", "-C", checkout, "rev-parse", "HEAD"], text=True).strip()
        tree = subprocess.check_output(["git", "-C", checkout, "show", "-s", "--format=%T", head], text=True).strip()
        parents = subprocess.check_output(["git", "-C", checkout, "show", "-s", "--format=%P", head], text=True).strip().split()
        value["source"][role] = {
            **value["source"][role],
            "ref": "tl/integration",
            "head": head,
            "tree": tree,
            "parents": parents,
        }
    value["environment"] = {
        "file": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-remotion.env",
        "ASTRID_REMOTION_PROJECT_DIR": "/home/user/work/runtimes/agent-remotion",
        "ASTRID_NODE_EXECUTABLE": "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node",
        "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": "/home/user/work/venv-agent/lib/python3.13/site-packages",
    }
    return value


def rows() -> dict[str, tuple[str, str]]:
    result = {}
    for line in SUITES.read_text(encoding="utf-8").splitlines():
        fields = line.split(None, 2)
        if len(fields) != 3 or fields[0] != "app" or fields[1] not in {"full-e2e-three-products", "ap2-P3-gate5-h6-0348"}:
            continue
        outer = fields[2]
        marker = "$(bash -c "
        start = outer.index(marker) + len(marker)
        end = outer.index(")\" && eval", start)
        body = shlex.split(outer[start:end])[0]
        result[fields[1]] = outer, body
    if set(result) != {"full-e2e-three-products", "ap2-P3-gate5-h6-0348"}:
        raise RuntimeError("approved P2/P3 templates are not both installed")
    return result


def assert_refusal(binding, mutated: dict, stage: str, template: str, label: str) -> None:
    try:
        binding.adapt_environment_block(template, stage=stage, recipe=mutated)
    except binding.BindingError:
        return
    raise AssertionError(f"negative control unexpectedly accepted: {label}")


def assert_template_refusal(binding, base: dict, mutated: str, stage: str, label: str) -> None:
    try:
        binding.adapt_environment_block(mutated, stage=stage, recipe=base)
    except binding.BindingError:
        return
    raise AssertionError(f"negative control unexpectedly accepted: {label}")


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def assert_launch_bindings(binding, result: dict[str, object], stage: str) -> None:
    """Exercise the named interpreter substitutions without starting a service."""

    values = result["bindings"]
    if not isinstance(values, dict):
        raise AssertionError(f"P{stage}: bindings are not a mapping")
    shell = "\n".join(
        (
            "set -eu",
            f'CPY={shlex.quote(values["agent_python"])}',
            f'RCPY={shlex.quote(values["runtime_python"])}',
            'ASTRID_AGENT_PYTHON="$CPY"',
            'ASTRID_RUNTIME_PYTHON="$RCPY"',
            "export ASTRID_AGENT_PYTHON ASTRID_RUNTIME_PYTHON",
            'test "$ASTRID_AGENT_PYTHON" = "$CPY"',
            'test "$ASTRID_RUNTIME_PYTHON" = "$RCPY"',
            'test "$("$ASTRID_AGENT_PYTHON" -c \'import os,sys; assert os.environ["ASTRID_AGENT_PYTHON"] == sys.executable; print(sys.executable)\')" = "$CPY"',
            'test "$("$ASTRID_RUNTIME_PYTHON" -c \'import os,sys; assert os.environ["ASTRID_RUNTIME_PYTHON"] == sys.executable; print(sys.executable)\')" = "$RCPY"',
            'if test "$ASTRID_RUNTIME_PYTHON" = "$CPY"; then exit 91; fi',
            'test "${ASTRID_AGENT_PYTHON:?}" = "$CPY"',
            'test "${ASTRID_RUNTIME_PYTHON:?}" = "$RCPY"',
        )
    )
    checked = subprocess.run(["bash", "-c", shell], text=True, capture_output=True, check=False)
    ensure(checked.returncode == 0, f"P{stage}: interpreter argv/export/failure control failed: {checked.stderr}")


def main() -> int:
    binding = module()
    base = recipe()
    template_rows = rows()
    reports = {}
    for name, (_outer, template) in template_rows.items():
        stage = "2" if name == binding.P2_TEMPLATE else "3"
        result = binding.adapt_environment_block(template, stage=stage, recipe=base)
        start, end = binding._region(template, stage)
        approval = binding._TEMPLATE_APPROVALS[stage]
        ensure(hashlib.sha256(template.encode()).hexdigest() == approval["source_sha256"], f"{name}: unapproved source template")
        ensure(start == approval["start"] and end == approval["end"], f"{name}: boundary moved")
        candidate = result["body"]
        ensure(candidate[:start] == template[:start], f"{name}: protected prefix changed")
        replacement_end = start + result["environment_region_bytes"]
        ensure(candidate[replacement_end:] == template[end:], f"{name}: protected suffix changed")
        ensure("original-body-NOTRUN" in candidate and "following-stages-NOTRUN" in candidate, f"{name}: failure guards changed")
        ensure("readiness" in candidate.lower() and "native" in candidate.lower(), f"{name}: protected readiness/native region changed")
        ensure("P2_ALLOCATED_PORT" in candidate or "P3_ALLOCATED_PORT" in candidate, f"{name}: allocated-port stage changed")
        ensure('ASTRID_AGENT_PYTHON="$CPY"' in candidate, f"{name}: Agent interpreter binding is not consumed")
        ensure('ASTRID_RUNTIME_PYTHON="$RCPY"' in candidate, f"{name}: Runtime interpreter binding is not consumed")
        ensure(result["launch_bindings"] == {"Agent": "CPY", "Runtime": "RCPY"}, f"{name}: launch binding contract changed")
        assert_launch_bindings(binding, result, stage)
        ensure("childvenv-" not in candidate[start:replacement_end] and "CHILD_PATH" not in candidate[start:replacement_end], f"{name}: child binding leaked")
        ensure(hashlib.sha256(template[:start].encode()).hexdigest() == result["protected_prefix_sha256"], f"{name}: prefix hash changed")
        ensure(hashlib.sha256(template[end:].encode()).hexdigest() == result["protected_suffix_sha256"], f"{name}: suffix hash changed")
        import tempfile
        with tempfile.TemporaryDirectory(prefix="working-service-binding-") as directory:
            path = Path(directory) / f"{name}.sh"
            path.write_text(candidate, encoding="utf-8")
            checked = subprocess.run(["bash", "-n", str(path)], text=True, capture_output=True, check=False)
            ensure(checked.returncode == 0, checked.stderr)
        reports[name] = {
            "source_sha256": result["source_sha256"],
            "body_sha256": result["body_sha256"],
            "environment_region_sha256": result["environment_region_sha256"],
            "environment_region_bytes": result["environment_region_bytes"],
            "protected_prefix_sha256": result["protected_prefix_sha256"],
            "protected_suffix_sha256": result["protected_suffix_sha256"],
        }

    p2 = template_rows[binding.P2_TEMPLATE][1]
    for path in (
        ("source", "agent", "head"),
        ("source", "agent", "tree"),
        ("source", "runtime", "head"),
        ("source", "app", "head"),
    ):
        mutated = copy.deepcopy(base)
        mutated[path[0]][path[1]][path[2]] = "0" * 40
        assert_refusal(binding, mutated, "2", p2, "stale source/ref/tree")
    for role in ("agent", "runtime", "app"):
        mutated = copy.deepcopy(base)
        mutated["source"][role]["parents"] = list(reversed(mutated["source"][role]["parents"]))
        assert_refusal(binding, mutated, "2", p2, f"wrong parent order: {role}")
        mutated = copy.deepcopy(base)
        mutated["source"][role]["parents"][0] = "0" * 40
        assert_refusal(binding, mutated, "2", p2, f"stale parent: {role}")
        mutated = copy.deepcopy(base)
        mutated["source"][role]["ref"] = "origin/main"
        assert_refusal(binding, mutated, "2", p2, f"wrong source ref: {role}")
    for section, key in (("client_contract", "schema_digest"), ("composition", "file_map_sha256"), ("remotion", "current_agent_remotion_tree")):
        mutated = copy.deepcopy(base)
        mutated[section][key] = "0" * (64 if key.endswith("digest") or key == "file_map_sha256" else 40)
        assert_refusal(binding, mutated, "2", p2, f"stale {section}.{key}")
    for name in binding._CLIENT_FILES:
        mutated = copy.deepcopy(base)
        mutated["client_contract"]["files"][name] = "0" * 64
        assert_refusal(binding, mutated, "2", p2, f"arbitrary client digest: {name}")
    for name in binding._RUNTIME_ARTIFACTS:
        mutated = copy.deepcopy(base)
        mutated["client_contract"]["runtime_artifacts"][name] = "0" * 64
        assert_refusal(binding, mutated, "2", p2, f"arbitrary Runtime artifact digest: {name}")
    mutated = copy.deepcopy(base)
    mutated["source"]["agent"]["head"] = "9b055a93ff15fce0a2e80f2647d47743b1fc4c33"
    assert_refusal(binding, mutated, "2", p2, "intermediate Agent source is not final integration head")
    mutated = copy.deepcopy(base)
    mutated["environment"]["ASTRID_NODE_EXECUTABLE"] = "/tmp/stale-node"
    assert_refusal(binding, mutated, "2", p2, "stale node origin")
    mutated = copy.deepcopy(base)
    mutated["remotion"]["historical_source_commit_marker"] = mutated["source"]["agent"]["head"]
    assert_refusal(binding, mutated, "2", p2, "historical child as current")
    for name, (_outer, template) in template_rows.items():
        stage = "2" if name == binding.P2_TEMPLATE else "3"
        marker = f'if test -n "$P{stage}FAIL"; then'
        assert_template_refusal(binding, base, template.replace(marker, marker + "\n" + marker, 1), stage, f"duplicate {marker} boundary")
        assert_template_refusal(binding, base, template.replace("STORE_ROOT=", marker + "\nSTORE_ROOT=", 1), stage, f"injected earlier {marker} boundary")
        assert_template_refusal(binding, base, template.replace(f"$P{stage}FAIL", f"$P{stage}FAIL $P{stage}FAIL", 1), stage, f"duplicate P{stage}FAIL marker")
        assert_template_refusal(binding, base, "X" + template[1:], stage, f"protected prefix mutation: {name}")
        assert_template_refusal(binding, base, template[:-1] + "X", stage, f"protected suffix mutation: {name}")

    print(json.dumps({"status": "PASS", "controls": reports, "live_execution": "NOT_RUN"}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"working-service-binding-control: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
