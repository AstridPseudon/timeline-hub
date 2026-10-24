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
import os
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


def file_map(root: Path) -> dict[str, str]:
    require(root.is_dir() and root.resolve() == root and not root.is_symlink(), f"physical directory required: {root}")
    files = {}
    for path in root.rglob("*"):
        require(not path.is_symlink(), f"aliased graph input: {path}")
        if path.is_file() and path.suffix != ".pyc" and "__pycache__" not in path.parts:
            files[path.relative_to(root).as_posix()] = sha256_file(path)
    return files


def canonical_sha(value: Any) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["/usr/bin/git", "-C", str(root), *args],
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
    elif name == "wrongschema":
        value["schema"]["files"]["banodoco_timeline_schema/timeline.schema.json"] = "0" * 64
    elif name == "bench":
        value["remotion"]["project"] = "/forged/remotion"
    elif name == "dist":
        value["dist"]["policy"] = "reuse-existing-build"
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
    require(expected["checkout"] == str(root) and expected["ref"] == NORMAL_REF, f"{label} source origin changed")
    require(git(root, "rev-parse", "--show-toplevel") == str(root), f"{label} checkout root changed")
    require(git(root, "symbolic-ref", "--short", "HEAD") == NORMAL_REF, f"{label} ref changed")
    require(git(root, "rev-parse", f"refs/heads/{NORMAL_REF}") == expected["source"], f"{label} normal ref moved")
    require(git(root, "rev-parse", "HEAD") == expected["source"], f"{label} source moved")
    require(git(root, "rev-parse", "HEAD^{tree}") == expected["tree"], f"{label} tree moved")
    require(git(root, "show", "-s", "--format=%P", "HEAD").split() == expected["parents"], f"{label} parents moved")
    require(not git(root, "status", "--porcelain=v1", "--untracked-files=all"), f"{label} checkout is dirty")


def assert_locks(facts: dict[str, Any]) -> None:
    for label, root in (("app", APP), ("agent", AGENT)):
        path = root / "runtime.lock.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        expected = facts["locks"][label]
        require(sha256_file(path) == expected["file_sha256"], f"{label} lock changed")
        require(canonical_sha(value["files"]) == expected["files_sha256"], f"{label} lock mappings changed")
        require(value["source_commit"] == facts["integrations"]["runtime"]["source"], f"{label} lock producer changed")
        require(value["producer_version"] == expected["producer_version"], f"{label} producer version changed")
        require(len(value["files"]) == expected["file_count"], f"{label} lock mapping count changed")
        for relative, item in value["files"].items():
            digest = item["sha256"].removeprefix("sha256:")
            require(sha256_file(root / relative) == digest, f"{label} consumed lock file changed: {relative}")
            require(sha256_file(RUNTIME / item["from"]) == digest, f"{label} producer lock file changed: {relative}")


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
    require(remotion["project"] == str(REMOTION_PROJECT), "consumed Remotion bench changed")
    require(REMOTION_PROJECT.resolve() == REMOTION_PROJECT and not REMOTION_PROJECT.is_symlink(), "Remotion bench is aliased")
    for relative in git(AGENT, "ls-tree", "-r", "--name-only", "HEAD:remotion").splitlines():
        require(sha256_file(REMOTION_PROJECT / relative) == sha256_file(AGENT / "remotion" / relative), f"consumed Remotion source changed: {relative}")
    for relative, digest in remotion["bench_files"].items():
        require(sha256_file(REMOTION_PROJECT / relative) == digest, f"consumed Remotion input changed: {relative}")
    for path_text, digest in facts["runtime_artifacts"].items():
        require(sha256_file(Path(path_text)) == digest, f"Runtime artifact changed: {path_text}")
    composition = facts["composition"]
    require(sha256_file(Path(composition["artifact"])) == composition["artifact_sha256"], "Composition artifact changed")
    graph = Path(composition["graph"])
    require(graph == REMOTION_PROJECT / "node_modules/@banodoco/timeline-composition", "Composition graph is not the consumed bench graph")
    require(graph.is_dir() and not graph.is_symlink() and graph.resolve() == graph, "approved Composition graph unavailable")
    files = file_map(graph)
    require(len(files) == composition["file_count"], "Composition graph file count changed")
    require(canonical_sha(files) == composition["file_map_sha256"], "Composition graph bytes changed")
    package = graph / "package.json"
    require(sha256_file(package) == composition["package_sha256"], "Composition package changed")
    require(json.loads(package.read_text(encoding="utf-8"))["version"] == composition["version"], "Composition version changed")
    app_graph = APP / "node_modules/@banodoco/timeline-composition"
    require(file_map(app_graph) == files, "consumed App Composition graph differs from authenticated artifact; existing node_modules is stale")


