#!/usr/bin/env python3
"""Prepare, but never submit, the current-head P1 source-mode caller.

The emitted shell is the existing mounted-App journey.  This module only
authenticates its source inputs and emits the command; it does not install,
launch, connect to, or execute any service, browser, HTTP, native, or backend.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
AGENT = Path("/home/user/work/agent")
RUNTIME = Path("/home/user/work/runtime")
AGENT_PYTHON = Path("/home/user/work/venv-agent/bin/python")
RUNTIME_PYTHON = Path("/home/user/work/venv-runtime/bin/python")
FACTS_PATH = HERE / "p1-current-caller-facts.json"
NORMAL_REF = "tl/integration"
P1_BODY = HERE / "tests/e2e/local/three-products.p1-chain.spec.ts"
P1_BODY_RELATIVE = "tests/e2e/local/three-products.p1-chain.spec.ts"
P1_TARGET = (
    "npm",
    "run",
    "test:e2e:three-products",
    "--",
    P1_BODY_RELATIVE,
)
ALLOWED_APP_CHANGES = {"p1-current-caller.py", "p1-current-caller-facts.json"}
FORBIDDEN_SHELL_TEXT = (
    "npm install",
    "npm ci",
    "pip install",
    "git push",
    "git reset",
    "git checkout",
    "rm -rf",
    "curl ",
    "wget ",
)


class PreparedError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PreparedError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    require(path.is_file() and not path.is_symlink(), f"regular file required: {path}")
    return sha256_bytes(path.read_bytes())


def canonical_sha(value: Any) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    require(result.returncode == 0, f"git check failed at {root}: {result.stderr.strip()}")
    return result.stdout.strip()


def load_facts() -> dict[str, Any]:
    try:
        facts = json.loads(FACTS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PreparedError(f"cannot read facts: {exc}") from exc
    require(isinstance(facts, dict), "facts must be an object")
    require(facts.get("status") == "PREPARED", "facts are not PREPARED")
    require(facts.get("submitted") is False, "submitted caller is refused")
    return facts


def expected_for_negative(facts: dict[str, Any], name: str | None) -> dict[str, Any]:
    if name is None:
        return facts
    value = json.loads(json.dumps(facts))
    if name == "wrong-source":
        value["integrations"]["agent"]["source"] = "0" * 40
    elif name == "tree":
        value["integrations"]["agent"]["tree"] = "0" * 40
    elif name == "parent":
        value["integrations"]["runtime"]["parents"] = ["0" * 40]
    elif name == "lock":
        value["locks"]["app"]["file_sha256"] = "0" * 64
    elif name == "target":
        value["target"]["command"] = ["forged-target"]
    elif name == "body":
        value["spec"]["sha256"] = "0" * 64
    elif name == "poison":
        value["poison_marker"] = "do-not-execute"
    else:
        raise PreparedError(f"unknown negative: {name}")
    return value


def assert_source_snapshot(facts: dict[str, Any]) -> None:
    app = facts["source"]
    require(app["checkout"] == str(HERE), "App source checkout changed")
    require(app["ref"] == NORMAL_REF, "App source ref changed")
    expected_commit = app["commit"]
    expected_tree = app["tree"]
    require(git(HERE, "show", "-s", "--format=%H", expected_commit) == expected_commit, "App source commit missing")
    require(git(HERE, "show", "-s", "--format=%T", expected_commit) == expected_tree, "App source tree changed")
    require(
        git(HERE, "show", "-s", "--format=%P", expected_commit).split() == app["parents"],
        "App source parents changed",
    )
    current = git(HERE, "rev-parse", "HEAD")
    current_tree = git(HERE, "rev-parse", "HEAD^{tree}")
    if current != expected_commit:
        require(
            git(HERE, "merge-base", "--is-ancestor", expected_commit, current) == "",
            "App is neither the bound source nor its descendant",
        )
        changed = set(git(HERE, "diff", "--name-only", f"{expected_commit}..{current}").splitlines())
        require(changed <= ALLOWED_APP_CHANGES, "later App snapshot contains unowned changes")
    else:
        require(current_tree == expected_tree, "App source tree changed")
    status = git(HERE, "status", "--porcelain=v1", "--untracked-files=all")
    changed_status = {line[3:] for line in status.splitlines() if len(line) >= 4}
    require(changed_status <= ALLOWED_APP_CHANGES, "App worktree contains unowned changes")


def assert_integration(label: str, root: Path, facts: dict[str, Any]) -> None:
    require(root.is_dir() and not root.is_symlink(), f"{label} checkout unavailable")
    expected = facts["integrations"][label.lower()]
    require(git(root, "rev-parse", "--show-toplevel") == str(root), f"{label} checkout root changed")
    require(git(root, "symbolic-ref", "--short", "HEAD") == NORMAL_REF, f"{label} ref changed")
    require(git(root, "rev-parse", "HEAD") == expected["source"], f"{label} source moved")
    require(git(root, "rev-parse", "HEAD^{tree}") == expected["tree"], f"{label} tree moved")
    require(git(root, "show", "-s", "--format=%P", "HEAD").split() == expected["parents"], f"{label} parents moved")
    require(not git(root, "status", "--porcelain=v1", "--untracked-files=all"), f"{label} checkout is dirty")


def assert_locks(facts: dict[str, Any]) -> None:
    for label, root in (("app", HERE), ("agent", AGENT)):
        path = root / "runtime.lock.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        expected = facts["locks"][label]
        require(sha256_file(path) == expected["file_sha256"], f"{label} lock changed")
        require(canonical_sha(value["files"]) == expected["files_sha256"], f"{label} lock mappings changed")
        require(value["source_commit"] == facts["integrations"]["runtime"]["source"], f"{label} lock producer changed")
        require(value["producer_version"] == expected["producer_version"], f"{label} producer version changed")
        require(len(value["files"]) == expected["file_count"], f"{label} lock mapping count changed")


def probe(python: Path, roots: str, modules: list[str]) -> dict[str, Any]:
    code = (
        "import importlib.metadata as md, importlib.util, json, sys; "
        "from pathlib import Path; "
        "names = json.loads(sys.argv[1]); "
        "print(json.dumps({'python': str(Path(sys.executable).resolve()), "
        "'imports': {name: (str(Path(spec.origin).resolve()) if (spec := importlib.util.find_spec(name)) and spec.origin else None) for name in names}, "
        "'versions': {name: (md.version(name) if name in {d.metadata['Name'] for d in md.distributions()} else None) for name in ['astrid', 'astrid-runtime', 'banodoco-timeline-schema']}}))"
    )
    result = subprocess.run(
        [str(python), "-c", code, json.dumps(modules)],
        check=False,
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": roots},
    )
    require(result.returncode == 0, f"{python} import probe refused")
    return json.loads(result.stdout)


def assert_interpreters(facts: dict[str, Any]) -> None:
    for role, python, roots, modules in (
        ("agent", AGENT_PYTHON, str(AGENT), ["astrid", "astrid_runtime_client"]),
        ("runtime", RUNTIME_PYTHON, str(RUNTIME), ["astrid_runtime", "runtime_protocol"]),
    ):
        expected = facts["interpreters"][role]
        require(python.is_file() and python.stat().st_mode & 0o111, f"{role} interpreter unavailable")
        actual = probe(python, roots, modules)
        require(actual == expected, f"{role} interpreter/import origins changed")


def assert_artifacts(facts: dict[str, Any]) -> None:
    remotion = facts["remotion"]
    require(git(AGENT, "rev-parse", "HEAD:remotion") == remotion["tree"], "Remotion source graph changed")
    require(sha256_file(AGENT / "remotion/package-lock.json") == remotion["package_lock_sha256"], "Remotion lock changed")
    for path_text, digest in facts["runtime_artifacts"].items():
        require(sha256_file(Path(path_text)) == digest, f"Runtime artifact changed: {path_text}")
    composition = facts["composition"]
    require(sha256_file(Path(composition["artifact"])) == composition["artifact_sha256"], "Composition artifact changed")
    graph = Path(composition["graph"])
    require(graph.is_dir() and not graph.is_symlink(), "approved Composition graph unavailable")
    files = {str(path.relative_to(graph)): sha256_file(path) for path in graph.rglob("*") if path.is_file()}
    require(len(files) == composition["file_count"], "Composition graph file count changed")
    require(canonical_sha(files) == composition["file_map_sha256"], "Composition graph bytes changed")


def assert_spec(facts: dict[str, Any]) -> None:
    spec = facts["spec"]
    require(P1_BODY.is_file(), "P1 spec is unavailable")
    require(sha256_file(P1_BODY) == spec["sha256"], "P1 spec body changed")
    require(git(HERE, "hash-object", P1_BODY_RELATIVE) == spec["git_blob"], "P1 spec Git blob changed")
    text = P1_BODY.read_text(encoding="utf-8")
    for title in spec["case_titles"]:
        require(f"test('{title}'" in text, f"P1 case missing: {title}")
    require(text.count("test('P1 split -> trim new clip:") == 2, "P1 case count changed")


def assert_wire(facts: dict[str, Any]) -> None:
    wire = facts["wire_contract"]
    require(wire["route"] == "/v1/projects/{project_id}/timelines/{timeline_id}/commit", "commit route changed")
    require(wire["request_headers"] == ["Idempotency-Key"], "commit header changed")
    require(set(wire["request_fields"]) >= {
        "api_version", "project_id", "timeline_id", "base_revision_id", "base_publication_id",
        "commands", "label", "steps", "merge", "reads", "source", "rationale", "group_id", "dry_run",
    }, "request closure is incomplete")
    require(set(wire["command_fields"]) == {"schema_version", "op", "version", "select", "args", "created"}, "command closure changed")
    require(set(wire["step_fields"]) == {"id", "label", "intent", "tags", "command_ordinals", "patch", "reads"}, "step closure changed")
    require(set(wire["reply_fields"]) >= {
        "data", "receipt", "status", "canonical_document", "document_digest", "id_map", "commands", "steps",
        "dependencies", "base_revision_id", "previous_revision_id", "accepted_revision_id", "provider_version",
        "compiler_version", "publisher", "receipt_id", "idempotency_key", "history", "guarded_undo",
    }, "reply closure is incomplete")
    require(set(wire["statuses"]) >= {"accepted", "merged", "conflict", "invalid", "dryrun"}, "reply statuses incomplete")


def validate(facts: dict[str, Any], negative: str | None = None) -> None:
    require(not facts.get("poison_marker"), "poison marker refused")
    require(facts["target"]["command"] == list(P1_TARGET), "execution target changed")
    assert_source_snapshot(facts)
    assert_integration("Agent", AGENT, facts)
    assert_integration("Runtime", RUNTIME, facts)
    assert_locks(facts)
    assert_interpreters(facts)
    assert_artifacts(facts)
    assert_spec(facts)
    assert_wire(facts)
    require(facts["chronology"]["future_snapshot_required"] is False, "future snapshot requirement is not allowed")
    require(facts["chronology"]["historical_caller_reused"] is False, "historical caller reuse is refused")
    require(facts["execution"]["submitted"] is False, "submission is outside this preparation")
    require(negative is None, "negative mutation was not refused")


def shell(facts: dict[str, Any]) -> str:
    source = facts["source"]
    agent = facts["integrations"]["agent"]
    runtime = facts["integrations"]["runtime"]
    body_sha = facts["spec"]["sha256"]
    target = " ".join(P1_TARGET)
    script = f'''#!/usr/bin/env bash
set -euo pipefail

# PREPARED only: this is the one authorized next mechanical step.  Running it
# is intentionally outside this preparation artifact.
APP_ROOT={str(HERE)!r}
AGENT_ROOT={str(AGENT)!r}
RUNTIME_ROOT={str(RUNTIME)!r}
EXPECTED_APP={source["commit"]!r}
EXPECTED_AGENT={agent["source"]!r}
EXPECTED_RUNTIME={runtime["source"]!r}
EXPECTED_BODY_SHA={body_sha!r}
fail() {{ echo "P1 current caller refused: $1" >&2; exit 2; }}
test "$(git -C "$APP_ROOT" merge-base --is-ancestor "$EXPECTED_APP" HEAD >/dev/null 2>&1; echo $?)" = 0 || fail App-source-freshness
test "$(git -C "$AGENT_ROOT" rev-parse HEAD)" = "$EXPECTED_AGENT" || fail Agent-source-freshness
test "$(git -C "$RUNTIME_ROOT" rev-parse HEAD)" = "$EXPECTED_RUNTIME" || fail Runtime-source-freshness
test "$(sha256sum "$APP_ROOT/{P1_BODY_RELATIVE}" | cut -d' ' -f1)" = "$EXPECTED_BODY_SHA" || fail P1-body-freshness
test "$(git -C "$AGENT_ROOT" status --porcelain=v1 --untracked-files=all)" = "" || fail Agent-dirty
test "$(git -C "$RUNTIME_ROOT" status --porcelain=v1 --untracked-files=all)" = "" || fail Runtime-dirty
cd "$APP_ROOT"
env -u NODE_PATH -u PYTHONHOME \\
  ASTRID_CHECKOUT="$AGENT_ROOT" \\
  ASTRID_PYTHON="{str(AGENT_PYTHON)}" \\
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME_ROOT" \\
  ASTRID_RUNTIME_PYTHON="{str(RUNTIME_PYTHON)}" \\
  TIMELINE_BUNDLE_AGENT_HEAD="$EXPECTED_AGENT" \\
  TIMELINE_BUNDLE_RUNTIME_HEAD="$EXPECTED_RUNTIME" \\
  PYTHONPATH="$APP_ROOT:$RUNTIME_ROOT:$AGENT_ROOT" \\
  {target}
'''
    for forbidden in FORBIDDEN_SHELL_TEXT:
        require(forbidden not in script, f"forbidden shell text: {forbidden}")
    return script


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-source", action="store_true", help="authenticate sources and emit the unrun shell")
    parser.add_argument(
        "--negative",
        choices=("wrong-source", "tree", "parent", "lock", "target", "body", "poison"),
        help="exercise one refusal control",
    )
    args = parser.parse_args()
    if not args.dry_source and args.negative is None:
        parser.error("use --dry-source; the caller is not submitted by this artifact")
    facts = load_facts()
    candidate = expected_for_negative(facts, args.negative)
    try:
        validate(candidate, args.negative)
        output = shell(candidate)
    except PreparedError as exc:
        if args.negative is not None:
            print(f"EXPECTED_REFUSAL {args.negative}: {exc}", file=sys.stderr)
            return 0
        print(f"PREPARED refusal: {exc}", file=sys.stderr)
        return 2
    if args.negative is not None:
        print(f"NEGATIVE_NOT_REFUSED {args.negative}", file=sys.stderr)
        return 2
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
