from __future__ import annotations

import base64
import csv
import errno
import fcntl
import hashlib
import importlib.util
import io
import json
import os
import re
import shlex
import subprocess
import sys
import tarfile
from contextlib import contextmanager
from pathlib import Path

import pytest

PACKET = Path(__file__).parent
SOURCE = json.loads((PACKET / "runtime-source-selection.json").read_text())
ROW = (PACKET / "registration-row.txt").read_text()
BRIEF = (PACKET / "FARM-CODEX-BRIEF.md").read_text()
README = (PACKET / "README.md").read_text()


def installer_source() -> str:
    return BRIEF.split("<<'PY'\n", 1)[1].split("\nPY\n", 1)[0]


def test_manifest_is_reproducible():
    for line in (PACKET / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert hashlib.sha256((PACKET.parent.parent / name).read_bytes()).hexdigest() == digest


def test_exact_source_and_graph_are_carryovers():
    assert SOURCE["agent_commit_tested_by_checkpoint"] == "9cd3dbe865a941c052bda04ae0d61306d18f8f26"
    assert SOURCE["agent_tree_tested_by_checkpoint"] == "57f0231da0d7904ecd8778169973d6384e0ae141"
    assert SOURCE["required_runtime_source_commit"] == "1d9ddba546f8fb1300f55ff62607ed492719cbaa"
    assert SOURCE["required_runtime_tree"] == "f56c396c4495547680b46e832565278d2c375e69"
    assert SOURCE["declared_runtime_source_commit"].startswith("45c3a7f4")
    assert SOURCE["remotion_base_suite"] == "remotion-env-nodes"
    assert SOURCE["remotion_registration"] == "agent-remotion-farm-v2-9cd"
    assert SOURCE["remotion_lock_sha256"] == "f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d"


def test_request_is_the_supported_normal_maker_route():
    assert "request-child-venv" in README
    for value in (
        "venv-agent-child-farm-v3-9cd",
        "9cd3dbe865a941c052bda04ae0d61306d18f8f26",
        "remotion-env-nodes",
        "agent-remotion-farm-v2-9cd",
        "/home/user/work/wt/agt-pin-9cd3dbe8",
        "/home/user/work/wt/rt-pin-1d9ddba5",
        "1d9ddba546f8fb1300f55ff62607ed492719cbaa",
    ):
        assert value in README
    assert "--source-carrier" in README
    assert "request-runtime" not in README


def test_candidate_row_is_one_line_isolated_and_preserves_remotion_carriers():
    assert ROW.count("\n") == 1
    assert " PYTHONPATH=" not in ROW
    assert " -I -c " in ROW
    assert "@CHILD_ROOT@" in ROW
    assert "@CHILD_INTERPRETER@" in ROW
    assert "@MANAGED_PROFILE@" in ROW
    assert "@RUNTIME_CHECKOUT@" in ROW
    assert "ASTRID_TEST_NODE_MODULES=@MANAGED_PROFILE@/node_modules" in ROW
    assert "v20.19.4" in ROW and "10.8.2" in ROW
    assert "pytest.main([\"-q\",\"-n\",\"3\"])" in ROW


def test_installer_is_syntax_valid_and_never_creates_a_child():
    compile(installer_source(), "farm-agent-full-v3-installer", "exec")
    assert "Store.initialize" not in installer_source()
    assert "request-child-venv" not in installer_source()
    assert "pip install" not in installer_source()
    assert '"git", "-C"' in installer_source()


@pytest.mark.parametrize(
    ("case", "required"),
    [
        ("wrong Agent", "Agent marker mismatch"),
        ("wrong Runtime", "Runtime marker mismatch"),
        ("wrong client", "client tuple mismatch"),
        ("missing receipt", "D21b child receipt/registration missing"),
        ("wrong interpreter", "child interpreter is not retained"),
        ("wrong Node", "Node20/npm"),
        ("wrong graph", "managed Remotion registration missing"),
        ("wrong Store owner", "child receipt is not singular managed custody"),
        ("wrong key", "client tuple mismatch"),
        ("wrong proof lock", "declared Runtime lock drift"),
    ],
)
def test_installer_names_each_refusal_boundary(case, required):
    # These are deliberately source-level private-fixture contracts: the live
    # Store and Farm are out of scope for this packet, while each refusal must
    # remain visible in the installer body for a fixture to exercise.
    text = installer_source() + "\n" + ROW
    if case == "wrong Node":
        assert "Node version mismatch" in text and "npm version mismatch" in text
    elif case == "wrong graph":
        assert required in text
    else:
        assert required in text


def test_child_identity_requires_exact_receipt_markers_and_origins():
    text = installer_source()
    for marker in (
        ".provision-report",
        ".astrid-source-commit",
        ".astrid-runtime-source-commit",
        ".astrid-runtime-client-identity",
        "report_bytes",
        "status=passed",
        "STORE_VERIFY_BEGIN",
        "registration_entries(child_name)",
    ):
        assert marker in text
    assert "existence-only" not in text


def test_registry_update_is_scoped_atomic_and_recoverable():
    text = installer_source()
    for marker in (
        "rows.count(full) == 1",
        "len(old) == 1",
        "with store.mutex()",
        "api.atomic",
        "backup.open(\"xb\")",
        "registry drift",
        "outside_bytes=unchanged",
    ):
        assert marker in text
    assert "owner.json" not in text and "index.json" not in text


def test_no_source_overlay_or_isolation_bypass_is_encoded():
    forbidden = (".pth", " PYTHONPATH=", "sys.path.insert", "sys.path.append", "pip install", "Store.initialize")
    assert all(token not in ROW + installer_source() for token in forbidden)
    assert "python -I" in BRIEF or " -I -c " in ROW


def test_missing_actual_farm_inputs_are_named():
    normalized = " ".join(BRIEF.split())
    for phrase in (
        "current Store owner/index",
        "current registry bytes",
        "existing `agent full` and single `agent full-farm` rows",
        "successful D21b child receipt",
        "Farm must stop",
        "not an actual Farm READY result",
    ):
        assert phrase in normalized or phrase in README


def test_no_literal_staging_head_or_synthetic_ready_claim():
    all_text = ROW + BRIEF + (PACKET / "README.md").read_text()
    assert "stagingHEAD" not in all_text
    assert "Farm READY" in all_text
    assert "synthetic packet test is not an actual Farm READY result" in all_text


ORCH = Path(os.environ.get(
    "FARM_ORCH_ROOT",
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch",
))
NODE_BIN = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin"
FULL = b"agent       full              /home/user/work/venv-agent/bin/python -m pytest -q -n 3\n"
OLD = b"agent full-farm /bin/false\n"
BODY = 'raise SystemExit(pytest.main(["-q","-n","3"]))'


def _api():
    spec = importlib.util.spec_from_file_location("fixture_store", ORCH / "bin/bench_store.py")
    module = importlib.util.module_from_spec(spec)
    # Never write a cache beside the installed helper.
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def _archive(files):
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        for name, content in files.items():
            info = tarfile.TarInfo(name)
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))
    return stream.getvalue()