def assert_schema(facts: dict[str, Any]) -> None:
    schema = facts["schema"]
    root = Path(schema["pythonpath"])
    require(root == Path("/home/user/work/venv-agent/lib/python3.13/site-packages"), "consumed schema root changed")
    require(set(schema["files"]) == {
        f"banodoco_timeline_schema/{name}" for name in (
            "__init__.py", "generated.py", "materialize.py", "theme.py", "timeline.schema.json", "validate.py",
        )
    }, "consumed schema file closure changed")
    require(schema["files"]["banodoco_timeline_schema/timeline.schema.json"] == facts["clients"]["files"]["vendor/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json"], "consumed schema contract changed")
    # AstridCli.env() drops the outer schema setting. Both consumers must agree;
    # selecting a vendored root only in the parent cannot repair that child.
    actual = probe(AGENT_PYTHON, f"{AGENT}:{RUNTIME}", ["banodoco_timeline_schema"])
    require(actual["imports"]["banodoco_timeline_schema"] == schema["origin"], "consumed Agent child schema origin changed")
    for relative, digest in schema["files"].items():
        require(sha256_file(APP / "vendor/timeline-schema/python" / relative) == digest, f"authoritative schema input changed: {relative}")
        require(sha256_file(root / relative) == digest, f"consumed schema differs from authenticated vendored schema: {relative}")


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
    require(target["command"] == list(P1_TARGET), "execution target changed")
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


def validate(facts: dict[str, Any]) -> None:
    require(not facts.get("poison_marker"), "poison marker refused")
    require(facts["target"]["command"] == list(P1_TARGET), "execution target changed")
    assert_source_snapshot(facts)
    assert_integration("Agent", AGENT, facts)
    assert_integration("Runtime", RUNTIME, facts)
    assert_locks(facts)
    assert_clients(facts)
    assert_interpreters(facts)
    assert_schema(facts)
    assert_artifacts(facts)
    assert_spec(facts)
    assert_target(facts)
    assert_wire(facts)
    require(facts["chronology"]["future_snapshot_required"] is False, "future snapshot requirement is not allowed")
    require(facts["chronology"]["historical_caller_reused"] is False, "historical caller reuse is refused")
    require(facts["execution"]["submitted"] is False, "submission is outside this preparation")
    require(facts["stages"]["root"] == "/tmp/timeline-p1-current-caller", "stage root changed")
    require(facts["stages"]["source"]["files"] == ["commit", "tree", "parents"], "source stage destinations are incomplete")
    require(facts["stages"]["environment"]["files"] == ["integration-heads", "body"], "environment stage destinations are incomplete")
    require(facts["stages"]["original"]["files"] == ["stdout.log", "stderr.log", "status", "playwright-output"], "original stage destinations are incomplete")
    require(facts["dist"] == {"policy": "fresh-build-only", "relative": "environment/dist", "status": "NOT_BUILT"}, "dist must be built fresh from selected App source")


def consumed_environment(facts: dict[str, Any]) -> dict[str, str]:
    # Existing sharedlaunch52966 source-mode interfaces; no installed-child claim.
    return {
        "PATH": f"{REMOTION_NODE.parent}:{APP}/node_modules/.bin:/usr/bin:/bin",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": f"{APP}:{RUNTIME}:{AGENT}",
        "ASTRID_CHECKOUT": str(AGENT),
        "ASTRID_PYTHON": str(AGENT_PYTHON),
        "ASTRID_AGENT_PYTHON": str(AGENT_PYTHON),
        "ASTRID_RUNTIME_CHECKOUT": str(RUNTIME),
        "ASTRID_RUNTIME_PYTHON": str(RUNTIME_PYTHON),
        "ASTRID_REMOTION_PROJECT_DIR": str(REMOTION_PROJECT),
        "ASTRID_NODE_EXECUTABLE": str(REMOTION_NODE),
        "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": facts["schema"]["pythonpath"],
        "TIMELINE_BUNDLE_AGENT_HEAD": facts["integrations"]["agent"]["source"],
        "TIMELINE_BUNDLE_RUNTIME_HEAD": facts["integrations"]["runtime"]["source"],
    }


