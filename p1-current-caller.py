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
import shlex
from typing import Any


HERE = Path(__file__).resolve().parent
APP = Path("/home/user/work/app")
AGENT = Path("/home/user/work/agent")
RUNTIME = Path("/home/user/work/runtime")
AGENT_PYTHON = Path("/home/user/work/venv-agent/bin/python")
RUNTIME_PYTHON = Path("/home/user/work/venv-runtime/bin/python")
REMOTION_ROOT = Path("/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830")
REMOTION_NODE = REMOTION_ROOT / ".toolchain/node-v20.19.4-linux-x64/bin/node"
REMOTION_NPM = REMOTION_ROOT / ".toolchain/node-v20.19.4-linux-x64/bin/npm"
REMOTION_PROJECT = Path(
    "/home/user/work/bench-store/entries/"
    "runtime-5ca5c561b7be7069051ac8769432cc1edf29060bed39384cd3c4ecab1736e690"
)
FACTS_PATH = HERE / "p1-current-caller-facts.json"
NORMAL_REF = "tl/integration"
APP_TARGET_REF = "tl/app-P2-P3-e68-current-pure-target-1409"
P1_BODY = APP / "tests/e2e/local/three-products.p1-chain.spec.ts"
P1_BODY_RELATIVE = "tests/e2e/local/three-products.p1-chain.spec.ts"
P1_TARGET = (
    "npm",
    "run",
    "test:e2e:three-products",
    "--",
    P1_BODY_RELATIVE,
)
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
    if name in {"wrong-source", "wrongsource"}:
        value["source"]["commit"] = "0" * 40
    elif name == "tree":
        value["source"]["tree"] = "0" * 40
    elif name in {"parent", "parents"}:
        value["source"]["parents"] = ["0" * 40]
    elif name == "lock":
        value["locks"]["app"]["file_sha256"] = "0" * 64
    elif name == "locks":
        value["locks"]["agent"]["file_sha256"] = "0" * 64
    elif name == "clients":
        value["clients"]["files"]["src/integrations/runtime/generated.ts"] = "0" * 64
    elif name == "import":
        value["interpreters"]["agent"]["imports"]["astrid"] = "/forged/astrid.py"
    elif name == "interpreters":
        value["interpreters"]["runtime"]["python"] = "/forged/python"
    elif name == "graph":
        value["composition"]["file_map_sha256"] = "0" * 64
    elif name == "target":
        value["target"]["command"] = ["forged-target"]
    elif name == "body":
        value["spec"]["sha256"] = "0" * 64
    elif name == "poison":
        value["poison_marker"] = "do-not-execute"
    elif name in {"stage", "missing-stage", "stale-stage"}:
        value["stages"]["source"]["files"] = []
    else:
        raise PreparedError(f"unknown negative: {name}")
    return value


def assert_source_snapshot(facts: dict[str, Any]) -> None:
    app = facts["source"]
    require(app["checkout"] == str(APP), "App source checkout changed")
    require(APP.is_dir() and not APP.is_symlink() and APP.resolve() == APP, "App source checkout is not stable")
    require(app["ref"] == NORMAL_REF, "App source ref changed")
    expected_commit = app["commit"]
    expected_tree = app["tree"]
    require(git(APP, "show", "-s", "--format=%H", expected_commit) == expected_commit, "App source commit missing")
    require(git(APP, "show", "-s", "--format=%T", expected_commit) == expected_tree, "App source tree changed")
    require(
        git(APP, "show", "-s", "--format=%P", expected_commit).split() == app["parents"],
        "App source parents changed",
    )
    require(git(APP, "rev-parse", "HEAD") == expected_commit, "App source moved")
    require(git(APP, "rev-parse", "HEAD^{tree}") == expected_tree, "App source tree changed")
    require(git(APP, "symbolic-ref", "--short", "HEAD") == app["ref"], "App source ref changed")
    require(git(APP, "rev-parse", f"refs/heads/{NORMAL_REF}") == expected_commit, "App normal ref moved")
    authority = app["authority"]
    require(authority["ref"] == APP_TARGET_REF, "App target ref changed")
    require(authority["commit"] == expected_commit, "App target commit changed")
    require(authority["tree"] == expected_tree, "App target metadata tree changed")
    require(authority["parents"] == app["parents"], "App target metadata parents changed")
    require(git(APP, "rev-parse", f"refs/heads/{authority['ref']}") == expected_commit, "App target ref moved")
    require(git(APP, "show", "-s", "--format=%T", authority["ref"]) == expected_tree, "App target tree changed")
    require(git(APP, "show", "-s", "--format=%P", authority["ref"]).split() == app["parents"], "App target parents changed")
    require(not git(APP, "status", "--porcelain=v1", "--untracked-files=all"), "App source is dirty")


