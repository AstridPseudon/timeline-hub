"""Fast, read-only identity qualification for a decoded caller row."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import base64
import re


class DryPreflightError(RuntimeError):
    """The candidate cannot be authenticated without entering the live phase."""


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise DryPreflightError(f"dry-preflight git identity failed: {root}: {exc}") from exc


def _physical(path: Path, *, directory: bool = False) -> Path:
    if not path.is_absolute() or path.is_symlink() or path.resolve() != path:
        raise DryPreflightError(f"dry-preflight nonphysical path: {path}")
    if any(parent.is_symlink() for parent in path.parents):
        raise DryPreflightError(f"dry-preflight symlinked parent: {path}")
    if directory and not path.is_dir():
        raise DryPreflightError(f"dry-preflight directory is unavailable: {path}")
    if not directory and not path.is_file():
        raise DryPreflightError(f"dry-preflight file is unavailable: {path}")
    return path


def _receipt(path: Path, expected_sha256: str) -> str:
    path = _physical(path)
    if _digest(path.read_bytes()) != expected_sha256:
        raise DryPreflightError(f"dry-preflight receipt changed: {path}")
    return path.read_text()


def _extract_inner(row: bytes) -> tuple[str, str]:
    try:
        outer = row.decode().split(None, 2)[2].rstrip("\n")
        start = outer.index("$(bash -c ") + len("$(bash -c ")
        end = outer.index(")\" && eval", start)
        import shlex

        decoded = shlex.split(outer[start:end])
    except (IndexError, ValueError, UnicodeDecodeError) as exc:
        raise DryPreflightError(f"dry-preflight wrapped caller cannot be decoded: {exc}") from exc
    if len(decoded) != 1:
        raise DryPreflightError("dry-preflight wrapped caller has an ambiguous decoded body")
    return outer, decoded[0]


def _syntax(text: str, label: str) -> None:
    result = subprocess.run(["/bin/bash", "-n"], input=text, text=True, capture_output=True, check=False)
    if result.returncode:
        raise DryPreflightError(f"dry-preflight {label} is not valid bash: {result.stderr.strip()}")


def _row_bindings(inner: str, expected: dict[str, object]) -> None:
    n = str(expected["stage"])
    agent = expected["agent"]
    runtime = expected["runtime"]
    app = expected["app"]
    required = {
        f"P{n}A": agent["source"],
        f"P{n}R": runtime["source"],
        f"P{n}APP": app["source"],
        f"P{n}TREE": app["tree"],
        f"P{n}PARENT": f"'{app['parent']}'",
        f"P{n}AG": f"${{P{n}_AGENT_CHECKOUT:-{agent['checkout']}}}",
        f"P{n}RT": f"${{P{n}_RUNTIME_CHECKOUT:-{runtime['checkout']}}}",
        "CN": expected["child"]["name"],
        "RN": expected["remotion"]["name"],
    }
    missing = [f"{key}={value}" for key, value in required.items() if f"{key}={value}" not in inner]
    if missing:
        raise DryPreflightError(f"dry-preflight decoded source binding mismatch: {missing}")
    if inner.count(agent["source"]) < 1 or inner.count(runtime["source"]) < 1:
        raise DryPreflightError("dry-preflight actual Agent/Runtime source identity is absent")


def _read_only_guard(inner: str, expected: dict[str, object]) -> str:
    n = str(expected["stage"])
    marker = f'printf "%s\\n" "$P{n}APP"'
    start = inner.find(marker)
    if start < 0:
        raise DryPreflightError("dry-preflight decoded source has no App identity guard")
    end_marker = f'if test -n "$P{n}FAIL"; then'
    end = inner.find(end_marker, start)
    if end < 0:
        raise DryPreflightError("dry-preflight decoded source has no fail-closed identity boundary")
    end = inner.find("fi;", end)
    if end < 0:
        raise DryPreflightError("dry-preflight decoded source has no completed identity guard")
    guard = inner[start : end + len("fi;")]
    encoded = re.findall(r'base64\.b64decode\(\\"([A-Za-z0-9+/=]+)', guard)
    if len(encoded) != 1:
        raise DryPreflightError("dry-preflight custody guard is missing or ambiguous")
    try:
        custody_guard = base64.b64decode(encoded[0], validate=True).decode()
    except (ValueError, UnicodeDecodeError) as exc:
        raise DryPreflightError("dry-preflight custody guard is not valid encoded source") from exc
    historic = expected["remotion"]["producer"]
    if f"marker(runtime_path, \".astrid-agent-source-commit\") != '{historic}'" not in custody_guard:
        raise DryPreflightError("dry-preflight retained Remotion producer identity is absent")
    forbidden = (
        "mkdir ",
        "npm run",
        "node --import",
        "startDirectHarness",
        "P2_ALLOCATED_PORT",
        "P3_ALLOCATED_PORT",
        "PLAYWRIGHT_OUTPUT_DIR",
        "curl ",
        "nc ",
        "listen(",
    )
    if any(token in guard for token in forbidden):
        raise DryPreflightError("dry-preflight identity guard contains live/setup work")
    return guard


def _target_identity(target: Path, app: dict[str, object]) -> dict[str, str]:
    target = _physical(target, directory=True)
    if any((target / name).exists() for name in ("caller-publication.py", "caller-custody.json", "caller-dry-preflight.py")):
        raise DryPreflightError("dry-preflight target is a caller artifact")
    if _git(target, "status", "--porcelain=v1", "--untracked-files=all"):
        raise DryPreflightError("dry-preflight target is dirty")
    if _git(target, "rev-parse", "--abbrev-ref", "HEAD") != "HEAD":
        raise DryPreflightError("dry-preflight target is not a detached checkout")
    source = str(app["source"])
    tree = str(app["tree"])
    parent = str(app["parent"])
    if _git(target, "rev-parse", f"{source}^{{commit}}") != source:
        raise DryPreflightError("dry-preflight target cannot resolve approved App source")
    if _git(target, "rev-parse", "HEAD^{tree}") != tree:
        raise DryPreflightError("dry-preflight target tree mismatch")
    head = _git(target, "rev-parse", "HEAD")
    parents = _git(target, "show", "-s", "--format=%P", "HEAD")
    if head != source and parents != source:
        raise DryPreflightError("dry-preflight target is not the approved source or a single-parent same-tree snapshot")
    return {"head": head, "tree": tree, "parents": parents}


def _pinned_checkout(name: str, checkout: Path, source: str, tree: str, parent: str, delta_sha256: str | None = None) -> dict[str, str]:
    checkout = _physical(checkout, directory=True)
    if _git(checkout, "status", "--porcelain=v1", "--untracked-files=all"):
        raise DryPreflightError(f"dry-preflight {name} checkout is dirty")
    if _git(checkout, "rev-parse", "HEAD") != source:
        raise DryPreflightError(f"dry-preflight {name} source mismatch")
    actual_tree = _git(checkout, "show", "-s", "--format=%T", source)
    actual_parent = _git(checkout, "show", "-s", "--format=%P", source)
    if actual_tree != tree or actual_parent != parent:
        raise DryPreflightError(f"dry-preflight {name} tree/parent mismatch")
    if delta_sha256 is not None:
        delta = subprocess.check_output(["git", "-C", str(checkout), "diff", "--binary", "--full-index", "--no-ext-diff", parent, source])
        if _digest(delta) != delta_sha256:
            raise DryPreflightError(f"dry-preflight {name} reviewed delta mismatch")
    return {"source": source, "tree": actual_tree, "parent": actual_parent, "checkout": str(checkout)}


def _custody(expected: dict[str, object]) -> dict[str, object]:
    agent = expected["agent"]
    runtime = expected["runtime"]
    app = expected["app"]
    child = expected["child"]
    remotion = expected["remotion"]
    _pinned_checkout("Agent", Path(agent["checkout"]), agent["source"], agent["tree"], agent["parent"], agent["delta_sha256"])
    _pinned_checkout("Runtime", Path(runtime["checkout"]), runtime["source"], runtime["tree"], runtime["parent"])
    _receipt(Path(agent["receipt"]), agent["receipt_sha256"])
    _receipt(Path(app["checkout_receipt"]), app["checkout_receipt_sha256"])
    _receipt(Path(app["source_report"]), app["source_report_sha256"])
    _receipt(Path(remotion["receipt"]), remotion["receipt_sha256"])
    for key in ("maker_receipt", "provision_receipt", "import_receipt"):
        _receipt(Path(child[key]), child[f"{key}_sha256"])
    child_root = _physical(Path(child["root"]), directory=True)
    marker = child_root / ".astrid-source-commit"
    if not marker.is_file() or marker.read_text().strip() != agent["source"]:
        raise DryPreflightError("dry-preflight child source marker mismatch")
    remotion_root = _physical(Path(remotion["root"]), directory=True)
    graph = remotion_root / "node_modules/@banodoco/timeline-composition"
    files = sorted(path for path in graph.rglob("*") if path.is_file())
    graph_digest = _digest(
        json.dumps(
            {str(path.relative_to(graph)): _digest(path.read_bytes()) for path in files},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    )
    if len(files) != remotion["component_file_count"] or graph_digest != remotion["component_tree_digest"]:
        raise DryPreflightError("dry-preflight Remotion component tree mismatch")
    return {
        "app": {"source": app["source"], "tree": app["tree"], "parent": app["parent"]},
        "agent": {"source": agent["source"], "tree": agent["tree"], "parent": agent["parent"]},
        "runtime": {"source": runtime["source"], "tree": runtime["tree"], "parent": runtime["parent"]},
        "child": {"name": child["name"], "key": child["key"]},
        "remotion": {"name": remotion["name"], "producer": remotion["producer"], "tree": remotion["tree"]},
        "component_tree_digest": graph_digest,
    }


def dry_preflight(row: bytes, *, target: Path, expected: dict[str, object]) -> dict[str, object]:
    """Authenticate one candidate row and its exact read-only custody context."""
    started = time.monotonic()
    outer, inner = _extract_inner(row)
    _syntax(outer, "wrapped caller")
    _syntax(inner, "decoded caller")
    _row_bindings(inner, expected)
    guard = _read_only_guard(inner, expected)
    target_facts = _target_identity(target, expected["app"])
    custody_facts = _custody(expected)
    n = str(expected["stage"])
    prefix = [
        "set -u",
        f"P{n}O={expected['orch']!s}",
        f"P{n}A={expected['agent']['source']}",
        f"P{n}R={expected['runtime']['source']}",
        f"P{n}APP={expected['app']['source']}",
        f"P{n}TREE={expected['app']['tree']}",
        f"P{n}PARENT={expected['app']['parent']!r}",
        f"P{n}AG={expected['agent']['checkout']}",
        f"P{n}RT={expected['runtime']['checkout']}",
        f"CN={expected['child']['name']}",
        f"RN={expected['remotion']['name']}",
        f"P{n}FAIL=",
        f"p{n.lower()}fail() {{ P{n}FAIL=\"$P{n}FAIL $1\"; }}",
        guard,
    ]
    result = subprocess.run(
        ["/bin/bash", "-c", "\n".join(prefix)],
        cwd=target,
        env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C"},
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip().splitlines()[-1:]
        raise DryPreflightError(f"dry-preflight actual identity guard refused: {detail}")
    elapsed = time.monotonic() - started
    return {
        "status": "PASS",
        "duration_seconds": round(elapsed, 3),
        "returncode": result.returncode,
        "target": target_facts,
        "custody": custody_facts,
        "guard": {"decoded": True, "wrapped": True, "read_only": True, "setup_stages_not_run": True},
    }