def assert_consumed_environment(facts: dict[str, Any], dist: str | None = None) -> None:
    for key, expected in consumed_environment(facts).items():
        require(os.environ.get(key) == expected, f"consumed environment changed: {key}")
    for key in ("NODE_PATH", "NODE_OPTIONS", "PYTHONHOME", "PYTHONSTARTUP", "LD_PRELOAD", "LD_LIBRARY_PATH"):
        require(key not in os.environ, f"poison environment: {key}")
    require(os.environ.get("ASTRID_APP_DIRECT_DIST") == dist, "consumed dist selection changed")


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
    # Embed the same readonly checks used by preparation, as sharedlaunch52966
    # does. The emitted caller never depends on this worker file surviving.
    checks = Path(__file__).read_text(encoding="utf-8").split("\ndef shell(", 1)[0]
    boundary_code = (
        "import json,sys\nn={'__name__':'p1_boundary','__file__':'/p1-current-caller.py'}\n"
        f"exec({checks!r},n)\nf=json.loads(sys.argv[1])\n"
        "try:\n"
        " n['assert_consumed_environment'](f, sys.argv[2] if len(sys.argv)>2 else None)\n"
        " n['validate'](f)\n"
        "except (RuntimeError, OSError, ValueError) as e:\n"
        " print('P1 source/environment refused: '+str(e),file=sys.stderr)\n"
        " sys.exit(2)\n"
    )
    boundary = f'"${{P1_ENV[@]}}" /usr/bin/python3 -c {q(boundary_code)} {q(json.dumps(facts, separators=(",", ":")))}'
    build_code = (
        "import {build} from 'vite'; "
        "import {resolveHostedRuntimeOrigin} from './scripts/hosted-build-origin.mjs'; "
        "process.env.VITE_RUNTIME_ORIGIN=resolveHostedRuntimeOrigin(); "
        "for (const k of ['ACTOR','REALM','INSTANCE']) process.env['VITE_WORKSPACE_RUNTIME_EXPECTED_'+k+'_ID']=''; "
        "await build({configFile:'config/vite/vite.config.ts',cacheDir:process.argv[2],"
        "build:{outDir:process.argv[1],emptyOutDir:false}});"
    )
    graph_code = (
        "import hashlib,json,sys; from pathlib import Path; "
        "p=Path(sys.argv[1]); paths=list(p.rglob('*')); "
        "bad=[x for x in paths if x.is_symlink()]; "
        "bad and sys.exit('aliased graph input'); "
        "f={str(x.relative_to(p)):hashlib.sha256(x.read_bytes()).hexdigest() "
        "for x in paths if x.is_file()}; "
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
        "export PATH=/usr/bin:/bin",
        "# PREPARED only: current consumed schema/App graph may refuse admission.",
        "# No old dist is accepted; the original journey follows a fresh build.",
        'for key in NODE_PATH NODE_OPTIONS PYTHONHOME PYTHONPATH PYTHONSTARTUP LD_PRELOAD LD_LIBRARY_PATH BASH_ENV ENV; do test -z "${!key+x}" || { echo "P1 poison environment: $key" >&2; exit 2; }; done',
        "P1_ENV=(env -i " + " ".join(q(f"{key}={value}") for key, value in consumed_environment(facts).items()) + ")",
        boundary,
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
        'test "$(readlink -f "$P1_STAGE_ROOT")" = "$P1_STAGE_ROOT" || fail stage-root-alias',
        'mkdir "$P1_STAGE_ROOT/$P1_RUN_ID" || fail stale-run-stage',
        'P1_RUN_ROOT="$P1_STAGE_ROOT/$P1_RUN_ID"',
        'test ! -L "$P1_RUN_ROOT" || fail stage-run-symlink',
        'for stage in source environment original; do mkdir "$P1_RUN_ROOT/$stage"; test -d "$P1_RUN_ROOT/$stage" && test ! -L "$P1_RUN_ROOT/$stage" || fail stage-$stage-destination; done',
        'test ! -e "$P1_RUN_ROOT/source/commit" || test "$(cat "$P1_RUN_ROOT/source/commit")" = "$EXPECTED_APP" || fail stale-source-stage',
        'printf "%s\\n" "$EXPECTED_APP" > "$P1_RUN_ROOT/source/commit"',
        'printf "%s\\n" "$EXPECTED_APP_TREE" > "$P1_RUN_ROOT/source/tree"',
        'printf "%s\\n" "$EXPECTED_APP_PARENTS" > "$P1_RUN_ROOT/source/parents"',
        'printf "%s\\n" "$EXPECTED_AGENT $EXPECTED_RUNTIME" > "$P1_RUN_ROOT/environment/integration-heads"',
        'printf "%s\\n" "$EXPECTED_BODY_SHA" > "$P1_RUN_ROOT/environment/body"',
        'PLAYWRIGHT_OUTPUT_DIR="$P1_RUN_ROOT/original/playwright-output"',
        'mkdir -p "$PLAYWRIGHT_OUTPUT_DIR"',
        'P1_DIST="$P1_RUN_ROOT/environment/dist"',
        'test ! -e "$P1_DIST" && test ! -L "$P1_DIST" || fail stale-dist',
        'mkdir "$P1_RUN_ROOT/environment/home" "$P1_RUN_ROOT/environment/tmp"',
        'P1_ENV+=("HOME=$P1_RUN_ROOT/environment/home" "TMPDIR=$P1_RUN_ROOT/environment/tmp" "ASTRID_APP_DIRECT_DIST=$P1_DIST" "PLAYWRIGHT_OUTPUT_DIR=$PLAYWRIGHT_OUTPUT_DIR")',
        'cd "$APP_ROOT"',
        f'test "$(pwd -P)" = {q(str(APP))} || fail execution-cwd',
        ': TIMELINE_P1_SOURCE_ENVIRONMENT_ADMITTED',
        '# NOT RUN during preparation: build into an absent private destination.',
        f'"${{P1_ENV[@]}}" "$REMOTION_NODE" --input-type=module -e {q(build_code)} "$P1_DIST" "$P1_RUN_ROOT/environment/vite-cache" >"$P1_RUN_ROOT/environment/build.stdout.log" 2>"$P1_RUN_ROOT/environment/build.stderr.log" || fail fresh-dist-build',
        boundary + ' "$P1_DIST"',
        'test -f "$P1_DIST/index.html" && test ! -L "$P1_DIST/index.html" || fail missing-built-dist',
        'test "$(readlink -f "$P1_DIST")" = "$P1_DIST" || fail built-dist-alias',
        'env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -c ' + q(graph_code) + ' "$P1_DIST" > "$P1_RUN_ROOT/environment/dist.sha256"',
        'test "$(env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -c ' + q(graph_code) + ' "$P1_DIST")" = "$(cat "$P1_RUN_ROOT/environment/dist.sha256")" || fail changed-built-dist',
        'set +e',
        f'"${{P1_ENV[@]}}" {" ".join(q(item) for item in P1_TARGET)} >"$P1_RUN_ROOT/original/stdout.log" 2>"$P1_RUN_ROOT/original/stderr.log"',
        'P1_STATUS=$?',
        'set -e',
        'printf "%s\\n" "$P1_STATUS" > "$P1_RUN_ROOT/original/status"',
        'exit "$P1_STATUS"',
    ])
    script = "\n".join(lines) + "\n"
    return script


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-source", action="store_true", help="authenticate sources and emit the unrun shell")
    parser.add_argument(
        "--negative",
        choices=("wrong-source", "wrongsource", "tree", "parent", "parents", "lock", "locks", "clients", "import", "interpreters", "graph", "wrongschema", "bench", "dist", "target", "body", "stage", "missing-stage", "stale-stage", "poison"),
        help="exercise one refusal control",
    )
    args = parser.parse_args()
    if not args.dry_source and args.negative is None:
        parser.error("use --dry-source; the caller is not submitted by this artifact")
    facts = load_facts()
    candidate = expected_for_negative(facts, args.negative)
    try:
        # A refusal on a broken baseline is not evidence for a negative control.
        if args.negative is not None:
            validate(facts)
    except PreparedError as exc:
        print(f"CONTROL_BASELINE_REFUSED: {exc}", file=sys.stderr)
        return 2
    try:
        validate(candidate)
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
