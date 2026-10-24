"""Pure join/refusal controls. Synthetic Git fixtures prove no actual schema build."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import io
import json
import os
import shlex
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest
import test_dependency_reuse as reuse
import test_farm_distribution_inputs as inputs

CANDIDATE = Path(__file__).parents[1] / "candidate"


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, CANDIDATE / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def helper():
    return load("join_seed", "verify_dependency_seed.py")


@pytest.fixture
def joined(tmp_path: Path, monkeypatch, helper):
    # The production Git backend is never replaced outside these unit fixtures.
    # This cannot authenticate SCHEMA_COMMIT or qualify a real schema child.
    source = inputs.private_schema_fixture(tmp_path)
    monkeypatch.setattr(inputs.component, "_git", inputs.fake_schema_git(source))
    monkeypatch.setattr(helper, "farm_component", lambda: inputs.component)
    archive = io.BytesIO()
    prefix = source / inputs.SCHEMA_SUBDIRECTORY
    with tarfile.open(fileobj=archive, mode="w") as stream:
        for path in sorted(prefix.rglob("*")):
            if path.is_file():
                data = path.read_bytes()
                entry = tarfile.TarInfo(path.relative_to(prefix).as_posix())
                entry.size, entry.mode = len(data), 0o644
                stream.addfile(entry, io.BytesIO(data))
    original = archive.getvalue()
    monkeypatch.setattr(helper.subprocess, "check_output", lambda *a, **kw: original)
    root = tmp_path / "child"
    root.mkdir()
    (root / ".source-inputs").mkdir()
    (root / ".child-venv-source-unit").mkdir()
    (root / ".bootstrap-input.tgz").write_bytes(reuse.BOOTSTRAP_ARCHIVE.read_bytes())
    receipt = helper.farm_inputs(source, root / ".bootstrap-input.tgz")
    helper.prepare_farm(root, source, receipt["component_identity"])
    yield helper, root, source, receipt, original
    # Pytest can remove private sealed fixtures normally, without shared writes.
    for path in [root, *root.rglob("*")]:
        if not path.is_symlink() and path.is_dir():
            path.chmod(path.stat().st_mode | 0o700)


def test_exact_reviewed_component_blobs():
    for filename, blob in (
        (CANDIDATE / "verify_farm_distribution_inputs.py", "0558a58a28496607cfbe668484ed37815442b8da"),
        (Path(__file__).with_name("test_farm_distribution_inputs.py"), "ee1bb8cb6ed56ca44bef195dff54e7bccbdefb1c"),
    ):
        data = filename.read_bytes()
        assert hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == blob


def test_authentic_component_refuses_missing_or_current_source(helper, tmp_path):
    for source in (tmp_path / "absent", Path("/home/user/work/agent")):
        with pytest.raises(ValueError, match="schema source"):
            helper.farm_inputs(source, reuse.BOOTSTRAP_ARCHIVE)


def test_component_pin_refuses_replaced_module(helper, monkeypatch):
    monkeypatch.setattr(helper, "FARM_COMPONENT_SHA256", "0" * 64)
    with pytest.raises(SystemExit, match="untrusted Farm"):
        helper.farm_component()


def test_retains_separate_original_archive_test_role_and_receipt(joined):
    helper, root, source, receipt, original = joined
    actual, wheels, owned = helper.retained_farm(root, receipt["component_identity"])
    assert actual == receipt
    assert (root / ".source-inputs/schema.tar").read_bytes() == original
    assert set(wheels) == {"pytest_xdist-3.8.0-py3-none-any.whl", "execnet-2.1.2-py3-none-any.whl"}
    assert ".farm-receipt.json" in owned and ".source-inputs/schema.tar" in owned
    assert not any(".bootstrap-wheelhouse" in name or ".dependency-wheelhouse" in name for name in owned)
    assert b"pip==" not in (root / ".farm-test-wheelhouse/requirements.txt").read_bytes()
    assert source == Path(actual["schema_source"]["custody"]["root"])


@pytest.mark.parametrize("field", ["commit", "tree", "package", "version", "subdirectory", "files", "content_sha256", "custody"])
def test_claimed_source_receipt_cannot_grant_authority(joined, field):
    helper, root, _, receipt, _ = joined
    forged = copy.deepcopy(receipt)
    if field == "custody":
        forged["schema_source"][field]["uid"] += 1
    elif field == "files":
        forged["schema_source"][field][0]["blob"] = "0" * 40
    else:
        forged["schema_source"][field] = "forged"
    (root / ".farm-receipt.json").chmod(0o600)
    (root / ".farm-receipt.json").write_text(json.dumps(forged))
    with pytest.raises(SystemExit, match="Farm receipt/source authority"):
        helper.retained_farm(root, receipt["component_identity"])


@pytest.mark.parametrize("case", ["key", "role", "lock", "wheel", "archive", "extra", "symlink", "hardlink", "source"])
def test_changed_retained_inputs_fail_closed(joined, case):
    helper, root, source, receipt, _ = joined
    authority = receipt["component_identity"]
    if case == "key":
        authority = "0" * 64
    elif case == "source":
        (source / inputs.SCHEMA_SUBDIRECTORY / "banodoco_timeline_schema/__init__.py").write_text("changed = True\n")
    elif case == "role":
        forged = copy.deepcopy(receipt)
        forged["wheel_inputs"]["distributions"][0]["role"] = "bootstrap3"
        (root / ".farm-receipt.json").chmod(0o600)
        (root / ".farm-receipt.json").write_text(json.dumps(forged))
    elif case == "extra":
        seed = root / ".farm-test-wheelhouse"
        seed.chmod(0o700)
        (seed / "foreign.whl").write_bytes(b"extra")
    else:
        path = root / (".source-inputs/schema.tar" if case == "archive" else ".farm-test-wheelhouse/requirements.txt" if case == "lock" else ".farm-test-wheelhouse/execnet-2.1.2-py3-none-any.whl")
        path.parent.chmod(0o700)
        if case == "symlink":
            other = root / "external"
            path.rename(other)
            path.symlink_to(other)
        elif case == "hardlink":
            os.link(path, root / "second-link")
        else:
            path.chmod(0o600)
            path.write_bytes(b"changed")
    with pytest.raises((SystemExit, ValueError, OSError)):
        helper.retained_farm(root, authority)


@pytest.mark.parametrize("case", ["changed", "extra", "missing", "traversal", "link", "mode", "duplicate"])
def test_original_schema_archive_must_match_exact_authenticated_blobs(joined, monkeypatch, case):
    helper, _, _, receipt, original = joined
    archive = io.BytesIO()
    with tarfile.open(fileobj=io.BytesIO(original)) as source, tarfile.open(fileobj=archive, mode="w") as target:
        entries = list(source)
        for index, entry in enumerate(entries):
            if case == "missing" and index == 0:
                continue
            data = source.extractfile(entry).read()
            if index == 0:
                if case == "changed":
                    data = b"changed"
                    entry.size = len(data)
                elif case == "traversal":
                    entry.name = "../escaped"
                elif case == "link":
                    entry.type = tarfile.SYMTYPE
                    entry.linkname = "outside"
                elif case == "mode":
                    entry.mode = 0o777
            target.addfile(entry, io.BytesIO(data))
            if case == "duplicate" and index == 0:
                target.addfile(entry, io.BytesIO(data))
        if case == "extra":
            entry = tarfile.TarInfo("unowned.py")
            entry.size = 1
            target.addfile(entry, io.BytesIO(b"x"))
    monkeypatch.setattr(helper.subprocess, "check_output", lambda *a, **kw: archive.getvalue())
    with pytest.raises(SystemExit, match="schema Git archive"):
        helper.schema_archive(receipt)


def test_store_key_binds_farm_alongside_bootstrap_and_refuses_legacy_identity():
    store = load("join_store", "bench_store.py")
    identity = {"agent_sha": "a" * 40, "backend_sha": "b" * 40, "client_tuple": {"client": "c"}, "bootstrap_authority": "d" * 64}
    old = store.key_for("child", identity)
    bound = store.key_for("child", {**identity, "farm_authority": "e" * 64})
    assert old != bound
    assert bound != store.key_for("child", {**identity, "farm_authority": "f" * 64})
    for value in (None, "wrong", "a" * 63):
        with pytest.raises(store.Refused):
            store.key_for("child", {**identity, "farm_authority": value})
    with pytest.raises(store.Refused):
        store.key_for("child", {key: value for key, value in {**identity, "farm_authority": "e" * 64}.items() if key != "bootstrap_authority"})


@pytest.mark.parametrize("caller", ["request-child-venv", "make-child-venv"])
@pytest.mark.parametrize("args", [[], ["--farm-schema-source", "/does-not-exist"], ["--farm-schema-source", "/tmp/../tmp"], ["--farm-schema-source", "relative"], ["--farm-schema-source"]])
def test_farm_missing_or_unsafe_source_refuses_before_installer_or_queue(tmp_path, caller, args):
    env = {**os.environ, "CHILD_VENV_ORCH_ROOT": str(tmp_path / "orch"), "CHILD_VENV_WORK_ROOT": str(tmp_path), "CHILD_VENV_FARM_SCHEMA_SOURCE": ""}
    result = subprocess.run([str(CANDIDATE / caller), "venv-agent-child-farm-unit", "a" * 40, "--farm-distributions", *args], env=env, capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert "REFUSED:" in result.stderr
    assert not (tmp_path / "orch").exists()


def test_request_serializes_explicit_private_source_carrier(tmp_path):
    orch = tmp_path / "orch"
    (orch / "queue/pending").mkdir(parents=True)
    work = tmp_path / "work"
    work.mkdir()
    source, wheels = tmp_path / "source", tmp_path / "wheels"
    source.mkdir()
    wheels.mkdir()
    agent, runtime = tmp_path / "agent", tmp_path / "runtime"
    a = reuse.git_repo(agent, {"pyproject.toml": b"[project]\nname='astrid'\n"})
    r = reuse.git_repo(runtime, {"packages/python/astrid_runtime_client/client.py": b"CLIENT=True\n"})
    env = {**os.environ, "CHILD_VENV_ORCH_ROOT": str(orch), "CHILD_VENV_WORK_ROOT": str(work), "CHILD_VENV_DEPENDENCY_WHEELHOUSE": str(wheels), "CHILD_VENV_FARM_SCHEMA_SOURCE": str(source)}
    result = subprocess.run([str(CANDIDATE / "request-child-venv"), "venv-agent-child-farm-unit", a, "--source-carrier", str(agent), str(runtime), r], env=env, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    args = shlex.split((orch / "queue/pending/childvenv-venv-agent-child-farm-unit").read_text())
    assert args[args.index("--farm-schema-source") + 1] == str(source)
    assert args[args.index("--dependency-wheelhouse") + 1] == str(wheels)


def test_production_path_traces_gate_create_staging_final_and_reuse():
    maker = (CANDIDATE / "make-child-venv").read_text()
    store_body = maker.split("<<'STORE_PY'\n", 1)[1].split("\nSTORE_PY", 1)[0]
    assert store_body.index("seed.farm_inputs(") < store_body.index("store = module.Store(") < store_body.index("store.ensure(")
    assert "seed_module().retained_farm(retained, identity['farm_authority'])" in store_body
    assert "module.retained_farm(pathlib.Path(root), farm_authority)" in maker
    assert maker.index("run_stage retain-farm-inputs") < maker.index("run_stage install-farm-schema")
    assert maker.index("run_stage verify-staging-inventory") < maker.index("run_stage shebang-relocation")
    assert "checkouts['banodoco-timeline-schema']" in maker
    assert "modules.issubset(rows)" in maker and "unowned local distribution RECORD addition" in maker
    assert '"astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client"' in maker


def test_real_normal_gate_refuses_wrong_source_before_store_or_installer(tmp_path):
    """Run the production caller with real reviewed inputs and wrong Git source."""
    maker = CANDIDATE / "make-child-venv"
    body = maker.read_text().split("<<'STORE_PY'\n", 1)[1].split("\nSTORE_PY", 1)[0]
    fake_store = tmp_path / "bench_store.py"
    fake_store.write_text("class Store:\n    def __init__(self, *args):\n        raise AssertionError('STORE_CONSTRUCTED_BEFORE_GATE')\n")
    args = [str(maker), str(fake_store), str(tmp_path / "store"), str(tmp_path),
            "venv-agent-child-farm-unit", "a" * 40, "b" * 40, "client=c",
            "/home/user/work/agent", str(tmp_path), str(tmp_path), sys.executable,
            "", "", "requirements/proof.lock", "c" * 64, str(tmp_path),
            hashlib.sha256((CANDIDATE / "verify_dependency_seed.py").read_bytes()).hexdigest(),
            "236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778",
            "/home/user/work/agent", "1", str(reuse.BOOTSTRAP_ARCHIVE)]
    result = subprocess.run([sys.executable, "-I", "-c", body, *args],
                            env={**os.environ, "STORE_CONTEXT": ""}, capture_output=True, text=True, check=False)
    assert result.returncode != 0
    assert "selected Agent commit" in result.stderr, result.stderr
    assert "STORE_CONSTRUCTED_BEFORE_GATE" not in result.stderr
    assert not (tmp_path / "store").exists()


def test_forged_test_lock_never_invokes_installer(joined, monkeypatch):
    helper, root, _, _, _ = joined
    requirements = root / ".farm-test-wheelhouse/requirements.txt"
    requirements.chmod(0o600)
    requirements.write_bytes(requirements.read_bytes() + b"# forged role lock\n")
    monkeypatch.setattr(helper, "install_snapshot", lambda *a, **kw: pytest.fail("installer invoked on forged Farm inputs"))
    monkeypatch.setattr(sys, "argv", [str(CANDIDATE / "verify_dependency_seed.py"), str(requirements.parent), str(requirements), "--install", "--no-deps"])
    with pytest.raises(SystemExit, match="retained Farm test2"):
        helper.main()


@pytest.mark.parametrize("case", ["unsafe-directory", "foreign-owner", "changed-descriptor"])
def test_retained_farm_custody_checks_real_metadata_and_revalidation(joined, monkeypatch, case):
    helper, root, _, _, _ = joined
    if case == "unsafe-directory":
        root.chmod(0o777)
    elif case == "foreign-owner":
        original = inputs.component.os.getuid
        monkeypatch.setattr(inputs.component.os, "getuid", lambda: original() + 1000)
    else:
        original = helper.schema_archive

        def change(receipt):
            result = original(receipt)
            marker = root / ".farm-receipt.json"
            marker.chmod(0o600)
            marker.write_bytes(marker.read_bytes())
            return result

        monkeypatch.setattr(helper, "schema_archive", change)
    with pytest.raises((ValueError, SystemExit), match="schema source|Farm"):
        helper.retained_farm(root)


@pytest.mark.parametrize("mutation", ["valid", "wrong-version", "source-bytes", "record-extra", "direct-url", "retained-source", "missing-module"])
def test_schema_source_inventory_uses_exact_archived_files_not_record_claims(tmp_path, monkeypatch, mutation):
    """Synthetic internal ownership seam only; no authentic schema or build proof."""
    import contextlib

    env, args, _ = reuse.retained_fixture(tmp_path, managed=False, source_archive=True)
    root = Path(env["CHILD_VENV_WORK_ROOT"]) / args[0]
    for path in [root, *root.rglob("*")]:
        path.chmod(path.stat().st_mode | (0o700 if path.is_dir() else 0o200))
    source_files = {
        "pyproject.toml": b'[project]\nname="banodoco-timeline-schema"\nversion="0.0.2"\n[tool.setuptools.packages.find]\ninclude=["banodoco_timeline_schema*"]\n',
        "banodoco_timeline_schema/__init__.py": b"SCHEMA = True\n",
    }
    archived = io.BytesIO()
    with tarfile.open(fileobj=archived, mode="w") as archive:
        for name, content in source_files.items():
            entry = tarfile.TarInfo(name)
            entry.size, entry.mode = len(content), 0o644
            archive.addfile(entry, io.BytesIO(content))
    archive_bytes = archived.getvalue()
    (root / ".source-inputs/schema.tar").write_bytes(archive_bytes)
    snapshot = root / ".child-venv-source-fixture/schema"
    for name, content in source_files.items():
        path = snapshot / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    site = root / "lib/python3.13/site-packages"
    metadata = "banodoco_timeline_schema-0.0.2.dist-info"
    url = (root / ".source-inputs/schema.tar").as_uri()
    installed = {
        "banodoco_timeline_schema/__init__.py": source_files["banodoco_timeline_schema/__init__.py"],
        metadata + "/METADATA": b"Name: banodoco-timeline-schema\nVersion: 0.0.2\n",
        metadata + "/direct_url.json": json.dumps({"url": url, "archive_info": {"hashes": {"sha256": hashlib.sha256(archive_bytes).hexdigest()}}}).encode(),
    }
    if mutation == "wrong-version":
        installed[metadata + "/METADATA"] = b"Name: banodoco-timeline-schema\nVersion: 9.9.9\n"
    elif mutation == "source-bytes":
        installed["banodoco_timeline_schema/__init__.py"] = b"FORGED=True\n"
    elif mutation == "record-extra":
        installed["banodoco_timeline_schema/extra.py"] = b"FORGED=True\n"
    elif mutation == "direct-url":
        installed[metadata + "/direct_url.json"] = b'{"url":"file:///wrong","dir_info":{}}'
    elif mutation == "retained-source":
        (snapshot / "banodoco_timeline_schema/__init__.py").write_bytes(b"changed")
    elif mutation == "missing-module":
        installed.pop("banodoco_timeline_schema/__init__.py")
    reuse.write_record(site, metadata, installed)
    origins = root / ".astrid-import-origins"
    origins.write_text(origins.read_text() + f"banodoco_timeline_schema={site}/banodoco_timeline_schema/__init__.py\n")
    metadata_path = root / ".astrid-distribution-metadata"
    metadata_path.write_text(metadata_path.read_text() + "banodoco-timeline-schema_name=banodoco-timeline-schema\nbanodoco-timeline-schema_version=0.0.2\n" + f"banodoco-timeline-schema_direct_url={url}\nbanodoco-timeline-schema_provenance=archive\n")
    report = root / ".provision-report"
    old = report.read_text()
    prefix = old.split("installed_import_origins:\n")[0]
    freeze = old.split("pip_freeze:\n")[1].splitlines()
    freeze.append(f"banodoco-timeline-schema @ {url}#sha256={hashlib.sha256(archive_bytes).hexdigest()}")
    report.write_text(prefix + "installed_import_origins:\n" + origins.read_text() + "installed_distribution_metadata:\n" + metadata_path.read_text() + "pip_freeze:\n" + "\n".join(sorted(freeze)) + "\n")
    for path in [root, *root.rglob("*")]:
        path.chmod(path.stat().st_mode & ~0o222)
    original = subprocess.check_output

    def archive(command, *a, **kw):
        if command[-1] == inputs.SCHEMA_COMMIT + ":" + inputs.SCHEMA_SUBDIRECTORY:
            return archive_bytes
        return original(command, *a, **kw)

    monkeypatch.setattr(subprocess, "check_output", archive)
    import runpy
    from importlib import metadata

    monkeypatch.setattr(metadata, "distributions", lambda path: [metadata.PathDistribution(p) for p in site.glob("*.dist-info")])
    monkeypatch.setattr(sys, "argv", ["verifier", str(root), (root / ".astrid-runtime-client-identity").read_text().rstrip("\n"), args[3], args[1], args[4], args[5], env["CHILD_VENV_WORK_ROOT"], env["CHILD_VENV_PYTHON"], "--farm-source", str(tmp_path / "synthetic-object-authority")])
    body = (CANDIDATE / "make-child-venv").read_text().split("# STORE_VERIFY_BEGIN\n", 1)[1].split("# STORE_VERIFY_END", 1)[0]
    verifier = tmp_path / "source-verifier.py"
    verifier.write_text(body)
    output = io.StringIO()
    if mutation == "valid":
        with contextlib.redirect_stdout(output):
            runpy.run_path(str(verifier), run_name="__main__")
        inventory = json.loads(output.getvalue())
        assert "banodoco_timeline_schema/__init__.py" in inventory[inputs.component.SCHEMA_PACKAGE]
        assert ".source-inputs/schema.tar" in inventory["__root__"]
    else:
        with pytest.raises(SystemExit):
            runpy.run_path(str(verifier), run_name="__main__")
    for path in [root, *root.rglob("*")]:
        if path.is_dir():
            path.chmod(path.stat().st_mode | 0o700)


def test_component_executes_exact_pinned_source_without_cached_code(tmp_path):
    import importlib._bootstrap_external as bootstrap_external
    import importlib.util

    component = tmp_path / "verify_farm_distribution_inputs.py"
    component.write_bytes((CANDIDATE / component.name).read_bytes())
    helper_path = tmp_path / "verify_dependency_seed.py"
    helper_path.write_bytes((CANDIDATE / helper_path.name).read_bytes())
    cached = Path(importlib.util.cache_from_source(str(component)))
    cached.parent.mkdir()
    code = compile("raise AssertionError('UNAUTHENTICATED_CACHE_EXECUTED')", str(component), "exec")
    cached.write_bytes(bootstrap_external._code_to_timestamp_pyc(code, int(component.stat().st_mtime), component.stat().st_size))
    helper = reuse.load_helper("join_private_component_loader", helper_path)
    assert helper.farm_component().SCHEMA_COMMIT == inputs.SCHEMA_COMMIT