def _record(site, folder, paths):
    stream = io.StringIO()
    writer = csv.writer(stream)
    for rel in sorted(paths):
        content = (site / rel).read_bytes()
        encoded = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
        writer.writerow([rel, "sha256=" + encoded, str(len(content))])
    writer.writerow([folder + "/RECORD", "", ""])
    (site / folder / "RECORD").write_text(stream.getvalue())


@pytest.fixture
def private(monkeypatch, tmp_path):
    # Tiny invented source archives, distributions and graph, never copied
    # benches/checkouts. They exercise production validators, not Farm identity.
    api = _api()
    orch = tmp_path / "orch"
    tests = orch / "tests"
    tests.mkdir(parents=True)
    (tests / "suites.conf").write_bytes(b"# preserve\r\n#" + OLD + FULL + OLD + b"agent outside /bin/true\n")
    (orch / "bin").mkdir()
    for name in ("bench_store.py", "make-child-venv"):
        (orch / "bin" / name).symlink_to(ORCH / "bin" / name)
    store = api.Store.initialize(tmp_path / "bench-store", tests)
    profile_entry = store.ensure(
        "runtime", {"remotion_tree": "b01dca9b3b24f54093c20b7c5657316f997725db"},
        {"name": SOURCE["remotion_registration"], "env": "PROFILE={bench_path}\n", "suite": ""},
        lambda stage, final: None, lambda path: None,
    )
    profile = Path(profile_entry["path"])
    (profile / "package-lock.json").write_text("private graph lock\n")
    (profile / "package.json").write_text('{"private":true}')
    peers = ["react", "react-dom", "remotion", "esbuild", "typescript", "@remotion/renderer",
             "@remotion/bundler", "@remotion/media", "@remotion/layout-utils", "@banodoco/timeline-composition"]
    for name in peers:
        folder = profile / "node_modules" / name
        folder.mkdir(parents=True)
        (folder / "package.json").write_text(json.dumps({"name": name, "main": "index.js"}))
        (folder / "index.js").write_text("module.exports={};\n")
    files = {
        "agent": {"astrid/__init__.py": b"", "astrid/core/__init__.py": b"",
                  "astrid/core/timeline/__init__.py": b"", "astrid/core/timeline/banodoco_schema.py": b"",
                  "runtime.lock.json": b"{}\n", "requirements/proof.lock": b"fixture proof\n"},
        "runtime": {"astrid_runtime/__init__.py": b"", "runtime_protocol/__init__.py": b"",
                    "runtime_protocol/external_pack_sources.py": b"# private D40 fixture\n"},
    }
    for name in SOURCE["canonical_client_sha256"]:
        files["agent"][name] = b"# private client fixture\n"
    for name, distribution, includes in (("agent", "astrid", '["astrid*", "astrid_runtime_client*"]'),
                                         ("runtime", "astrid-runtime", '["astrid_runtime*", "runtime_protocol*"]')):
        files[name]["pyproject.toml"] = (f'[project]\nname="{distribution}"\nversion="0.1.0"\n'
                                              f'[tool.setuptools.packages.find]\ninclude={includes}\n').encode()
    selection = dict(SOURCE)
    selection["remotion_lock_sha256"] = hashlib.sha256((profile / "package-lock.json").read_bytes()).hexdigest()
    selection["canonical_client_sha256"] = {
        name: hashlib.sha256(files["agent"][name]).hexdigest() for name in SOURCE["canonical_client_sha256"]
    }
    for key, content in (("required_runtime_module_sha256", files["runtime"]["runtime_protocol/external_pack_sources.py"]),
                         ("declared_runtime_lock_sha256", files["agent"]["runtime.lock.json"]),
                         ("proof_lock_sha256", files["agent"]["requirements/proof.lock"])):
        selection[key] = hashlib.sha256(content).hexdigest()
    client = "\n".join("packages/python/" + name + "=" + value
                       for name, value in sorted(selection["canonical_client_sha256"].items()))
    checkouts = {}
    for name, source_files in files.items():
        checkout = tmp_path / name
        checkout.mkdir()
        checkouts[name] = checkout
        for rel, content in source_files.items():
            path = checkout / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    identity = {"agent_sha": SOURCE["agent_commit_tested_by_checkpoint"],
                "backend_sha": SOURCE["required_runtime_source_commit"],
                "client_tuple": dict(line.split("=", 1) for line in client.splitlines())}
    child_path = store.root / "entries" / ("child-" + api.key_for("child", identity))
    report = []

    def build(stage, final):
        (stage / "bin").mkdir()
        # One interpreter binary, not a copied venv or dependency install.
        (stage / "bin/python").write_bytes(Path(SOURCE["maker_python"]).read_bytes())
        (stage / "bin/python").chmod(0o700)
        (stage / "pyvenv.cfg").write_text("home = /usr/bin\ninclude-system-site-packages = false\n")
        site = stage / "lib/python3.13/site-packages"
        site.mkdir(parents=True)
        snapshot = stage / ".child-venv-source-fixture"
        metadata = []
        for name, dist in (("agent", "astrid"), ("runtime", "astrid-runtime")):
            installed = []
            for rel, content in files[name].items():
                retained = snapshot / name / rel
                retained.parent.mkdir(parents=True, exist_ok=True)
                retained.write_bytes(content)
                if rel.endswith(".py"):
                    path = site / rel
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content)
                    installed.append(rel)
            folder = dist.replace("-", "_") + "-0.1.0.dist-info"
            (site / folder).mkdir()
            url = (final / snapshot.name / name).as_uri()
            for rel, content in {
                "METADATA": f"Metadata-Version: 2.1\nName: {dist}\nVersion: 0.1.0\n",
                "direct_url.json": json.dumps({"url": url, "dir_info": {}}),
            }.items():
                (site / folder / rel).write_text(content)
                installed.append(folder + "/" + rel)
            _record(site, folder, installed)
            metadata.extend([f"{dist}_name={dist}", f"{dist}_version=0.1.0", f"{dist}_direct_url={url}", f"{dist}_provenance=directory"])
        for name in ("pytest", "xdist", "banodoco_timeline_schema"):
            (site / name).mkdir()
            (site / name / "__init__.py").write_text("")
        origins = "".join(f"{name}={final}/lib/python3.13/site-packages/{name}/__init__.py\n"
                          for name in ("astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client"))
        markers = {".astrid-source-commit": identity["agent_sha"] + "\n",
                   ".astrid-runtime-source-commit": identity["backend_sha"] + "\n",
                   ".astrid-runtime-client-identity": client + "\n", ".astrid-import-origins": origins,
                   ".astrid-distribution-metadata": "\n".join(metadata) + "\n"}
        for marker, value in markers.items():
            (stage / marker).write_text(value)
        value = (f"status=passed\nagent_sha={identity['agent_sha']}\nruntime_sha={identity['backend_sha']}\n"
                 f"runtime_client_identity_sha256={hashlib.sha256(client.encode()).hexdigest()}\n"
                 f"requirements_path=requirements/proof.lock\nrequirements_lock_sha256={selection['proof_lock_sha256']}\n"
                 "installed_import_origins:\n" + origins + "installed_distribution_metadata:\n" + markers[".astrid-distribution-metadata"] +
                 "pip_freeze:\n" + "".join(f"{dist} @ {(final / snapshot.name / name).as_uri()}\n"
                                             for name, dist in (("agent", "astrid"), ("runtime", "astrid-runtime"))))
        (stage / ".provision-report").write_text(value)
        report.append(value)

    def seal(path):
        for item in [*path.rglob("*"), path]:
            item.chmod(item.stat().st_mode & ~0o222)

    store.ensure("child", identity,
                 lambda path, final, reused: {"name": SOURCE["child_name"], "env": "", "suite": "",
                                               "require_names": [SOURCE["remotion_registration"]], "report": report[0]},
                 build, lambda path: None, seal=seal)
    packet = tmp_path / "packet"
    packet.mkdir()
    (packet / "runtime-source-selection.json").write_text(json.dumps(selection))
    row = ROW
    for key in ("required_runtime_module_sha256", "declared_runtime_lock_sha256", "remotion_lock_sha256"):
        row = row.replace(SOURCE[key], selection[key])
    for name, digest in SOURCE["canonical_client_sha256"].items():
        row = row.replace(digest, selection["canonical_client_sha256"][name])
    row = row.replace("da2728a6903be1c676de1ed954a3ecea589b698a6d205f436457efdf368069e9",
                      hashlib.sha256((client + "\n").encode()).hexdigest())
    (packet / "registration-row.txt").write_text(row)
    real_output = subprocess.check_output
    real_run = subprocess.run

    def output(argv, **kwargs):
        if argv[0] == "git" and argv[2] in {str(v) for v in checkouts.values()}:
            name = next(k for k, v in checkouts.items() if str(v) == argv[2])
            if argv[3] == "archive":
                return _archive(files[name])
            if argv[3] == "status":
                return ""
            key = ("agent_commit_tested_by_checkpoint" if name == "agent" else "required_runtime_source_commit")
            if argv[-1] == "HEAD^{tree}":
                key = "agent_tree_tested_by_checkpoint" if name == "agent" else "required_runtime_tree"
            return SOURCE[key] + "\n"
        return real_output(argv, **kwargs)

    def run(argv, **kwargs):
        if kwargs.get("input", "").startswith("import base64, csv, fnmatch"):
            # Execute the maker verifier unchanged, only Git object retrieval is
            # replaced with the tiny invented committed archive above.
            with monkeypatch.context() as patch:
                patch.setattr(sys, "argv", ["-", *argv[4:]])
                exec(compile(kwargs["input"], "normal-maker-verifier", "exec"), {})  # noqa: S102 - pinned maker code
            return subprocess.CompletedProcess(argv, 0)
        return real_run(argv, **kwargs)

    monkeypatch.setattr(subprocess, "check_output", output)
    monkeypatch.setattr(subprocess, "run", run)
    return {"store": store, "profile": profile, "tests": tests, "child": child_path,
            "packet": packet, "agent": checkouts["agent"], "runtime": checkouts["runtime"],
            "selection": selection, "files": files, "seal": seal}


