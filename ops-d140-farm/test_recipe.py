from __future__ import annotations

import json
import ast
import hashlib
import os
import re
import subprocess
import types
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parent
COMMANDS = (ROOT / "commands.md").read_text()
RECEIVER = (ROOT / "receive-farm.sh").read_text()


def run_receiver(tmp_path: Path, phase: str, receiver: Path | None = None, **bindings: str) -> dict:
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("FARM_") or name.endswith("_SHA256") or name == "KIT_SOURCE_CHECKOUT":
            env.pop(name)
    for name in (
        "AGENT_CHECKOUT", "RUNTIME_CHECKOUT", "APP_CHECKOUT", "COMPOSITION_CHECKOUT",
        "MAKER_PATH", "WRAPPER_PATH", "CHECKER_PATH", "RECEIVED_MAKER",
        "SCHEMA_INSTALLED_DISTRIBUTION", "SCHEMA_SOURCE_MANIFEST", "SCHEMA_RECORD_CLOSURE",
        "SCHEMA_DIRECT_URL", "CANONICAL_CENSUS", "DEPENDENCY_SEED", "CENTRAL_SERVICE",
        "CENTRAL_SUITE", "D73_LAUNCHER", "NODE_BIN", "NORMAL_REQUEST_ROUTE",
        "IMPORT_CHECK_ROUTE", "D73_DRY_ROUTE", "CORE_ROUTE", "PROFILE", "DISK_ADMISSION",
        "RETAINED_ROOT", "P4_PYTHON", "CHILD_PYTHON", "CHILD_BOOTSTRAP", "CHILD_RECEIPT",
        "P4_D73_MANIFEST", "P4_D73_EVIDENCE", "P4_D73_REQUEST_ID", "OUTPUT_ROOT", "JUNIT_ROOT",
        "RAW_ROOT", "STARTSTOP_ROOT", "KEEP_ROOT", "POSITIVE_CONTROL", "POSITIVE_COUNTER",
        "POISON_CONTROL", "POISON_COUNTER", "POISON_MANIFEST", "FARM_CURRENT_AGENT_RECEIPT",
        "FARM_CURRENT_RUNTIME_RECEIPT", "FARM_CURRENT_APP_RECEIPT",
        "FARM_CURRENT_COMPOSITION_RECEIPT", "FARM_D139A_KIT_RECEIPT", "FARM_D73_RECEIPT",
    ):
        env.pop(name, None)
    env["D140_PHASE"] = phase
    env.update(bindings)
    result = subprocess.run(
        [str(receiver or ROOT / "receive-farm.sh"), "--check-only"],
        cwd=ROOT.parent,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    return json.loads(result.stdout)


def test_receiver_is_check_only_and_contains_current_tuple() -> None:
    assert '"$1" != "--check-only"' in RECEIVER
    for value in (
        "41ad656529fa8489829de9078b1b6e157c7433c8",
        "f103bb46866999c961a8865636f2e66d544e0c9b",
        "5696769dfca056676cde1ab46d8bc94354b3a44a",
        "635f4de06fda22a85fc2e4cfc764d0153a4c9f40",
    ):
        assert value in RECEIVER


def test_core_selector_has_exactly_22_unfiltered_roots() -> None:
    expected = [
        "tests/editing_conformance",
        "tests/sdk",
        "tests/timeline",
        "tests/core/timeline",
        "tests/core/test_timeline_element_orphan_cleanup.py",
        "tests/core/test_timeline_element_publication.py",
        "tests/core/test_timeline_element_publication_runtime.py",
        "tests/core/rendering/test_timeline_visualize_cli_grammar.py",
        "tests/core/rendering/test_local_schema.py",
        "tests/packs/timeline",
        "tests/packs/rendering/test_composition_package.py",
        "tests/packs/rendering/test_live_scene_composition.py",
        "tests/packs/rendering/test_render_export_task_adapter.py",
        "tests/packs/rendering/test_timeline_filmstrip_cards.py",
        "tests/packs/rendering/test_timeline_filmstrip_execution.py",
        "tests/packs/video_editing/test_runtime_publication_chain.py",
        "tests/stage1/test_cold_launch_autobootstrap.py",
        "tests/test_installer_schema.py",
        "tests/test_installer_sources.py",
        "tests/test_installer_bootstrap_schema.py",
        "tests/test_timeline_clip_replacement.py",
        "tests/v10/test_timelines_create.py",
    ]
    body = COMMANDS.split("agent-core-full", 1)[1]
    assert "-k " not in body
    assert "--collect-only" not in body
    assert body.count("tests/") >= len(expected)
    for root in expected:
        assert root in body
    assert len(expected) == 22


def test_schema_and_control_gates_are_literal() -> None:
    for token in (
        "--schema-installed-distribution",
        "--schema-source-manifest",
        "--census-file",
        "positive_rc",
        "poison_rc",
        "= 17",
        'POSITIVE_COUNTER\")" = 1',
        'POISON_COUNTER\")" = 0',
    ):
        assert token in COMMANDS
    assert "--farm-schema-source" in (ROOT / "README.md").read_text()


def test_no_alternate_launcher_or_profile_is_advertised() -> None:
    assert re.search(r"existing reviewed D73 launcher", (ROOT / "README.md").read_text())
    assert "fallback profile" in (ROOT / "README.md").read_text()
    assert "p4-d73-pinned-launch.sh" in COMMANDS


def test_phase_census_does_not_admit_future_inputs_or_start_routes(tmp_path: Path) -> None:
    marker = tmp_path / "route-called"
    route = tmp_path / "route"
    route.write_text(f"#!/bin/sh\ntouch {marker}\n", encoding="utf-8")
    route.chmod(0o755)
    pre = run_receiver(tmp_path, "pre-child", NORMAL_REQUEST_ROUTE=str(route))
    post = run_receiver(tmp_path, "post-child", NORMAL_REQUEST_ROUTE=str(route))
    pre_ids = {check["id"] for check in pre["checks"]}
    post_ids = {check["id"] for check in post["checks"]}
    assert pre["phase"] == "pre-child"
    assert post["phase"] == "post-child"
    assert "binding.CHILD_RECEIPT" not in pre_ids
    assert "binding.P4_D73_MANIFEST" not in pre_ids
    assert "binding.OUTPUT_ROOT" not in pre_ids
    assert "binding.FARM_DISTRIBUTION_SOURCE" not in pre_ids
    assert "distribution.original-bootstrap" not in pre_ids
    assert "route.normal-caller" in pre_ids
    assert "receipt.FARM_D73_RECEIPT" not in pre_ids | post_ids
    assert "binding.CHILD_RECEIPT" in post_ids
    assert "binding.P4_D73_MANIFEST" in post_ids
    assert "binding.OUTPUT_ROOT" in post_ids
    assert not marker.exists()


def test_wrong_receipt_and_poison_content_are_not_presence_passes(tmp_path: Path) -> None:
    wrong_receipt = tmp_path / "wrong-receipt.json"
    wrong_receipt.write_text('{"status":"passed","commit":"wrong"}\n', encoding="utf-8")
    result = run_receiver(tmp_path, "pre-child", FARM_CURRENT_AGENT_RECEIPT=str(wrong_receipt),
                          FARM_CURRENT_AGENT_RECEIPT_SHA256=sha(wrong_receipt.read_bytes()), FARM_ORCH_ROOT=str(tmp_path))
    receipt_check = next(check for check in result["checks"] if check["id"] == "receipt.FARM_CURRENT_AGENT_RECEIPT")
    assert receipt_check["status"] == "MISMATCH"

    positive = tmp_path / "positive.manifest"
    poison = tmp_path / "poison.manifest"
    positive.write_text("format=p4-d73-v1\nagent_sha=" + "1" * 40 + "\nagent_tree=tree\n", encoding="utf-8")
    poison.write_text("format=p4-d73-v1\nagent_sha=" + "0" * 40 + "\nagent_tree=wrong\n", encoding="utf-8")
    result = run_receiver(
        tmp_path,
        "post-child",
        P4_D73_MANIFEST=str(positive),
        POISON_MANIFEST=str(poison),
    )
    poison_check = next(check for check in result["checks"] if check["id"] == "control.poison-content")
    assert poison_check["status"] == "MISMATCH"


def test_schema_paths_are_bound_to_the_physical_dist_info(tmp_path: Path) -> None:
    dist = tmp_path / "banodoco_timeline_schema-0.0.2.dist-info"
    dist.mkdir()
    record = tmp_path / "detached-RECORD"
    direct = tmp_path / "detached-direct_url.json"
    manifest = tmp_path / "manifest.json"
    for path in (record, direct, manifest):
        path.write_text("{}\n", encoding="utf-8")
    result = run_receiver(
        tmp_path,
        "pre-child",
        SCHEMA_INSTALLED_DISTRIBUTION=str(dist),
        SCHEMA_RECORD_CLOSURE=str(record),
        SCHEMA_DIRECT_URL=str(direct),
        SCHEMA_SOURCE_MANIFEST=str(manifest),
    )
    path_check = next(check for check in result["checks"] if check["id"] == "schema.bound-paths")
    assert path_check["status"] == "MISMATCH"


def test_import_failure_stops_before_controls_and_core() -> None:
    failure = COMMANDS.index('if [ "$imports_rc" -ne 0 ]')
    controls = COMMANDS.index("## 3. D73 dry controls")
    assert failure < controls
    assert 'exit "$imports_rc"' in COMMANDS[:controls]
    assert 'P4_D73_MANIFEST="$P4_D73_MANIFEST"' in COMMANDS
    assert 'P4_D73_EVIDENCE="$KEEP_ROOT"' in COMMANDS
    assert 'CORE_ROUTE="$CORE_ROUTE"' in COMMANDS
    assert '--junitxml="$2"' in COMMANDS
    assert 'test -s "$raw_log"' in COMMANDS
    assert 'test -s "$DISK_ADMISSION"' in COMMANDS


def test_poison_and_d124_controls_are_not_weakened() -> None:
    assert 'only agent_sha replaced by forty zeroes' in RECEIVER
    assert 'check_source_receipt' in RECEIVER
    assert 'check_d73_receipt' in RECEIVER
    assert 'GIT, "--no-replace-objects", "-C", str(repo)' in (ROOT / "receipts.py").read_text()
    assert COMMANDS.count("tests/") >= 22
    assert "-k " not in COMMANDS
    assert "--collect-only" not in COMMANDS


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def receipt_status(result: dict, name: str) -> str:
    return next(row["status"] for row in result["checks"] if row["id"] == "receipt." + name)


@pytest.fixture
def custody(tmp_path: Path) -> dict:
    """Small producer artifacts only; no venv, Store, request, or body executes."""
    constants = dict(re.findall(r"^readonly ([A-Z_]+)=([^\n]+)$", RECEIVER, re.M))
    orch = tmp_path / "orch"
    (orch / "queue/done").mkdir(parents=True)
    (orch / "bin").mkdir()
    bindings = {"FARM_ORCH_ROOT": str(orch)}
    live = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin")
    # These are tiny reviewed operational sources, never shared dependencies.
    for name in ("make-checkout", "dispatcher-daemon", "bench_store.py", "verify_dependency_seed.py", "verify_farm_distribution_inputs.py"):
        path = orch / "bin" / name
        path.write_bytes((live / name).read_bytes())
        path.chmod(0o755)
    for name in ("make-child-venv", "request-child-venv", "check-child-imports"):
        path = orch / "bin" / name
        path.write_bytes((ROOT.parent / "ops-child-custody" / name).read_bytes())
        path.chmod(0o755)
    bindings.update({name: str(orch / "bin" / tool) for tool, names in (
        ("make-child-venv", ("MAKER_PATH", "RECEIVED_MAKER")),
        ("request-child-venv", ("WRAPPER_PATH", "NORMAL_REQUEST_ROUTE")),
        ("check-child-imports", ("CHECKER_PATH", "IMPORT_CHECK_ROUTE")),
    ) for name in names})
    for kind in ("agent", "runtime", "app", "composition"):
        commit = constants[kind.upper() + "_SHA"]
        prefix = {"agent": "agt", "runtime": "rt", "app": "app", "composition": "vw"}[kind]
        worker = prefix + "-pin-" + commit[:8]
        repo = tmp_path / "work/wt" / worker
        repo.mkdir(parents=True)
        bindings[kind.upper() + "_CHECKOUT"] = str(repo)
        name = "FARM_CURRENT_" + kind.upper() + "_RECEIPT"
        path = orch / "queue/done" / f"checkout-{kind}-{commit}"
        path.write_text(f"created {repo} (detached at {commit}, KEEP)\n")
        bindings[name] = str(path)
        bindings[name + "_SHA256"] = sha(path.read_bytes())
        prefix = {"agent": "agt", "runtime": "rt", "app": "app", "composition": "vw"}[kind]
        worker = prefix + "-pin-" + commit[:8]
        record = orch / "workers" / worker
        record.mkdir(parents=True)
        (record / "KEEP").touch()
        (record / "meta").write_text(
            f"name={worker}\nrepo={kind}\nbase={commit[:8]}\nbase_sha={commit[:8]}\n"
            f"model=none\neffort=none\nheavy=0\nworktree={repo}\nstarted=2026-10-25T00:00:00Z\n"
        )
    launcher = Path(bindings["AGENT_CHECKOUT"]) / "tools/p4-d73-pinned-launch.sh"
    launcher.parent.mkdir()
    launcher.write_bytes(subprocess.check_output([
        "git", "-C", "/home/user/work/agent", "show",
        constants["AGENT_SHA"] + ":tools/p4-d73-pinned-launch.sh",
    ]))
    launcher.chmod(0o755)
    bindings["D73_LAUNCHER"] = str(launcher)
    kit_source = tmp_path / "kit-source"
    kit_source.mkdir()
    bindings["KIT_SOURCE_CHECKOUT"] = str(kit_source)
    bindings["RECEIVED_MAKER"] = str(orch / "bin/make-child-venv")
    client = b"CLIENT = 1\n"
    client_rel = "packages/python/astrid_runtime_client/__init__.py"
    fake_git = tmp_path / "git"
    states = {bindings[k.upper() + "_CHECKOUT"]: [constants[k.upper() + "_SHA"], constants[k.upper() + "_TREE"]]
              for k in ("agent", "runtime", "app", "composition")}
    states[str(kit_source)] = ["a" * 40, "b" * 40]
    # The git shim deliberately supplies perfect supporting checkout evidence,
    # including in the final2332 attack. It never authenticates a receipt.
    fake_git.write_text(
        "#!/usr/bin/python3\nimport sys\nfrom pathlib import Path\n"
        f"states={states!r}\nroot={str(ROOT.parent)!r}\n"
        "i=sys.argv.index('-C'); repo=sys.argv[i+1]; args=sys.argv[i+2:]\ncommit,tree=states[repo]\n"
        "if args[0]=='rev-parse': print(tree if 'tree' in args[-1] else commit)\n"
        "elif args[0]=='status': pass\n"
        "elif args[0]=='rev-list': print(commit)\n"
        f"elif args[0]=='ls-tree': print({client_rel!r})\n"
        "elif args[0]=='show':\n"
        " rel=args[1].split(':',1)[1]\n"
        f" sys.stdout.buffer.write({client!r} if rel=={client_rel!r} else (Path(root)/rel).read_bytes())\n"
        "elif args[0]=='cat-file': pass\nelse: sys.exit(1)\n"
    )
    fake_git.chmod(0o755)
    bindings["PATH"] = str(tmp_path) + os.pathsep + os.environ["PATH"]
    # Private OS boundary only: production has no env override for these roots
    # or Git. All admission functions and the shell caller run unchanged.
    overlay = tmp_path / "receiver"
    overlay.mkdir()
    receiver = overlay / "receive-farm.sh"
    receiver.write_text(RECEIVER)
    receiver.chmod(0o755)
    checker = (ROOT / "receipts.py").read_text()
    checker = re.sub(r'^NORMAL_ORCH_ROOT = Path\(.*\)$', f'NORMAL_ORCH_ROOT = Path({str(orch)!r})', checker, flags=re.M)
    checker = checker.replace('NORMAL_WORK_ROOT = Path("/home/user/work")', f'NORMAL_WORK_ROOT = Path({str(tmp_path / "work")!r})')
    checker = checker.replace('GIT = "/usr/bin/git"', f'GIT = {str(fake_git)!r}')
    (overlay / "receipts.py").write_text(checker)
    bindings["receiver"] = receiver
    return {"bindings": bindings, "constants": constants, "orch": orch,
            "client_identity": f"{client_rel}={sha(client)}", "tmp": tmp_path}


def bind_artifact(custody: dict, name: str, path: Path, data: bytes) -> None:
    path.write_bytes(data)
    custody["bindings"].update({name: str(path), name + "_SHA256": sha(data)})


@pytest.mark.parametrize("kind", ["agent", "runtime", "app", "composition"])
@pytest.mark.parametrize("fault", [None, "producer", "digest", "tree", "format", "path", "meta", "missing-digest"])
def test_checkout_receipts_use_normal_producer_custody(custody: dict, kind: str, fault: str | None) -> None:
    bindings = custody["bindings"].copy()
    name = "FARM_CURRENT_" + kind.upper() + "_RECEIPT"
    path = Path(bindings[name])
    if fault == "producer":
        (custody["orch"] / "bin/make-checkout").write_text("#!/bin/sh\nexit 0\n")
    elif fault == "digest":
        bindings[name + "_SHA256"] = "0" * 64
    elif fault == "missing-digest":
        bindings.pop(name + "_SHA256")
    elif fault == "tree":
        script = custody["tmp"] / "git"
        script.write_text(script.read_text().replace(custody["constants"][kind.upper() + "_TREE"], "0" * 40))
    elif fault == "format":
        path.write_text(json.dumps({"schema": "timeline.synthetic-forged/v1", "status": "passed"}))
        bindings[name + "_SHA256"] = sha(path.read_bytes())
    elif fault == "path":
        detached = custody["tmp"] / "detached"
        detached.write_bytes(path.read_bytes())
        bindings[name] = str(detached)
    elif fault == "meta":
        prefix = {"agent": "agt", "runtime": "rt", "app": "app", "composition": "vw"}[kind]
        meta = custody["orch"] / "workers" / (prefix + "-pin-" + custody["constants"][kind.upper() + "_SHA"][:8]) / "meta"
        meta.write_text(meta.read_text().replace("repo=" + kind, "repo=untrusted"))
    result = run_receiver(custody["tmp"], "pre-child", **bindings)
    assert result["status"] == "NOT_READY"
    assert receipt_status(result, name) == ("PASS" if fault is None else "MISSING" if fault == "missing-digest" else "MISMATCH")


def test_final2332_synthetic_attack_cannot_use_perfect_checkout_as_authority(custody: dict) -> None:
    bindings, constants = custody["bindings"], custody["constants"]
    name = "FARM_CURRENT_AGENT_RECEIPT"
    forged = {"schema": "timeline.synthetic-forged/v1", "status": "passed", "producer": "untrusted",
              "commit": constants["AGENT_SHA"], "tree": constants["AGENT_TREE"], "repo": bindings["AGENT_CHECKOUT"]}
    bind_artifact(custody, name, Path(bindings[name]), json.dumps(forged).encode())
    result = run_receiver(custody["tmp"], "pre-child", **bindings)
    assert next(row for row in result["checks"] if row["id"] == "source.agent.checkout")["status"] == "PASS"
    assert receipt_status(result, name) == "MISMATCH"


def kit_artifacts(custody: dict) -> None:
    orch, bindings = custody["orch"], custody["bindings"]
    installer = {"path": str(orch / "bin/make-child-venv"), "sha256": custody["constants"]["MAKER_SHA"],
                 "bytes": 111171, "mode": "0755", "regular_nonsymlink": True}
    helpers = {name: sha((orch / "bin" / name).read_bytes()) for name in ("bench_store.py", "verify_dependency_seed.py")}
    installation = {"result": "PASS_INSTALL", "installer": "ops-child-custody/install-prep/apply-reviewed-maker.sh",
                    "installer_review": "installer1826", "source_commit": "a" * 40, "source_tree": "b" * 40,
                    "candidate": {key: installer[key] for key in ("sha256", "bytes", "mode")},
                    "target": {"path": installer["path"], "sha256": installer["sha256"], "bytes": 111171,
                               "mode": "0755", "regular_single_link": True, "matches_candidate": True},
                    "protected_helpers": helpers}
    path = custody["tmp"] / "installation.json"
    bind_artifact(custody, "FARM_KIT_INSTALLATION", path, json.dumps(installation).encode())
    value = {"schema": "timeline.ops.d137.installed-kit/v1", "status": "qualified_for_one_request", "installer": installer,
             "source": {"commit": "a" * 40, "tree": "b" * 40, "review": "PASS_SOURCE_SECURITY", "reviewed_installer": "installer1826"},
             "protected_helpers": helpers, "receipts": {"installation": str(path)}}
    bind_artifact(custody, "FARM_INSTALLED_KIT_SUMMARY", custody["tmp"] / "kit.json", json.dumps(value).encode())
    assert bindings["KIT_SOURCE_CHECKOUT"]


@pytest.mark.parametrize("fault", [None, "producer", "schema", "digest", "tree", "source", "installation", "child-fallback"])
def test_installed_kit_authenticates_composition_source_and_installation(custody: dict, fault: str | None) -> None:
    kit_artifacts(custody)
    bindings = custody["bindings"]
    name = "FARM_INSTALLED_KIT_SUMMARY"
    path = Path(bindings[name])
    value = json.loads(path.read_bytes())
    if fault == "producer":
        (custody["orch"] / "bin/make-child-venv").write_text("#!/bin/sh\nexit 0\n")
    elif fault == "schema":
        value["schema"] = "timeline.ops.synthetic-installed-kit/v1"
    elif fault == "digest":
        bindings[name + "_SHA256"] = "0" * 64
    elif fault == "tree":
        value["source"]["tree"] = "0" * 40
    elif fault == "source":
        value["source"]["commit"] = custody["constants"]["AGENT_SHA"]
    elif fault == "installation":
        Path(bindings["FARM_KIT_INSTALLATION"]).write_text("{}")
    elif fault == "child-fallback":
        bind_artifact(custody, name, path, b"status=verified\nreuse=verified\n")
    if fault in {"schema", "tree", "source"}:
        bind_artifact(custody, name, path, json.dumps(value).encode())
    result = run_receiver(custody["tmp"], "pre-child", **bindings)
    assert next(row["status"] for row in result["checks"] if row["id"] == "operational.installation-summary") == ("PASS" if fault is None else "MISMATCH")


def child_artifacts(custody: dict, reused: bool = False, farm_authority: str | None = None) -> None:
    constants, bindings, orch = custody["constants"], custody["bindings"], custody["orch"]
    for name in ("SCHEMA_RECORD_CLOSURE", "SCHEMA_SOURCE_MANIFEST", "SCHEMA_DIRECT_URL"):
        path = custody["tmp"] / name
        path.write_text("{}\n")
        bindings[name] = str(path)
    schema = {"origin": "https://github.com/banodoco/ArtAgents.git",
              "commit": "242f9c4306bf3b501222cb041a9eb246ef47bc85",
              "subdirectory": "packages/timeline-schema/python", "source_tree": "75a5a697f630affee40632e500b3f5b704a9b834",
              "input_kind": "installed_distribution", "package": "banodoco-timeline-schema", "version": "0.0.2",
              "record_rows": 18, "record_hashed_rows": 12, "tree_tie": "UNAVAILABLE", "record_sha256": sha(b"{}\n"),
              "manifest_sha256": sha(b"{}\n"), "direct_url_sha256": sha(b"{}\n")}
    schema_text = json.dumps(schema, sort_keys=True, separators=(",", ":"))
    client_tuple = dict(line.split("=", 1) for line in custody["client_identity"].splitlines())
    if farm_authority is None:
        client_tuple["__timeline_schema_identity__"] = schema_text
    identity = {"agent_sha": constants["AGENT_SHA"], "backend_sha": constants["RUNTIME_SHA"],
                "client_tuple": client_tuple, "bootstrap_authority": "b" * 64}
    parts = ["child", identity["agent_sha"], identity["backend_sha"], client_tuple, identity["bootstrap_authority"]]
    if farm_authority is not None:
        identity["farm_authority"] = farm_authority
        parts.append(farm_authority)
    key = sha(json.dumps(parts, sort_keys=True, separators=(",", ":")).encode())
    store = custody["tmp"] / "work/bench-store"
    child = store / "entries" / ("child-" + key)
    (child / "bin").mkdir(parents=True)
    (child / "bin/python").write_text("#!/bin/sh\nexit 1\n")
    (child / "bin/python").chmod(0o755)
    bindings["P4_PYTHON"] = bindings["CHILD_PYTHON"] = str(child / "bin/python")
    imports = ""
    for name in ("astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client"):
        origin = child / "lib/python3.13/site-packages" / name / "__init__.py"
        origin.parent.mkdir(parents=True)
        origin.write_text("")
        imports += f"{name}={origin}\n"
    metadata = ("schema_source_identity=" + schema_text + "\n" if farm_authority is None else "") + "astrid_name=astrid\n"
    for name, data in ((".astrid-import-origins", imports),
                       (".bootstrap-authority", identity["bootstrap_authority"] + "\n"),
                       (".astrid-distribution-metadata", metadata), (".astrid-source-commit", constants["AGENT_SHA"] + "\n"),
                       (".astrid-runtime-source-commit", constants["RUNTIME_SHA"] + "\n"),
                       (".astrid-runtime-client-identity", custody["client_identity"] + "\n")):
        (child / name).write_text(data)
    if farm_authority is None:
        (child / ".schema-source-identity").write_text(schema_text + "\n")
    schema_header = f"schema_source_identity_sha256={sha(schema_text.encode())}\n" if farm_authority is None else ""
    report = (f"status=passed\nagent_sha={constants['AGENT_SHA']}\nruntime_sha={constants['RUNTIME_SHA']}\n"
              f"runtime_client_identity_sha256={sha(custody['client_identity'].encode())}\n"
              f"{schema_header}requirements_path=requirements/proof.lock\n"
              f"requirements_lock_sha256={constants['PROOF_LOCK_SHA']}\ninstalled_import_origins:\n{imports}"
              f"installed_distribution_metadata:\n{metadata}pip_freeze:\nastrid==0.1.0\n")
    (child / ".provision-report").write_text(report)
    (orch / "tests/provision").mkdir(parents=True)
    (orch / "tests/provision/venv-agent-child-d140.txt").write_text(report)
    # Execute the actual maker's pure success formatter, not a copy of its
    # protocol. report_bytes is already exercised by the custody maker suite.
    maker = (ROOT.parent / "ops-child-custody/make-child-venv").read_text()
    formatter = maker.split("def success_receipt(entry, report):", 1)[1].split("\nidentity =", 1)[0]
    namespace = {"pathlib": __import__("pathlib"), "hashlib": hashlib,
                 "report_bytes": lambda path: (path / ".provision-report").read_bytes(),
                 "tests": str(orch / "tests"), "name": "venv-agent-child-d140", "agent": constants["AGENT_SHA"],
                 "backend": constants["RUNTIME_SHA"], "remotion": "", "schema_required": "1" if farm_authority is None else "0", "schema_identity_json": schema_text}
    exec(compile(ast.parse("def success_receipt(entry, report):" + formatter), "maker formatter", "exec"), namespace)
    receipt = namespace["success_receipt"]({"path": str(child), "key": key, "reused": reused}, report.encode())
    path = orch / "queue/done/childvenv-venv-agent-child-d140"
    bind_artifact(custody, "CHILD_RECEIPT", path, (receipt + "\n").encode())
    # Retained normal registration files only; no Store is initialized or run.
    (store / "locks").mkdir()
    lock = store / "locks" / child.name
    lock.touch()
    owner = {"version": 1, "uid": os.getuid(), "id": "private-owner", "root": str(store), "tests": str(orch / "tests")}
    marker = {"owner": owner["id"], "component": "child", "key": key, "identity": identity}
    entry = {**marker, "path": str(child), "seq": 1,
             "node": [child.stat().st_dev, child.stat().st_ino], "lock": [lock.stat().st_dev, lock.stat().st_ino]}
    reg = {"env": "", "suite": "", "requires": [child.name], "report": report, "report_sha256": sha(report.encode())}
    reg["hash"] = sha(json.dumps(reg, sort_keys=True, separators=(",", ":")).encode())
    index = {"version": 1, "seq": 1, "entries": {child.name: entry}, "registrations": {"venv-agent-child-d140": reg},
             "retired": [], "retired_suites": []}
    for path, value in ((store / "owner.json", owner), (store / "index.json", index), (child / ".bench-owner.json", marker)):
        path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")))
    custody["child"] = child


@pytest.mark.parametrize("fault", [None, "reused", "producer", "schema", "digest", "tree", "report", "client", "path", "json-fallback"])
def test_registered_child_closes_real_success_and_provision_formats(custody: dict, fault: str | None) -> None:
    child_artifacts(custody, reused=fault == "reused")
    bindings, child = custody["bindings"], custody["child"]
    path = Path(bindings["CHILD_RECEIPT"])
    if fault == "producer":
        (custody["orch"] / "bin/request-child-venv").write_text("#!/bin/sh\nexit 0\n")
    elif fault == "schema":
        schema_path = child / ".schema-source-identity"
        old_schema = schema_path.read_text().strip()
        new_schema = old_schema.replace('"input_kind":"installed_distribution"', '"input_kind":"source_tree"')
        old_report = (child / ".provision-report").read_bytes()
        for artifact in (schema_path, child / ".astrid-distribution-metadata", child / ".provision-report",
                         custody["orch"] / "tests/provision/venv-agent-child-d140.txt"):
            artifact.write_text(artifact.read_text().replace(old_schema, new_schema).replace(sha(old_schema.encode()), sha(new_schema.encode())))
        new_report = (child / ".provision-report").read_bytes()
        data = path.read_bytes().replace(sha(old_report).encode(), sha(new_report).encode())
        data = data.replace(sha(old_schema.encode()).encode(), sha(new_schema.encode()).encode())
        bind_artifact(custody, "CHILD_RECEIPT", path, data)
    elif fault == "digest":
        bindings["CHILD_RECEIPT_SHA256"] = "0" * 64
    elif fault == "tree":
        script = custody["tmp"] / "git"
        script.write_text(script.read_text().replace(custody["constants"]["RUNTIME_TREE"], "0" * 40))
    elif fault == "report":
        (child / ".provision-report").write_text("status=passed\n")
    elif fault == "client":
        (child / ".astrid-runtime-client-identity").write_text("wrong\n")
    elif fault == "path":
        bindings["CHILD_PYTHON"] = "/detached/bin/python"
    elif fault == "json-fallback":
        value = {"status": "passed", "agent_sha": custody["constants"]["AGENT_SHA"],
                 "runtime_sha": custody["constants"]["RUNTIME_SHA"], "lock_sha256": custody["constants"]["PROOF_LOCK_SHA"],
                 "installed_import_origins": True}
        bind_artifact(custody, "CHILD_RECEIPT", path, json.dumps(value).encode())
    result = run_receiver(custody["tmp"], "post-child", **bindings)
    assert receipt_status(result, "CHILD_RECEIPT") == ("PASS" if fault in {None, "reused"} else "MISMATCH")


def d73_artifacts(custody: dict) -> None:
    bindings, constants = custody["bindings"], custody["constants"]
    values = {"format": "p4-d73-v1", "agent_parents": constants["AGENT_SHA"],
              "python": "/private/child/bin/python", "node": "/private/node", "profile": "/private/profile",
              "schema": "/private/schema", "node_version": "v20.19.4", "profile_lock_sha": "1" * 64,
              "profile_archive_sha": "2" * 64, "profile_registry_sha": "3" * 64,
              "composition_version": "0.0.14", "original_p4_test_hash": "4" * 64,
              "service_versions": "reviewed", "junit_paths": "/private/junit.xml"}
    bindings.update({"P4_PYTHON": values["python"], "NODE_BIN": values["node"], "PROFILE": values["profile"]})
    for kind in ("agent", "runtime", "app", "composition"):
        values[kind + "_sha"] = constants[kind.upper() + "_SHA"]
        values[kind + "_tree"] = constants[kind.upper() + "_TREE"]
        values[kind + "_path"] = bindings[kind.upper() + "_CHECKOUT"]
    data = "".join(f"{key}={value}\n" for key, value in values.items()).encode()
    (custody["orch"] / "tests").mkdir(exist_ok=True)
    bind_artifact(custody, "P4_D73_MANIFEST", custody["orch"] / "tests/positive.manifest", data)
    evidence = custody["orch"] / "tests/d140-keep"
    evidence.mkdir(parents=True)
    bindings.update(P4_D73_EVIDENCE=str(evidence), KEEP_ROOT=str(evidence), P4_D73_REQUEST_ID="d140-positive")
    bind_artifact(custody, "FARM_D73_RECEIPT", evidence / "d140-positive.manifest", data)
    # Run only the launcher's actual harmless evidence writer, with its parser.
    # No preflight, original P4 test, child import or body executes.
    launcher = Path(bindings["D73_LAUNCHER"]).read_text()
    parser = launcher[launcher.index("declare -A pin"):launcher.index("\nrequired=(")]
    writer = "evidence=${" + launcher.split("evidence=${", 1)[1].split("\npreflight()", 1)[0]
    subprocess.run(["bash", "-c", "manifest=$1\n" + parser + "\n" + writer, "writer", bindings["P4_D73_MANIFEST"]],
                   env={**os.environ, "P4_D73_EVIDENCE": str(evidence), "P4_D73_REQUEST_ID": "d140-positive"}, check=True)
    for suffix, content in (("preflight.exit", "0\n"), ("body.exit", "17\n"), ("preflight.log", ""), ("body.log", ""), ("command", "stub\n")):
        (evidence / f"d140-positive.{suffix}").write_text(content)


@pytest.mark.parametrize("fault", [None, "producer", "schema", "digest", "tree", "copy", "missing-field", "parents", "input"])
def test_d73_receipt_authenticates_manager_digest_and_all_sources(custody: dict, fault: str | None) -> None:
    d73_artifacts(custody)
    bindings = custody["bindings"]
    if fault == "producer":
        Path(bindings["D73_LAUNCHER"]).write_text("#!/bin/sh\nexit 0\n")
    elif fault == "digest":
        bindings["FARM_D73_RECEIPT_SHA256"] = "0" * 64
    elif fault == "copy":
        path = Path(bindings["FARM_D73_RECEIPT"])
        bind_artifact(custody, "FARM_D73_RECEIPT", path, path.read_bytes() + b"# changed\n")
    elif fault in {"schema", "tree", "missing-field", "parents", "input"}:
        data = Path(bindings["P4_D73_MANIFEST"]).read_bytes()
        if fault == "schema":
            data = data.replace(b"format=p4-d73-v1", b"format=timeline.synthetic/v1")
        elif fault == "tree":
            data = data.replace(custody["constants"]["APP_TREE"].encode(), b"0" * 40)
        elif fault == "missing-field":
            data = data.replace(b"service_versions=reviewed\n", b"")
        elif fault == "parents":
            data = data.replace(b"agent_parents=", b"agent_parents=wrong-")
        else:
            data = data.replace(b"python=/private/child/bin/python", b"python=/other/bin/python")
        for name in ("P4_D73_MANIFEST", "FARM_D73_RECEIPT"):
            bind_artifact(custody, name, Path(bindings[name]), data)
    result = run_receiver(custody["tmp"], "post-launch", **bindings)
    assert receipt_status(result, "FARM_D73_RECEIPT") == ("PASS" if fault is None else "MISMATCH")


def checker_module(custody: dict, monkeypatch):
    module = types.ModuleType("private_d140_checker")
    exec(compile((Path(custody["bindings"]["receiver"]).parent / "receipts.py").read_bytes(), "private receiver", "exec"), module.__dict__)
    for name, value in {**custody["constants"], **custody["bindings"]}.items():
        if isinstance(value, str):
            monkeypatch.setenv(name, value)
    return module


def checker_call(module, monkeypatch, kind: str, name: str) -> int:
    monkeypatch.setattr(sys, "argv", ["receipts.py", kind, name])
    return module.main()


@pytest.fixture(scope="module")
def genuine_wheel_receipt():
    """Validate the original five wheels in place, without copying a bench."""
    orch = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
    seed = types.ModuleType("private_seed_control")
    seed.__file__ = str(orch / "bin/verify_dependency_seed.py")
    data = Path(seed.__file__).read_bytes()
    assert sha(data) == "116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2"
    exec(compile(data, seed.__file__, "exec"), seed.__dict__)
    component = seed.farm_component()
    wheelhouse = orch / "workers/rt-OPS-farm-bootstrap-wheel-input-0932/evidence/bootstrap-wheel-input/wheelhouse"
    wheels = component.validate_wheel_inputs(wheelhouse)
    assert wheels["schema"] == "timeline.farm-distribution-inputs.v1"
    assert len(wheels["roles"]["bootstrap3"]) == 3
    assert len(wheels["roles"]["test2"]) == 2
    assert wheels["roles"]["additional"] == []
    assert len(wheels["lock"]) == len(wheels["distributions"]) == 5
    assert wheels["ownership"]
    assert wheels["component_identity"] == component._json_digest({k: v for k, v in wheels.items() if k != "component_identity"})
    return component, wheelhouse, wheels


def test_real_farm_producer_validates_exact_original_packet(genuine_wheel_receipt) -> None:
    component, wheelhouse, wheels = genuine_wheel_receipt
    assert component.validate_wheel_inputs(wheelhouse) == wheels
    with pytest.raises(component.ValidationError, match="additional wheel authority"):
        component.validate_wheel_inputs(wheelhouse, additional_wheels=[component.APPROVED_WHEELS[0]])


@pytest.mark.parametrize("phase", ["pre-child", "post-child"])
@pytest.mark.parametrize("fault", [None, "legacy", "identity", "roles", "raw", "retained", "mode", "registration"])
def test_farm_main_calls_real_producer_and_retention_boundary(custody: dict, monkeypatch, genuine_wheel_receipt, phase: str, fault: str | None) -> None:
    component, wheelhouse, _ = genuine_wheel_receipt
    # No genuine selected schema checkout is available. This explicit validator
    # double isolates the caller/retention seam; it is never a source positive.
    monkeypatch.setattr(component, "validate_schema_source", lambda _: {"private_schema_validator_double": True})
    packet = component.validate_farm_distribution_inputs(schema_source=custody["tmp"], wheelhouse=wheelhouse)
    if phase == "post-child":
        child_artifacts(custody, farm_authority=packet["component_identity"])
    module = checker_module(custody, monkeypatch)
    child = custody.get("child", custody["tmp"] / "absent-future-child")
    calls = []

    def inputs(source, archive):
        assert source == custody["tmp"]
        assert archive == archive_path
        calls.append("farm_inputs")
        return packet

    def retained(path, authority):
        assert path == child and authority == packet["component_identity"]
        calls.append("retained_farm")
        if fault == "retained":
            raise ValueError("dependency closure changed")
        return packet, {}, set()

    # The full source/archive validators are not replaced in production. This
    # control checks main -> kit -> exact helper args and canonical retention.
    monkeypatch.setattr(module, "seed_component", lambda _: types.SimpleNamespace(farm_inputs=inputs, retained_farm=retained))
    if fault == "registration" and phase == "post-child":
        index_path = child.parent.parent / "index.json"
        index = json.loads(index_path.read_bytes())
        index["registrations"]["venv-agent-child-d140"]["report_sha256"] = "0" * 64
        index_path.write_text(json.dumps(index))
    archive_path = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts") / f"bootstrap-wheel-input-0932-{module.ARCHIVE_SHA}.tgz"
    real_physical = module.physical

    def physical(path, directory=False):
        if Path(path) == custody["orch"] / "artifacts" / archive_path.name:
            return real_physical(archive_path)
        return real_physical(path, directory)

    monkeypatch.setattr(module, "physical", physical)
    monkeypatch.setenv("FARM_REQUIRED", "1")
    monkeypatch.setenv("FARM_DISTRIBUTION_SOURCE", str(custody["tmp"]))
    monkeypatch.setenv("D140_PHASE", phase)
    value = json.loads(module.canonical(packet))
    if fault == "legacy":
        value = {"schema": "timeline.ops.d137.installed-kit/v1", "status": "qualified_for_one_request"}
    elif fault == "identity":
        value["component_identity"] = "0" * 64
    elif fault == "roles":
        value["wheel_inputs"]["roles"]["test2"] = []
    raw = module.canonical(value) + (b"\n" if fault == "raw" else b"")
    path = child / ".farm-receipt.json"
    if phase == "post-child":
        path.write_bytes(raw)
        path.chmod(0o644 if fault == "mode" else 0o400)
        monkeypatch.setenv("FARM_D139A_KIT_RECEIPT", str(path))
        monkeypatch.setenv("FARM_D139A_KIT_RECEIPT_SHA256", sha(raw))
    # The pre-child check must ignore even a wrong future receipt. Post-child
    # must reject it despite a matching caller-supplied consistency hash.
    assert checker_call(module, monkeypatch, "kit", "FARM_D139A_KIT_RECEIPT") == (0 if phase == "pre-child" or fault is None else 1)
    assert calls == (["farm_inputs", "retained_farm"] if phase == "post-child" and fault in {None, "retained"} else ["farm_inputs"])
    if phase == "pre-child":
        assert not child.exists()


@pytest.mark.parametrize("fault", ["detached", "request-id", "runmanifest", "run-tuple", "preflight", "body-exit", "missing-runmanifest", "evidence-root"])
def test_d73_main_refuses_detached_or_changed_genuine_writer_outputs(custody: dict, monkeypatch, fault: str) -> None:
    d73_artifacts(custody)
    bindings = custody["bindings"]
    evidence = Path(bindings["P4_D73_EVIDENCE"])
    if fault == "detached":
        path = custody["tmp"] / "detached.manifest"
        bind_artifact(custody, "FARM_D73_RECEIPT", path, Path(bindings["FARM_D73_RECEIPT"]).read_bytes())
    elif fault == "evidence-root":
        bindings["KEEP_ROOT"] = str(custody["tmp"])
    else:
        suffix = {"request-id": "request-id", "runmanifest": "runmanifest", "run-tuple": "runmanifest", "preflight": "preflight.exit",
                  "body-exit": "body.exit", "missing-runmanifest": "runmanifest"}[fault]
        path = evidence / ("d140-positive." + suffix)
        if fault == "missing-runmanifest":
            path.rename(evidence / "detached.runmanifest")
        else:
            data = path.read_bytes()
            path.write_bytes(data.replace(custody["constants"]["AGENT_SHA"].encode(), b"0" * 40) if fault == "run-tuple" else data + b"changed\n")
    module = checker_module(custody, monkeypatch)
    assert checker_call(module, monkeypatch, "d73", "FARM_D73_RECEIPT") == 1


def test_matching_hash_cannot_register_an_arbitrary_owner_root(custody: dict) -> None:
    bindings = custody["bindings"].copy()
    bindings.pop("receiver")  # Use the actual production root policy.
    result = run_receiver(custody["tmp"], "pre-child", **bindings)
    assert receipt_status(result, "FARM_CURRENT_AGENT_RECEIPT") == "MISMATCH"
    assert result["status"] == "NOT_READY"


def test_real_normal_caller_uses_ordinary_route_and_special_join_still_refuses(custody: dict, monkeypatch) -> None:
    module = checker_module(custody, monkeypatch)
    assert checker_call(module, monkeypatch, "caller", "normal-request") == 0
    result = run_receiver(custody["tmp"], "pre-child", **custody["bindings"])
    assert next(row["status"] for row in result["checks"] if row["id"] == "route.normal-caller") == "PASS"
    assert next(row["status"] for row in result["checks"] if row["id"] == "route.ordinary-installed-schema") == "PASS"
    wrapper = (ROOT.parent / "ops-child-custody/request-child-venv").read_text()
    guard_end = wrapper.index('\nif [ "$SCHEMA_REQUIRED" = 1 ]; then')
    parser = wrapper[:guard_end]
    ordinary = subprocess.run(["bash", "-c", parser, "request-control", "venv-agent-child-d140", custody["constants"]["AGENT_SHA"],
                               "--schema-installed-distribution", "/private/dist-info", "--schema-source-manifest", "/private/manifest"],
                              capture_output=True, text=True, check=False)
    assert ordinary.returncode == 0
    special = subprocess.run(["bash", "-c", parser, "request-control", "venv-agent-child-d140", custody["constants"]["AGENT_SHA"],
                              "--farm-distributions", "--schema-installed-distribution", "/private/dist-info", "--schema-source-manifest", "/private/manifest"],
                             capture_output=True, text=True, check=False)
    assert special.returncode == 2
    assert "installed schema input cannot be combined with Farm schema authority" in special.stderr
    assert not list((custody["orch"] / "queue/done").glob("childvenv-*"))


def test_special_farm_profile_remains_strict(custody: dict, monkeypatch) -> None:
    monkeypatch.setenv("FARM_REQUIRED", "1")
    module = checker_module(custody, monkeypatch)
    assert checker_call(module, monkeypatch, "caller", "normal-request") == 1
    result = run_receiver(custody["tmp"], "pre-child", FARM_REQUIRED="1", **custody["bindings"])
    assert next(row["status"] for row in result["checks"] if row["id"] == "binding.FARM_DISTRIBUTION_SOURCE") == "MISSING"
    assert next(row["status"] for row in result["checks"] if row["id"] == "route.normal-caller") == "MISMATCH"