def assert_integration(label: str, root: Path, facts: dict[str, Any]) -> None:
    require(root.is_dir() and not root.is_symlink() and root.resolve() == root, f"{label} checkout unavailable")
    expected = facts["integrations"][label.lower()]
    require(git(root, "rev-parse", "--show-toplevel") == str(root), f"{label} checkout root changed")
    require(git(root, "symbolic-ref", "--short", "HEAD") == NORMAL_REF, f"{label} ref changed")
    require(git(root, "rev-parse", f"refs/heads/{NORMAL_REF}") == expected["source"], f"{label} normal ref moved")
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


def assert_clients(facts: dict[str, Any]) -> None:
    for relative, expected in facts["clients"]["files"].items():
        require(sha256_file(APP / relative) == expected, f"client source changed: {relative}")


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
        require(str(python) == expected["command"], f"{role} interpreter command changed")
        actual = probe(python, roots, modules)
        require(actual == {key: value for key, value in expected.items() if key != "command"}, f"{role} interpreter/import origins changed")


def assert_artifacts(facts: dict[str, Any]) -> None:
    remotion = facts["remotion"]
    require(git(AGENT, "rev-parse", "HEAD:remotion") == remotion["tree"], "Remotion source graph changed")
    require(sha256_file(AGENT / "remotion/package-lock.json") == remotion["package_lock_sha256"], "Remotion lock changed")
    require(sha256_file(AGENT / "remotion/package.json") == remotion["package_sha256"], "Remotion package changed")
    require(REMOTION_NODE.is_file() and REMOTION_NODE.stat().st_mode & 0o111, "Remotion Node unavailable")
    require(REMOTION_NPM.is_file() and REMOTION_NPM.stat().st_mode & 0o111, "Remotion npm unavailable")
    node = subprocess.run([str(REMOTION_NODE), "--version"], check=False, capture_output=True, text=True)
    npm = subprocess.run(
        [str(REMOTION_NPM), "--version"],
        check=False,
        capture_output=True,
        text=True,
        env={"PATH": f"{REMOTION_NODE.parent}:/usr/bin:/bin"},
    )
    require(node.returncode == 0 and node.stdout.strip() == remotion["node"], "Remotion Node changed")
    require(npm.returncode == 0 and npm.stdout.strip() == remotion["npm"], "Remotion npm changed")
    for path_text, digest in facts["runtime_artifacts"].items():
        require(sha256_file(Path(path_text)) == digest, f"Runtime artifact changed: {path_text}")
    composition = facts["composition"]
    require(sha256_file(Path(composition["artifact"])) == composition["artifact_sha256"], "Composition artifact changed")
    graph = Path(composition["graph"])
    require(graph.is_dir() and not graph.is_symlink() and graph.resolve() == graph, "approved Composition graph unavailable")
    files = {str(path.relative_to(graph)): sha256_file(path) for path in graph.rglob("*") if path.is_file() and not path.is_symlink()}
    require(len(files) == composition["file_count"], "Composition graph file count changed")
    require(canonical_sha(files) == composition["file_map_sha256"], "Composition graph bytes changed")
    package = graph / "package.json"
    require(sha256_file(package) == composition["package_sha256"], "Composition package changed")
    require(json.loads(package.read_text(encoding="utf-8"))["version"] == composition["version"], "Composition version changed")