def _install(monkeypatch, private, baseline=None):
    tests = private["tests"]
    snapshot = tests.parent / "baseline.conf"
    snapshot.write_bytes((tests / "suites.conf").read_bytes() if baseline is None else baseline)
    argv = ["-", str(tests.parent), str(private["store"].root), str(private["packet"]),
            str(private["child"]), str(private["profile"]), str(private["runtime"]),
            str(private["agent"]), str(snapshot), str(tests.parent)]
    with monkeypatch.context() as patch:
        patch.setattr(sys, "argv", argv)
        exec(compile(installer_source(), "guarded-installer", "exec"), {})  # noqa: S102 - packet under test
    return (tests / "suites.conf").read_bytes()


def _selected(tests):
    source = (ORCH / "bin/test-run").read_text()
    assert hashlib.sha256(source.encode()).hexdigest() == SOURCE["test_run_sha256"]
    line = next(line for line in source.splitlines() if line.startswith("CMD=$(awk "))
    extraction = line.split("); [ -n", 1)[0] + ")"
    return subprocess.check_output(["bash", "-c", extraction + '\nprintf "%s" "$CMD"'],
                                   env={"PATH": "/usr/bin:/bin", "O": str(tests.parent),
                                        "repo": "agent", "suite": "full-farm"}, text=True)


