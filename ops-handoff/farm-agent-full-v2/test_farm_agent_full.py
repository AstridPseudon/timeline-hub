from __future__ import annotations

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
ORCH = Path(os.environ.get(
    "FARM_ORCH_ROOT",
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch",
))
BENCH_SOURCE = ORCH / "bin/bench_store.py"
SOURCE = json.loads((PACKET / "runtime-source-selection.json").read_bytes())
NODE_BIN = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin"
SCHEMA = "/home/user/work/venv-agent/lib/python3.13/site-packages"
PYTHON = "/home/user/work/venv-agent/bin/python"
NAME = "agent-remotion-farm-v2-9cd"
FULL = b"agent       full              /home/user/work/venv-agent/bin/python -m pytest -q -n 3\n"
OLD = b"agent full-farm env OLD_PROFILE=/stale /bin/false\n"
BODY = 'raise SystemExit(pytest.main(["-q","-n","3"]))'


def _api():
    # The installed module and its cache are read-only inputs.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("fixture_store", BENCH_SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def sources(tmp_path_factory):
    # Exact read-only Git objects, exported as private source fixtures. No Git
    # checkout, shared dependency mutation, or source stand-ins.
    base = tmp_path_factory.mktemp("farm-source")
    for name, repo, commit, paths in (
        ("agent", "/home/user/work/agent", SOURCE["agent_commit_tested_by_checkpoint"],
         ["astrid", "astrid_runtime_client", "runtime.lock.json", "pyproject.toml"]),
        ("runtime", str(PACKET.parents[1]), SOURCE["required_runtime_source_commit"],
         ["runtime_protocol"]),
    ):
        archive = subprocess.check_output(["git", "-C", repo, "archive", commit, *paths])
        target = base / name
        target.mkdir()
        with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
            stream.extractall(target, filter="data")
    return base / "agent", base / "runtime"


@pytest.fixture
def existing(tmp_path):
    api = _api()
    tests = tmp_path / "orch/tests"
    tests.mkdir(parents=True)
    # Include non-row bytes and CRLF outside the replacement boundary.
    (tests / "suites.conf").write_bytes(b"# existing registry\r\n#" + OLD + FULL + OLD + b"agent outside /bin/true\n")
    (tests.parent / "bin").mkdir()
    (tests.parent / "bin/bench_store.py").symlink_to(BENCH_SOURCE)
    store = api.Store.initialize(tmp_path / "bench-store", tests)
    borrowed = Path("/home/user/work/runtimes/agent-remotion/node_modules").resolve(strict=True)

    def build(stage, _final):
        # Historical peers are only read for the bounded Node import diagnostic;
        # this fixture does not authenticate a current Farm graph or receipt.
        (stage / "package.json").write_text('{"private":true}\n')
        (stage / "node_modules").symlink_to(borrowed, target_is_directory=True)

    entry = store.ensure(
        "runtime", {"remotion_tree": "b01dca9b3b24f54093c20b7c5657316f997725db"},
        {"name": NAME, "env": "ASTRID_REMOTION_PROJECT_DIR={bench_path}\n",
         "suite": "agent fixture-managed /bin/true\n"},
        build, lambda path: None,
    )
    # The installer must OPEN this existing Store; it must not initialize one.
    return api.Store(store.root, tests), Path(entry["path"]), tests


def _install(monkeypatch, existing, runtime, baseline=None):
    store, profile, tests = existing
    snapshot = tests.parent / "pre-full-farm.suites.conf"
    snapshot.write_bytes(baseline if baseline is not None else (tests / "suites.conf").read_bytes())
    text = (PACKET / "FARM-CODEX-BRIEF.md").read_text()
    code = text.split("<<'PY'\n", 1)[1].split("\nPY\n", 1)[0]
    script = tests.parent / "installer-fixture.py"
    script.write_text(code)
    spec = importlib.util.spec_from_file_location("installer_fixture", script)
    module = importlib.util.module_from_spec(spec)
    argv = ["-", str(tests.parent), str(store.root), str(PACKET), str(profile),
            str(runtime), str(snapshot), str(tests.parent)]
    with monkeypatch.context() as patch:
        patch.setattr(sys, "argv", argv)
        spec.loader.exec_module(module)
    return (tests / "suites.conf").read_bytes()