def assert_spec(facts: dict[str, Any]) -> None:
    spec = facts["spec"]
    require(P1_BODY.is_file(), "P1 spec is unavailable")
    require(sha256_file(P1_BODY) == spec["sha256"], "P1 spec body changed")
    require(git(APP, "hash-object", P1_BODY_RELATIVE) == spec["git_blob"], "P1 spec Git blob changed")
    text = P1_BODY.read_text(encoding="utf-8")
    for title in spec["case_titles"]:
        require(f"test('{title}'" in text, f"P1 case missing: {title}")
    require(text.count("test('P1 split -> trim new clip:") == 2, "P1 case count changed")


def assert_target(facts: dict[str, Any]) -> None:
    target = facts["target"]
    source = facts["source"]
    require(target["cwd"] == str(APP), "execution target cwd changed")
    require(target["source_ref"] == APP_TARGET_REF, "execution target ref changed")
    require(target["source_commit"] == source["commit"], "execution target commit changed")
    require(target["source_tree"] == source["tree"], "execution target tree changed")
    require(target["route"] == "mounted App -> persisted outbox -> generated commitTimeline", "execution route changed")


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
    assert_clients(facts)
    assert_interpreters(facts)
    assert_artifacts(facts)
    assert_spec(facts)
    assert_target(facts)
    assert_wire(facts)
    require(facts["chronology"]["future_snapshot_required"] is False, "future snapshot requirement is not allowed")
    require(facts["chronology"]["historical_caller_reused"] is False, "historical caller reuse is refused")
    require(facts["execution"]["submitted"] is False, "submission is outside this preparation")
    require(facts["stages"]["source"]["files"], "source stage destinations are incomplete")
    require(facts["stages"]["environment"]["files"], "environment stage destinations are incomplete")
    require(facts["stages"]["original"]["files"], "original stage destinations are incomplete")
    require(negative is None, "negative mutation was not refused")