def _suite_lease():
    source = (ORCH / "bin/test-run").read_text()
    code = source.split("@contextmanager\ndef suite_lease", 1)[1].split("\n\ndef supervise", 1)[0]
    namespace = {"contextmanager": contextmanager, "Path": Path}
    exec("@contextmanager\ndef suite_lease" + code, namespace)  # noqa: S102 - pinned caller code
    return namespace["suite_lease"]


def _run(command, agent, fds=()):
    prefix, payload = command.rsplit(" -c ", 1)
    code, = shlex.split(payload)
    assert code.count(BODY) == 1
    diagnostic = (f"[os.fstat(fd) for fd in {list(fds)!r}]; "
                  'print("PRIVATE_DIAGNOSTIC="+json.dumps(dict(executable=sys.executable,env=dict(os.environ),cwd=str(root)),sort_keys=True))')
    probe = "import astrid, runtime_protocol, os; assert \"PYTHONPATH\" not in os.environ; print(astrid.__file__, runtime_protocol.__file__)"
    diagnostic += f"; print(\"ISOLATED_CHILD=\"+subprocess.check_output([sys.executable,\"-I\",\"-c\",{probe!r}],text=True,pass_fds={tuple(fds)!r}).strip())"
    code = code.replace(BODY, diagnostic)
    return subprocess.run(["bash", "-c", prefix + " -c " + shlex.quote(code)], cwd=agent,
                          env={"PATH": "/usr/bin:/bin", "PYTHONPATH": "/wrong-ambient",
                               "PYTHONNOUSERSITE": "1", "ASTRID_RUNTIME_CHECKOUT": "/wrong"},
                          pass_fds=tuple(fds), capture_output=True, text=True, timeout=30, check=False)