def _selected(tests):
    # Execute production's EXACT awk extraction, including its whitespace rebuild.
    line = (ORCH / "bin/test-run").read_text().splitlines()[14]
    extraction = line.split("); [ -n", 1)[0] + ")"
    return subprocess.check_output(
        ["bash", "-c", extraction + '\nprintf "%s" "$CMD"'],
        env={"PATH": "/usr/bin:/bin", "O": str(tests.parent), "repo": "agent", "suite": "full-farm"},
        text=True,
    )


def _suite_lease(tests):
    # Only the installed context manager, never the dispatcher, snapshot body,
    # supervisor or full-suite service. Its Store calls remain production calls.
    source = (ORCH / "bin/test-run").read_text()
    code = source.split("@contextmanager\ndef suite_lease", 1)[1].split("\n\ndef supervise", 1)[0]
    script = tests.parent / "lease-fixture.py"
    script.write_text("from contextlib import contextmanager\nfrom pathlib import Path\n"
                      "@contextmanager\ndef suite_lease" + code)
    spec = importlib.util.spec_from_file_location("lease_fixture", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.suite_lease


def _run(command, agent, body, fds=()):
    assert command.count(BODY) == 1
    # Replace ONLY pytest's body. Every real environment, version, peer, import,
    # source hash and origin check in the rendered recipe still executes.
    prefix, payload = command.rsplit(" -c ", 1)
    code, = shlex.split(payload)
    command = prefix + " -c " + shlex.quote(code.replace(BODY, body))
    return subprocess.run(
        ["bash", "-c", command], cwd=agent,
        env={"PATH": "/usr/bin:/bin", "ASTRID_RUNTIME_CHECKOUT": "/ambient-wrong",
             "PYTHONPATH": "/ambient-wrong", "PYTHONNOUSERSITE": "1"},
        pass_fds=fds, text=True, capture_output=True, timeout=60, check=False,
    )


def test_packet_source_and_candidate_row_are_explicit():
    assert hashlib.sha256(BENCH_SOURCE.read_bytes()).hexdigest() == "6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8"
    assert SOURCE["declared_runtime_source_commit"].startswith("45c3a7f4")
    assert SOURCE["required_runtime_source_commit"].startswith("1d9ddba5")
    assert SOURCE["status"].startswith("source checkout")
    row = (PACKET / "registration-row.txt").read_text()
    assert row.count("\n") == 1 and row.endswith("\n")
    assert "ASTRID_TEST_NODE_MODULES=@MANAGED_PROFILE@/node_modules" in row
    assert "FARM_RECEIPT_MANAGED_PROFILE" not in row
    assert BODY in row and "env -i " in row
    assert "v20.19.4" in row and "10.8.2" in row


def test_candidate_template_holds_without_managed_receipt(tmp_path):
    command = (PACKET / "registration-row.txt").read_text().split(None, 2)[2].strip()
    result = subprocess.run(["bash", "-c", command], cwd=tmp_path,
                            text=True, capture_output=True, timeout=60, check=False)
    assert result.returncode != 0
    assert "PROFILE_PEERS_OK" not in result.stdout


def test_existing_store_replaces_one_full_farm_row_and_runs_selected_recipe(
    monkeypatch, existing, sources,
):
    store, profile, tests = existing
    agent, runtime = sources
    before = (tests / "suites.conf").read_bytes()
    metadata = [(store.root / p).read_bytes() for p in ("owner.json", "index.json")]
    post = _install(monkeypatch, existing, runtime)
    candidate = [r for r in post.splitlines(keepends=True) if r.split(None, 2)[:2] == [b"agent", b"full-farm"]]
    assert len(candidate) == 1
    assert b"@MANAGED_PROFILE@" not in candidate[0] and b"@RUNTIME_CHECKOUT@" not in candidate[0]
    assert post == b"".join(candidate[0] if r == OLD else r for r in before.splitlines(keepends=True))
    assert FULL in post
    assert [(store.root / p).read_bytes() for p in ("owner.json", "index.json")] == metadata
    backups = list(tests.parent.glob("suites-*.conf"))
    assert len(backups) == 1 and backups[0].read_bytes() == before
    assert re.fullmatch(r"suites-\d{8}T\d{6}\.\d{6}Z.conf", backups[0].name)
    selected = _selected(tests)
    raw = candidate[0].decode().split(None, 2)[2].rstrip("\n")
    assert selected == " ".join(raw.split())
    assert store.names_for_suite("agent", "full-farm", raw) == [NAME]
    with _suite_lease(tests)(store, "agent", "full-farm", selected, tests) as (entries, fds):
        assert len(entries) == len(fds) == 1
        assert entries[0]["path"] == str(profile)
        # Both the diagnostic Python and its own child inherit the acquired fd.
        child = (
            "import json,os,pathlib,runtime_protocol.external_pack_sources as p,astrid; "
            f"[os.fstat(fd) for fd in {fds!r}]; "
            "print(json.dumps(dict(env=dict(os.environ),runtime=p.__file__,agent=astrid.__file__)))"
        )
        body = f'print("CHILD="+subprocess.check_output([sys.executable,"-c",{child!r}],text=True,pass_fds={tuple(fds)!r}).strip())'
        result = _run(selected, agent, body, tuple(fds))
        assert result.returncode == 0, result.stdout + result.stderr
        observed = json.loads(result.stdout.split("CHILD=", 1)[1])
        env = observed["env"]
        expected = {
            "PATH": f"{NODE_BIN}:/home/user/work/venv-agent/bin:/usr/bin:/bin",
            "ASTRID_REMOTION_PROJECT_DIR": str(profile),
            "ASTRID_TEST_NODE_MODULES": str(profile / "node_modules"),
            "ASTRID_NODE_EXECUTABLE": NODE_BIN + "/node",
            "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": SCHEMA,
            "ASTRID_RUNTIME_CHECKOUT": str(runtime), "PYTHONPATH": f"{agent}:{runtime}",
            "HOME": "/root", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        assert all(env.get(k) == v for k, v in expected.items())
        assert "PYTHONNOUSERSITE" not in env
        assert observed["runtime"] == str(runtime / "runtime_protocol/external_pack_sources.py")
        assert observed["agent"] == str(agent / "astrid/__init__.py")
        lock = store.root / "locks" / (entries[0]["component"] + "-" + entries[0]["key"])
        with lock.open("r+") as stream, pytest.raises(BlockingIOError):
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
    for fd in fds:
        with pytest.raises(OSError) as error:
            os.fstat(fd)
        assert error.value.errno == errno.EBADF
    with lock.open("r+") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)


def test_projection_refuses_wrong_source_without_store_mutation(monkeypatch, existing, tmp_path):
    _store, _profile, tests = existing
    wrong = tmp_path / "wrong-runtime/runtime_protocol"
    wrong.mkdir(parents=True)
    (wrong / "external_pack_sources.py").write_text("# wrong source\n")
    baseline = (tests / "suites.conf").read_bytes()
    with pytest.raises(AssertionError, match="Runtime D40 source mismatch"):
        _install(monkeypatch, existing, wrong.parent)
    assert (tests / "suites.conf").read_bytes() == baseline
    assert not list(tests.parent.glob("suites-*.conf"))


def test_existing_store_replacement_refuses_registry_drift(monkeypatch, existing, sources):
    _store, _profile, tests = existing
    baseline = (tests / "suites.conf").read_bytes()
    drift = baseline + b"agent concurrent /bin/true\n"
    (tests / "suites.conf").write_bytes(drift)
    with pytest.raises(AssertionError, match="registry drift"):
        _install(monkeypatch, existing, sources[1], baseline)
    assert (tests / "suites.conf").read_bytes() == drift
    assert not list(tests.parent.glob("suites-*.conf"))


@pytest.mark.parametrize("concurrent", [False, True])
def test_existing_store_replacement_rolls_back_on_post_update_refusal(
    monkeypatch, existing, sources, concurrent,
):
    store, _profile, tests = existing
    before = (tests / "suites.conf").read_bytes()
    real_replace = os.replace
    published = []

    def replace(source, target):
        if Path(target) == tests / "suites.conf" and not published:
            # Observe the real atomic publication under the real mutex.
            with (store.root / "mutex").open("r+") as mutex, pytest.raises(BlockingIOError):
                fcntl.flock(mutex, fcntl.LOCK_EX | fcntl.LOCK_NB)
            real_replace(source, target)
            published.append(Path(target).read_bytes())
            (tests / (NAME + ".env")).write_text("drift\n")
            if concurrent:
                Path(target).write_bytes(published[0] + b"# concurrent writer\n")
        else:
            real_replace(source, target)

    monkeypatch.setattr(os, "replace", replace)
    with pytest.raises((RuntimeError, AssertionError), match=(
        "atomic replacement differs" if concurrent else "registration env changed"
    )):
        _install(monkeypatch, existing, sources[1])
    assert (tests / "suites.conf").read_bytes() == (
        published[0] + b"# concurrent writer\n" if concurrent else before
    )


@pytest.mark.parametrize("fault", ["node", "npm", "peer", "source", "client", "lock"])
def test_preflight_refuses_before_body(monkeypatch, existing, sources, tmp_path, fault):
    agent, runtime = sources
    _install(monkeypatch, existing, runtime)
    _store, _profile, tests = existing
    command = _selected(tests)
    if fault in ("node", "npm"):
        tools = tmp_path / "tools"
        tools.mkdir()
        for name, version in (("node", "v22.22.0" if fault == "node" else "v20.19.4"),
                              ("npm", "9.0.0" if fault == "npm" else "10.8.2")):
            tool = tools / name
            tool.write_text(f"#!/bin/sh\nprintf '%s\\n' '{version}'\n")
            tool.chmod(0o700)
        command = command.replace(NODE_BIN, str(tools))
    elif fault == "peer":
        # Rebind the whole profile to a private empty graph, never alter a
        # borrowed installation, even through a private symlink.
        empty = tmp_path / "empty-profile"
        (empty / "node_modules").mkdir(parents=True)
        (empty / "package.json").write_text("{}")
        command = command.replace(str(existing[1]), str(empty))
    else:
        # Only private exported source fixtures; other cases reuse pristine
        # session sources, so create a shallow private file overlay for damage.
        import shutil
        if fault == "source":
            target = tmp_path / "bad-runtime"
            shutil.copytree(runtime, target)
            (target / "runtime_protocol/external_pack_sources.py").write_text("# wrong source\n")
            command = command.replace(str(runtime), str(target))
        else:
            target = tmp_path / "bad-agent"
            shutil.copytree(agent, target)
            leaf = "astrid_runtime_client/contract_metadata.py" if fault == "client" else "runtime.lock.json"
            with (target / leaf).open("a") as stream:
                stream.write("\n# drift\n")
            agent = target
    result = _run(command, agent, 'print("BODY_MUST_NOT_RUN")')
    assert result.returncode != 0, result.stdout + result.stderr
    assert "BODY_MUST_NOT_RUN" not in result.stdout
    reason = {"node": "Node version mismatch", "npm": "npm version mismatch",
              "peer": "missing profile peer", "source": "D40 source mismatch",
              "client": "canonical client drift", "lock": "declared Runtime lock drift"}[fault]
    assert ("Error: missing profile peer:" if fault == "peer" else "AssertionError: " + reason) in result.stderr, result.stdout + result.stderr


def test_lease_refuses_selection_drift(monkeypatch, existing, sources):
    store, _profile, tests = existing
    _install(monkeypatch, existing, sources[1])
    selected = _selected(tests)
    original = store.acquire

    @contextmanager
    def acquire(names):
        with original(names) as entries:
            # A real registry edit after acquisition must refuse the child.
            registry = tests / "suites.conf"
            rows = registry.read_bytes().splitlines(keepends=True)
            index = next(i for i, row in enumerate(rows)
                         if row.split(None, 2)[:2] == [b"agent", b"full-farm"])
            rows[index] = b"agent full-farm /bin/false\n"
            registry.write_bytes(b"".join(rows))
            yield entries

    monkeypatch.setattr(store, "acquire", acquire)
    with (
        pytest.raises(ValueError, match="changed during lease acquisition"),
        _suite_lease(tests)(store, "agent", "full-farm", selected, tests),
    ):
        pytest.fail("diagnostic child must not start")