def shell(facts: dict[str, Any]) -> str:
    source = facts["source"]
    agent = facts["integrations"]["agent"]
    runtime = facts["integrations"]["runtime"]
    q = shlex.quote
    body_sha = facts["spec"]["sha256"]
    app_parents = " ".join(source["parents"])
    agent_parents = " ".join(agent["parents"])
    runtime_parents = " ".join(runtime["parents"])
    interpreter = facts["interpreters"]
    composition = facts["composition"]
    graph_code = (
        "import hashlib,json,sys; from pathlib import Path; "
        "p=Path(sys.argv[1]); f={str(x.relative_to(p)):hashlib.sha256(x.read_bytes()).hexdigest() "
        "for x in p.rglob('*') if x.is_file() and not x.is_symlink()}; "
        "print(len(f),hashlib.sha256(json.dumps(f,sort_keys=True,separators=(',',':')).encode()).hexdigest())"
    )
    probe_code = (
        "import importlib.util,sys; from pathlib import Path; "
        "s=importlib.util.find_spec(sys.argv[1]); "
        "print(str(Path(s.origin).resolve()) if s and s.origin else '')"
    )
    full_probe_code = (
        "import importlib.metadata as md,importlib.util,json,sys; from pathlib import Path; "
        "names=json.loads(sys.argv[1]); "
        "print(json.dumps({'python':str(Path(sys.executable).resolve()),"
        "'imports':{n:(str(Path(s.origin).resolve()) if (s:=importlib.util.find_spec(n)) and s.origin else None) for n in names},"
        "'versions':{n:(md.version(n) if n in {d.metadata['Name'] for d in md.distributions()} else None) for n in ['astrid','astrid-runtime','banodoco-timeline-schema']}},sort_keys=True,separators=(',',':')))"
    )
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "# PREPARED: authenticate the stable source tuple, retain source-only records,",
        "# then invoke the unchanged two-case P1 script as the final command.",
        f"APP_ROOT={q(str(APP))}",
        f"AGENT_ROOT={q(str(AGENT))}",
        f"RUNTIME_ROOT={q(str(RUNTIME))}",
        f"REMOTION_NODE={q(str(REMOTION_NODE))}",
        f"REMOTION_NPM={q(str(REMOTION_NPM))}",
        'REMOTION_NODE_DIR="$(dirname "$REMOTION_NODE")"',
        f"COMPOSITION_GRAPH={q(str(composition['graph']))}",
        f"COMPOSITION_ARTIFACT={q(str(composition['artifact']))}",
        f"EXPECTED_APP={q(source['commit'])}",
        f"EXPECTED_APP_TREE={q(source['tree'])}",
        f"EXPECTED_APP_PARENTS={q(app_parents)}",
        f"EXPECTED_AGENT={q(agent['source'])}",
        f"EXPECTED_AGENT_TREE={q(agent['tree'])}",
        f"EXPECTED_AGENT_PARENTS={q(agent_parents)}",
        f"EXPECTED_RUNTIME={q(runtime['source'])}",
        f"EXPECTED_RUNTIME_TREE={q(runtime['tree'])}",
        f"EXPECTED_RUNTIME_PARENTS={q(runtime_parents)}",
        f"EXPECTED_BODY_SHA={q(body_sha)}",
        f"EXPECTED_REMOTION_TREE={q(facts['remotion']['tree'])}",
        f"EXPECTED_REMOTION_LOCK={q(facts['remotion']['package_lock_sha256'])}",
        f"EXPECTED_REMOTION_NODE={q(facts['remotion']['node'])}",
        f"EXPECTED_REMOTION_NPM={q(facts['remotion']['npm'])}",
        f"EXPECTED_COMPOSITION_FILES={q(str(composition['file_count']))}",
        f"EXPECTED_COMPOSITION_MAP={q(composition['file_map_sha256'])}",
        "fail() { echo \"P1 current caller refused: $1\" >&2; exit 2; }",
        'test "$(git -C "$APP_ROOT" rev-parse HEAD)" = "$EXPECTED_APP" || fail App-source',
        'test "$(git -C "$APP_ROOT" rev-parse HEAD^{tree})" = "$EXPECTED_APP_TREE" || fail App-tree',
        'test "$(git -C "$APP_ROOT" show -s --format=%P HEAD)" = "$EXPECTED_APP_PARENTS" || fail App-parents',
        f'test "$(git -C "$APP_ROOT" rev-parse refs/heads/{NORMAL_REF})" = "$EXPECTED_APP" || fail App-ref',
        f'test "$(git -C "$APP_ROOT" rev-parse refs/heads/{APP_TARGET_REF})" = "$EXPECTED_APP" || fail App-target-ref',
        'test "$(git -C "$APP_ROOT" status --porcelain=v1 --untracked-files=all)" = "" || fail App-dirty',
        'test "$(git -C "$AGENT_ROOT" rev-parse HEAD)" = "$EXPECTED_AGENT" || fail Agent-source',
        'test "$(git -C "$AGENT_ROOT" rev-parse HEAD^{tree})" = "$EXPECTED_AGENT_TREE" || fail Agent-tree',
        'test "$(git -C "$AGENT_ROOT" show -s --format=%P HEAD)" = "$EXPECTED_AGENT_PARENTS" || fail Agent-parents',
        f'test "$(git -C "$AGENT_ROOT" rev-parse refs/heads/{NORMAL_REF})" = "$EXPECTED_AGENT" || fail Agent-ref',
        'test "$(git -C "$AGENT_ROOT" status --porcelain=v1 --untracked-files=all)" = "" || fail Agent-dirty',
        'test "$(git -C "$RUNTIME_ROOT" rev-parse HEAD)" = "$EXPECTED_RUNTIME" || fail Runtime-source',
        'test "$(git -C "$RUNTIME_ROOT" rev-parse HEAD^{tree})" = "$EXPECTED_RUNTIME_TREE" || fail Runtime-tree',
        'test "$(git -C "$RUNTIME_ROOT" show -s --format=%P HEAD)" = "$EXPECTED_RUNTIME_PARENTS" || fail Runtime-parents',
        f'test "$(git -C "$RUNTIME_ROOT" rev-parse refs/heads/{NORMAL_REF})" = "$EXPECTED_RUNTIME" || fail Runtime-ref',
        'test "$(git -C "$RUNTIME_ROOT" status --porcelain=v1 --untracked-files=all)" = "" || fail Runtime-dirty',
        f'test "$(sha256sum "$APP_ROOT/runtime.lock.json" | cut -d\' \' -f1)" = {q(facts["locks"]["app"]["file_sha256"])} || fail App-lock',
        f'test "$(sha256sum "$AGENT_ROOT/runtime.lock.json" | cut -d\' \' -f1)" = {q(facts["locks"]["agent"]["file_sha256"])} || fail Agent-lock',
        f'test "$(sha256sum "$APP_ROOT/{P1_BODY_RELATIVE}" | cut -d\' \' -f1)" = "$EXPECTED_BODY_SHA" || fail P1-body',
    ]
    for path, digest in facts["clients"]["files"].items():
        lines.append(f'test "$(sha256sum "$APP_ROOT/{path}" | cut -d\' \' -f1)" = {q(digest)} || fail Client-{path.replace("/", "-")}')
    lines.extend([
        'test "$(git -C "$AGENT_ROOT" rev-parse HEAD:remotion)" = "$EXPECTED_REMOTION_TREE" || fail Remotion-tree',
        'test "$(sha256sum "$AGENT_ROOT/remotion/package-lock.json" | cut -d\' \' -f1)" = "$EXPECTED_REMOTION_LOCK" || fail Remotion-lock',
        f'test "$(sha256sum "$AGENT_ROOT/remotion/package.json" | cut -d\' \' -f1)" = {q(facts["remotion"]["package_sha256"])} || fail Remotion-package',
        'test -x "$REMOTION_NODE" && test "$($REMOTION_NODE --version)" = "$EXPECTED_REMOTION_NODE" || fail Remotion-node',
        'test -x "$REMOTION_NPM" && test "$(PATH="$(dirname "$REMOTION_NODE"):/usr/bin:/bin" "$REMOTION_NPM" --version)" = "$EXPECTED_REMOTION_NPM" || fail Remotion-npm',
        f'test -f "$COMPOSITION_ARTIFACT" && test "$(sha256sum "$COMPOSITION_ARTIFACT" | cut -d\' \' -f1)" = {q(composition["artifact_sha256"])} || fail Composition-artifact',
        'test -d "$COMPOSITION_GRAPH" && test ! -L "$COMPOSITION_GRAPH" || fail Composition-graph',
        'test "$(env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -c ' + q(graph_code) + ' "$COMPOSITION_GRAPH")" = "$EXPECTED_COMPOSITION_FILES $EXPECTED_COMPOSITION_MAP" || fail Composition-map',
        f'test "$(sha256sum "$COMPOSITION_GRAPH/package.json" | cut -d\' \' -f1)" = {q(composition["package_sha256"])} || fail Composition-package',
        f'test "$(PATH="$(dirname "$REMOTION_NODE"):/usr/bin:/bin" "$REMOTION_NODE" -p "require(\\\"$COMPOSITION_GRAPH/package.json\\\").version")" = {q(composition["version"])} || fail Composition-version',
        f'test "$(readlink -f {q(str(AGENT_PYTHON))})" = {q(interpreter["agent"]["python"])} || fail Agent-interpreter',
        f'test "$(readlink -f {q(str(RUNTIME_PYTHON))})" = {q(interpreter["runtime"]["python"])} || fail Runtime-interpreter',
    ])
    for path, digest in facts["runtime_artifacts"].items():
        lines.append(f'test "$(sha256sum {q(path)} | cut -d\' \' -f1)" = {q(digest)} || fail Runtime-artifact-{Path(path).name}')
    for role, root, python, modules in (
        ("Agent", "$AGENT_ROOT", AGENT_PYTHON, interpreter["agent"]["imports"]),
        ("Runtime", "$RUNTIME_ROOT", RUNTIME_PYTHON, interpreter["runtime"]["imports"]),
    ):
        expected_probe = {key: value for key, value in interpreter[role.lower()].items() if key != "command"}
        lines.append(
            f'test "$(env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="{root}" '
            f'{q(str(python))} -c {q(full_probe_code)} {q(json.dumps(list(modules), separators=(",", ":")))})" = {q(json.dumps(expected_probe, sort_keys=True, separators=(",", ":")))} || fail {role}-imports-versions'
        )
        for module, origin in modules.items():
            lines.append(
                f'test "$(env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="{root}" '
                f'{q(str(python))} -c {q(probe_code)} {q(module)})" = {q(origin)} || fail {role}-import-{module.replace("_", "-")}'
            )
    stage_root = facts["stages"]["root"]
    lines.extend([
        f'P1_STAGE_ROOT="${{TIMELINE_P1_STAGE_ROOT:-{stage_root}}}"',
        'P1_RUN_ID="${TIMELINE_P1_RUN_ID:-p1-$(date +%s)-$$}"',
        'case "$P1_STAGE_ROOT" in /*) ;; *) fail stage-root-path ;; esac',
        'case "$P1_RUN_ID" in ""|*[!A-Za-z0-9._-]*) fail stage-run-id ;; esac',
        'test -d "$P1_STAGE_ROOT" || fail stage-root-missing',
        'test ! -L "$P1_STAGE_ROOT" || fail stage-root-symlink',
        'mkdir -p "$P1_STAGE_ROOT/$P1_RUN_ID"',
        'P1_RUN_ROOT="$P1_STAGE_ROOT/$P1_RUN_ID"',
        'test ! -L "$P1_RUN_ROOT" || fail stage-run-symlink',
        'for stage in source environment original; do mkdir -p "$P1_RUN_ROOT/$stage"; test -d "$P1_RUN_ROOT/$stage" || fail stage-$stage-destination; done',
        'test ! -e "$P1_RUN_ROOT/source/commit" || test "$(cat "$P1_RUN_ROOT/source/commit")" = "$EXPECTED_APP" || fail stale-source-stage',
        'printf "%s\\n" "$EXPECTED_APP" > "$P1_RUN_ROOT/source/commit"',
        'printf "%s\\n" "$EXPECTED_APP_TREE" > "$P1_RUN_ROOT/source/tree"',
        'printf "%s\\n" "$EXPECTED_APP_PARENTS" > "$P1_RUN_ROOT/source/parents"',
        'printf "%s\\n" "$EXPECTED_AGENT $EXPECTED_RUNTIME" > "$P1_RUN_ROOT/environment/integration-heads"',
        'printf "%s\\n" "$EXPECTED_BODY_SHA" > "$P1_RUN_ROOT/environment/body"',
        'PLAYWRIGHT_OUTPUT_DIR="$P1_RUN_ROOT/original/playwright-output"',
        'mkdir -p "$PLAYWRIGHT_OUTPUT_DIR"',
        'cd "$APP_ROOT"',
        'set +e',
        f'env -u NODE_PATH -u PYTHONHOME ASTRID_CHECKOUT="$AGENT_ROOT" ASTRID_PYTHON={q(str(AGENT_PYTHON))} ASTRID_RUNTIME_CHECKOUT="$RUNTIME_ROOT" ASTRID_RUNTIME_PYTHON={q(str(RUNTIME_PYTHON))} ASTRID_REMOTION_PROJECT_DIR={q(str(REMOTION_PROJECT))} ASTRID_NODE_EXECUTABLE="$REMOTION_NODE" ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages TIMELINE_BUNDLE_AGENT_HEAD="$EXPECTED_AGENT" TIMELINE_BUNDLE_RUNTIME_HEAD="$EXPECTED_RUNTIME" PYTHONPATH="$APP_ROOT:$RUNTIME_ROOT:$AGENT_ROOT" PATH="$REMOTION_NODE_DIR:$APP_ROOT/node_modules/.bin:/usr/bin:/bin" PLAYWRIGHT_OUTPUT_DIR="$PLAYWRIGHT_OUTPUT_DIR" {" ".join(q(item) for item in P1_TARGET)} >"$P1_RUN_ROOT/original/stdout.log" 2>"$P1_RUN_ROOT/original/stderr.log"',
        'P1_STATUS=$?',
        'set -e',
        'printf "%s\\n" "$P1_STATUS" > "$P1_RUN_ROOT/original/status"',
        'exit "$P1_STATUS"',
    ])
    script = "\n".join(lines) + "\n"
    for forbidden in FORBIDDEN_SHELL_TEXT:
        require(forbidden not in script, f"forbidden shell text: {forbidden}")
    return script


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-source", action="store_true", help="authenticate sources and emit the unrun shell")
    parser.add_argument(
        "--negative",
        choices=("wrong-source", "wrongsource", "tree", "parent", "parents", "lock", "locks", "clients", "import", "interpreters", "graph", "target", "body", "stage", "missing-stage", "stale-stage", "poison"),
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