def test_existing_store_installer_and_actual_production_caller(monkeypatch, private):
    store, tests = private["store"], private["tests"]
    before = (tests / "suites.conf").read_bytes()
    metadata = [(store.root / name).read_bytes() for name in ("owner.json", "index.json")]
    post = _install(monkeypatch, private)
    candidate, = [row for row in post.splitlines(keepends=True) if row.split(None, 2)[:2] == [b"agent", b"full-farm"]]
    assert post == b"".join(candidate if row == OLD else row for row in before.splitlines(keepends=True))
    assert FULL in post
    assert [(store.root / name).read_bytes() for name in ("owner.json", "index.json")] == metadata
    backup, = tests.parent.glob("suites-*.conf")
    assert backup.read_bytes() == before
    assert re.fullmatch(r"suites-\d{8}T\d{6}\.\d{6}Z.conf", backup.name)
    selected = _selected(tests)
    assert selected == " ".join(candidate.decode().split(None, 2)[2].split())
    with _suite_lease()(store, "agent", "full-farm", selected, tests) as (entries, fds):
        assert {e["path"] for e in entries} == {str(private["child"]), str(private["profile"])}
        locks = [store.root / "locks" / (e["component"] + "-" + e["key"]) for e in entries]
        for lock in locks:
            with lock.open("r+") as stream, pytest.raises(BlockingIOError):
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        snapshot = _snapshot(private)
        result = _run(selected, snapshot, fds)
        assert result.returncode == 0, result.stdout + result.stderr
        observed = json.loads(result.stdout.split("PRIVATE_DIAGNOSTIC=", 1)[1].splitlines()[0])
        assert observed["cwd"] == str(snapshot)
        print("PRODUCTION_CALLER_PRIVATE", json.dumps(observed, sort_keys=True))
        assert observed["executable"] == str(private["child"] / "bin/python")
        assert "PYTHONPATH" not in observed["env"] and "PYTHONNOUSERSITE" not in observed["env"]
        assert observed["env"]["ASTRID_RUNTIME_CHECKOUT"] == str(private["runtime"])
        assert observed["env"]["ASTRID_TEST_NODE_MODULES"] == str(private["profile"] / "node_modules")
        assert "PROFILE_PEERS_OK" in result.stdout and "CHILD_ORIGINS" in result.stdout
    for fd in fds:
        with pytest.raises(OSError) as error:
            os.fstat(fd)
        assert error.value.errno == errno.EBADF
    for lock in locks:
        with lock.open("r+") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)


def _damage(path, content):
    path.chmod(path.stat().st_mode | 0o200)
    path.write_text(content)
    path.chmod(path.stat().st_mode & ~0o222)


@pytest.mark.parametrize(("fault", "reason"), [
    ("agent", "Agent marker mismatch"), ("runtime", "Runtime marker mismatch"),
    ("client", "client tuple mismatch"), ("lock", "proof lock drift"),
    ("report", "provision report identity mismatch"), ("receipt", "provision report identity mismatch"),
    ("record", "RECORD bytes mismatch"), ("direct_url", "source is not a noneditable"),
    ("source", "retained source differs"), ("origin", "import origin mismatch"),
    ("owner", "entry ownership/path mismatch"), ("key", "entry identity mismatch"),
    ("tuple", "child registered identity/key mismatch"), ("report_projection", "registration report changed"),
])
def test_private_custody_negatives(monkeypatch, private, fault, reason):
    child, store = private["child"], private["store"]
    tests = private["tests"]
    before = (tests / "suites.conf").read_bytes()
    site = child / "lib/python3.13/site-packages"
    if fault in ("agent", "runtime", "client"):
        marker = {"agent": ".astrid-source-commit", "runtime": ".astrid-runtime-source-commit", "client": ".astrid-runtime-client-identity"}[fault]
        _damage(child / marker, "wrong\n")
    elif fault == "lock":
        (private["agent"] / "requirements/proof.lock").write_text("wrong")
    elif fault in ("report", "receipt"):
        # Change both authenticated projections for the semantic-report case;
        # merely changing a field must still fail normal-maker validation.
        report_path = child / ".provision-report"
        value = report_path.read_text().replace("status=passed", "status=not-passed")
        _damage(report_path, value)
        if fault == "report":
            projection = tests / "provision" / (SOURCE["child_name"] + ".txt")
            projection.write_text(value)
            index = json.loads((store.root / "index.json").read_text())
            reg = index["registrations"][SOURCE["child_name"]]
            reg.update(report=value, report_sha256=hashlib.sha256(value.encode()).hexdigest())
            reg["hash"] = _api().digest(_api().canonical({k: v for k, v in reg.items() if k != "hash"}))
            (store.root / "index.json").write_text(json.dumps(index))
    elif fault == "record":
        _damage(site / "astrid/__init__.py", "wrong bytes")
    elif fault == "direct_url":
        path = site / "astrid-0.1.0.dist-info/direct_url.json"
        value = json.loads(path.read_text())
        value["dir_info"]["editable"] = True
        _damage(path, json.dumps(value))
    elif fault == "source":
        _damage(child / ".child-venv-source-fixture/agent/astrid/__init__.py", "wrong bytes")
    elif fault == "origin":
        _damage(child / ".astrid-import-origins", (child / ".astrid-import-origins").read_text().replace("astrid/__init__.py", "astrid/core/__init__.py"))
    elif fault in ("owner", "key", "tuple"):
        index = json.loads((store.root / "index.json").read_text())
        entry = next(e for e in index["entries"].values() if e["component"] == "child")
        if fault == "owner":
            entry["owner"] = "wrong"
        elif fault == "key":
            entry["key"] = "0" * 64
        else:
            # A self-consistent different registered tuple is tested by changing
            # the packet's expected identity, leaving actual Store custody intact.
            selection = private["selection"]
            selection["agent_commit_tested_by_checkpoint"] = "0" * 40
            (private["packet"] / "runtime-source-selection.json").write_text(json.dumps(selection))
        (store.root / "index.json").write_text(json.dumps(index))
    else:
        (tests / "provision" / (SOURCE["child_name"] + ".txt")).write_text("wrong projection")
    with pytest.raises((AssertionError, RuntimeError, SystemExit), match=reason):
        _install(monkeypatch, private)
    assert (tests / "suites.conf").read_bytes() == before
    assert not list(tests.parent.glob("suites-*.conf"))


def _snapshot(private):
    snapshot = private["tests"].parent / "staged-agent-snapshot"
    snapshot.mkdir()
    for rel, content in private["files"]["agent"].items():
        path = snapshot / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return snapshot


@pytest.mark.parametrize(("fault", "reason"), [
    ("node", "Node version mismatch"), ("npm", "npm version mismatch"),
    ("peer", "missing profile peer"), ("profile_lock", "Remotion lock drift"),
    ("source", "D40 source mismatch"), ("client", "canonical client drift"),
    ("lock", "declared Runtime lock drift"), ("receipt", "child receipt drift"),
    ("interpreter", "child interpreter mismatch"),
])
def test_rendered_row_preflight_refuses_before_body(monkeypatch, private, tmp_path, fault, reason):
    _install(monkeypatch, private)
    selected = _selected(private["tests"])
    snapshot = _snapshot(private)
    if fault in ("node", "npm"):
        tools = tmp_path / "tools"
        tools.mkdir()
        for name, version in (("node", "v22.22.0" if fault == "node" else "v20.19.4"),
                              ("npm", "9.0.0" if fault == "npm" else "10.8.2")):
            tool = tools / name
            tool.write_text(f"#!/bin/sh\nif [ \"$1\" = --version ]; then printf '%s\\n' '{version}'; else exec {NODE_BIN}/{name} \"$@\"; fi\n")
            tool.chmod(0o700)
        selected = selected.replace(NODE_BIN, str(tools))
    elif fault == "peer":
        _damage(private["profile"] / "node_modules/react/package.json", '{"main":"missing.js"}')
        # Keep the real Node resolver in the path, but make the mandatory file
        # absent by renaming one private fixture file.
        path = private["profile"] / "node_modules/@remotion/media/package.json"
        path.rename(path.with_name("wrong.json"))
    elif fault == "profile_lock":
        (private["profile"] / "package-lock.json").write_text("wrong lock")
    elif fault == "source":
        _damage(private["child"] / "lib/python3.13/site-packages/runtime_protocol/external_pack_sources.py", "# drift\n")
    elif fault in ("client", "lock"):
        path = snapshot / ("astrid_runtime_client/contract_metadata.py" if fault == "client" else "runtime.lock.json")
        path.write_text("# staged drift\n")
    elif fault == "receipt":
        _damage(private["child"] / ".provision-report", "wrong receipt")
    else:
        selected = selected.replace(str(private["child"] / "bin/python") + " -I", SOURCE["maker_python"] + " -I")
    result = _run(selected, snapshot)
    assert result.returncode != 0
    assert reason in result.stderr, result.stdout + result.stderr
    assert "PRIVATE_DIAGNOSTIC=" not in result.stdout


def test_registry_drift_refused_without_backup(monkeypatch, private):
    tests = private["tests"]
    baseline = (tests / "suites.conf").read_bytes()
    drift = baseline + b"# concurrent change\n"
    (tests / "suites.conf").write_bytes(drift)
    with pytest.raises(AssertionError, match="registry drift"):
        _install(monkeypatch, private, baseline)
    assert (tests / "suites.conf").read_bytes() == drift
    assert not list(tests.parent.glob("suites-*.conf"))


@pytest.mark.parametrize("concurrent", [False, True])
def test_atomic_rollback_preserves_concurrent_bytes(monkeypatch, private, concurrent):
    tests, store = private["tests"], private["store"]
    before = (tests / "suites.conf").read_bytes()
    real_replace = os.replace
    published = []

    def replace(source, target):
        if Path(target) == tests / "suites.conf" and not published:
            with (store.root / "mutex").open("r+") as mutex, pytest.raises(BlockingIOError):
                fcntl.flock(mutex, fcntl.LOCK_EX | fcntl.LOCK_NB)
            real_replace(source, target)
            published.append(Path(target).read_bytes())
            (tests / (SOURCE["remotion_registration"] + ".env")).write_text("drift\n")
            if concurrent:
                Path(target).write_bytes(published[0] + b"# concurrent writer\n")
        else:
            real_replace(source, target)

    monkeypatch.setattr(os, "replace", replace)
    with pytest.raises((AssertionError, RuntimeError), match="atomic replacement differs" if concurrent else "registration env changed"):
        _install(monkeypatch, private)
    assert (tests / "suites.conf").read_bytes() == (published[0] + b"# concurrent writer\n" if concurrent else before)


def test_production_lease_refuses_selection_drift(monkeypatch, private):
    _install(monkeypatch, private)
    store, tests = private["store"], private["tests"]
    selected = _selected(tests)
    original = store.acquire

    @contextmanager
    def acquire(names):
        with original(names) as entries:
            rows = (tests / "suites.conf").read_bytes().splitlines(keepends=True)
            position = next(i for i, row in enumerate(rows) if row.split(None, 2)[:2] == [b"agent", b"full-farm"])
            rows[position] = b"agent full-farm /bin/false\n"
            (tests / "suites.conf").write_bytes(b"".join(rows))
            yield entries

    monkeypatch.setattr(store, "acquire", acquire)
    with pytest.raises(ValueError, match="changed during lease acquisition"), _suite_lease()(store, "agent", "full-farm", selected, tests):
        pytest.fail("child must not start")


@pytest.mark.parametrize(("fault", "reason"), [
    ("source_sha", "source receipt SHA mismatch"),
    ("source_tree", "source receipt tree mismatch"),
    ("dirty", "source checkout dirty"),
    ("source_url", "source root escapes retained work root"),
    ("record_path", "unsafe or duplicate.*RECORD path"),
    ("report_metadata", "provision report provenance mismatch"),
    ("remotion_tuple", "Remotion registered identity mismatch"),
    ("graph_lock", "Remotion lock drift"),
    ("full_row", "original agent full changed"),
    ("duplicate_row", "exactly one existing full-farm row required"),
    ("missing_child", "registration absent"),
])
def test_additional_installer_boundaries(monkeypatch, private, fault, reason):
    tests, child, store = private["tests"], private["child"], private["store"]
    output = subprocess.check_output
    if fault in ("source_sha", "source_tree", "dirty"):
        def wrong_source(argv, **kwargs):
            if argv[0] == "git" and argv[2] == str(private["agent"]):
                if (fault == "source_sha" and argv[-1] == "HEAD") or (fault == "source_tree" and argv[-1] == "HEAD^{tree}"):
                    return "0" * 40 + "\n"
                if fault == "dirty" and argv[3] == "status":
                    return " M file\n"
            return output(argv, **kwargs)
        monkeypatch.setattr(subprocess, "check_output", wrong_source)
    elif fault == "source_url":
        path = child / "lib/python3.13/site-packages/astrid-0.1.0.dist-info/direct_url.json"
        value = json.loads(path.read_text())
        value["url"] = "file:///outside/agent"
        _damage(path, json.dumps(value))
    elif fault == "record_path":
        path = child / "lib/python3.13/site-packages/astrid-0.1.0.dist-info/RECORD"
        _damage(path, path.read_text() + "../../../../../../outside,,\n")
    elif fault == "report_metadata":
        path = child / ".astrid-distribution-metadata"
        _damage(path, path.read_text().replace("_version=0.1.0", "_version=wrong"))
    elif fault == "remotion_tuple":
        selection = private["selection"]
        selection["remotion_tree"] = "0" * 40
        (private["packet"] / "runtime-source-selection.json").write_text(json.dumps(selection))
    elif fault == "graph_lock":
        (private["profile"] / "package-lock.json").write_text("wrong")
    elif fault in ("full_row", "duplicate_row"):
        value = (tests / "suites.conf").read_bytes()
        (tests / "suites.conf").write_bytes(value.replace(FULL, b"agent full /bin/true\n") if fault == "full_row" else value + OLD)
    else:
        index = json.loads((store.root / "index.json").read_text())
        del index["registrations"][SOURCE["child_name"]]
        (store.root / "index.json").write_text(json.dumps(index))
    before = (tests / "suites.conf").read_bytes()
    with pytest.raises((AssertionError, RuntimeError, SystemExit), match=reason):
        _install(monkeypatch, private)
    assert (tests / "suites.conf").read_bytes() == before
    assert not list(tests.parent.glob("suites-*.conf"))
