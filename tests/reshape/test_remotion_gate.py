"""Focused safety tests for the reproducible Remotion gate."""

from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path

import pytest

from scripts.reshape import remotion_gate as gate


def _fake_node_distribution(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "node"
    node = root / "bin" / "node"
    npm_cli = root / "lib" / "node_modules" / "npm" / "bin" / "npm-cli.js"
    node.parent.mkdir(parents=True)
    npm_cli.parent.mkdir(parents=True)
    node.write_text(
        "#!/bin/sh\n"
        "if [ \"$1\" = \"--version\" ]; then printf 'v20.19.4\\n'; "
        "else printf '10.8.2\\n'; fi\n",
        encoding="utf-8",
    )
    npm_cli.write_text("// fake npm cli\n", encoding="utf-8")
    node.chmod(0o755)
    return node, npm_cli


def test_toolchain_uses_node_distribution_npm_cli_not_path_fallback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_node = tmp_path / "bin" / "node"
    fake_node.parent.mkdir()
    fake_node.write_text("#!/bin/sh\nprintf 'v20.19.4\\n'\n", encoding="utf-8")
    fake_node.chmod(0o755)
    fake_npm = tmp_path / "bin" / "npm"
    fake_npm.write_text("#!/bin/sh\nprintf '10.8.2\\n'\n", encoding="utf-8")
    fake_npm.chmod(0o755)
    monkeypatch.setenv("PATH", str(fake_node.parent))
    monkeypatch.delenv("ASTRID_NODE_EXECUTABLE", raising=False)
    monkeypatch.delenv("ASTRID_NPM_EXECUTABLE", raising=False)

    with pytest.raises(RuntimeError, match="npm CLI"):
        gate._resolve_tools()


def test_arbitrary_npm_executable_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    node, _npm_cli = _fake_node_distribution(tmp_path)
    external_npm = tmp_path / "outside-npm-cli.js"
    external_npm.write_text("// hostile\n", encoding="utf-8")
    monkeypatch.setenv("ASTRID_NODE_EXECUTABLE", str(node))
    monkeypatch.setenv("ASTRID_NPM_EXECUTABLE", str(external_npm))

    with pytest.raises(RuntimeError, match="contained"):
        gate._resolve_tools()


def test_npm_invocation_is_node_plus_contained_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    node, npm_cli = _fake_node_distribution(tmp_path)
    remotion = tmp_path / "remotion"
    (remotion / "node_modules").mkdir(parents=True)
    monkeypatch.setattr(gate, "REMOTION_ROOT", remotion)
    tools = gate.RemotionTools(node, npm_cli, "v20.19.4", "10.8.2")
    commands: list[list[str]] = []
    monkeypatch.setattr(gate, "_check_free_space", lambda: None)
    monkeypatch.setattr(gate, "_validate_install", lambda: None)
    monkeypatch.setattr(
        gate,
        "_run",
        lambda command, **kwargs: commands.append(command),
    )
    gate._install(tools, {})

    assert commands == [[str(node), str(npm_cli), "ci", "--no-audit", "--fund=false"]]
    assert all(Path(part).is_absolute() for part in commands[0][:2])


def test_version_probe_is_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    def timeout(*_args: object, **_kwargs: object) -> None:
        raise gate.subprocess.TimeoutExpired(["node"], 5)

    monkeypatch.setattr(gate.subprocess, "run", timeout)
    with pytest.raises(RuntimeError, match="timed out"):
        gate._run_version(["node", "--version"])


def test_install_validation_rejects_unlocked_or_missing_packages(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    remotion = tmp_path / "remotion"
    node_modules = remotion / "node_modules"
    node_modules.mkdir(parents=True)
    expected = {
        "lockfileVersion": 3,
        "packages": {
            "node_modules/@banodoco/timeline-composition": {
                "version": "0.0.6",
                "integrity": "sha512-composition",
            }
        },
    }
    (remotion / "package-lock.json").write_text(json.dumps(expected), encoding="utf-8")
    (node_modules / ".package-lock.json").write_text(json.dumps(expected), encoding="utf-8")
    monkeypatch.setattr(gate, "REMOTION_ROOT", remotion)

    with pytest.raises(RuntimeError, match="required Remotion package"):
        gate._validate_install()


def test_false_zero_npm_cannot_reuse_stale_closure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    node, npm_cli = _fake_node_distribution(tmp_path)
    remotion = tmp_path / "remotion"
    node_modules = remotion / "node_modules"
    node_modules.mkdir(parents=True)
    lock = {"lockfileVersion": 3, "packages": {}}
    (remotion / "package-lock.json").write_text(json.dumps(lock), encoding="utf-8")
    (node_modules / ".package-lock.json").write_text(json.dumps(lock), encoding="utf-8")
    monkeypatch.setattr(gate, "REMOTION_ROOT", remotion)
    monkeypatch.setattr(gate, "_check_free_space", lambda: None)
    monkeypatch.setattr(gate, "_run", lambda *_args, **_kwargs: None)

    with pytest.raises(RuntimeError, match="did not produce"):
        gate._install(gate.RemotionTools(node, npm_cli, "v20.19.4", "10.8.2"), {})


_COMPOSITION = "node_modules/@banodoco/timeline-composition"
_VENDOR = "vendor/timeline-composition"


@pytest.fixture
def packed_composition(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Use the real committed link/vendor/manifests with a tiny shipped tree."""
    remotion = tmp_path / "remotion"
    source = remotion / _VENDOR
    packed = remotion / _COMPOSITION
    source.mkdir(parents=True)
    committed = json.loads((gate.REMOTION_ROOT / "package-lock.json").read_text())
    source_manifest = (gate.REMOTION_ROOT / _VENDOR / "package.json").read_bytes()
    (source / "package.json").write_bytes(source_manifest)
    (source / "README.md").write_text("Composition package\n")
    for relative in ("typescript/dist/index.js", "typescript/src/index.ts", "scripts/gen.ts"):
        path = source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("// selected source\n")
    shutil.copytree(source, packed)
    dependencies = {"@banodoco/timeline-composition": "file:vendor/timeline-composition"}
    (remotion / "package.json").write_text(json.dumps({"dependencies": dependencies}))
    external = {"version": "1.0.0", "resolved": "https://example.invalid/pinned.tgz",
                "integrity": "sha512-pinned"}
    packages = {"": {"dependencies": dependencies},
                _COMPOSITION: committed["packages"][_COMPOSITION],
                _VENDOR: committed["packages"][_VENDOR],
                "node_modules/@banodoco/timeline-schema": external,
                "node_modules/@banodoco/timeline-theme-2rp": external}
    expected = {"lockfileVersion": 3, "packages": packages}
    actual = copy.deepcopy(expected)
    actual["packages"].pop("")
    actual["packages"].pop(_VENDOR)
    installed_record = copy.deepcopy(packages[_VENDOR])
    installed_record.pop("name")
    installed_record.pop("devDependencies")
    installed_record["resolved"] = "file:vendor/timeline-composition"
    actual["packages"][_COMPOSITION] = installed_record
    for name in ("timeline-schema", "timeline-theme-2rp"):
        (remotion / "node_modules/@banodoco" / name).mkdir()
    (remotion / "package-lock.json").write_text(json.dumps(expected))
    (remotion / "node_modules/.package-lock.json").write_text(json.dumps(actual))
    monkeypatch.setattr(gate, "REMOTION_ROOT", remotion)
    return remotion


def _edit_json(path: Path, edit) -> None:
    data = json.loads(path.read_text())
    edit(data)
    path.write_text(json.dumps(data))


def test_valid_packed_composition_resolves_authentic_committed_link(packed_composition: Path) -> None:
    gate._validate_install()


def test_valid_packed_composition_checks_all_real_declared_files(packed_composition: Path) -> None:
    original = gate.REPO_ROOT / "remotion" / _VENDOR
    source = packed_composition / _VENDOR
    packed = packed_composition / _COMPOSITION
    # Replace only this fixture's two tiny package trees, never the selected source.
    shutil.rmtree(source)
    shutil.rmtree(packed)
    source.mkdir()
    for name in ("package.json", "README.md"):
        shutil.copy2(original / name, source / name)
    for name in ("typescript/dist", "typescript/src", "scripts"):
        shutil.copytree(original / name, source / name, dirs_exist_ok=True)
    shutil.copytree(source, packed)
    assert sum(path.is_file() for path in packed.rglob("*")) == 89
    gate._validate_install()


@pytest.mark.parametrize(("location", "field", "value"), [
    ("root", "dependency", "file:vendor/elsewhere"),
    ("root-lock", "dependency", "file:vendor/elsewhere"),
    ("link", "resolved", "vendor/elsewhere"),
    ("link", "resolved", "../timeline-composition"),
    ("link", "link", False),
    ("link", "version", "0.0.7"),
    ("vendor", "name", "@banodoco/other"),
    ("vendor", "version", "0.0.8"),
    ("vendor", "dependencies", {}),
    ("vendor", "peerDependencies", {}),
    ("vendor", "devDependencies", {}),
    ("vendor", "resolved", "https://example.invalid/other.tgz"),
    ("installed", "version", "0.0.8"),
    ("installed", "name", "@banodoco/other"),
    ("installed", "resolved", "vendor/timeline-composition"),
    ("installed", "resolved", "file:vendor/../vendor/timeline-composition"),
    ("installed", "dependencies", {}),
    ("installed", "peerDependencies", {}),
    ("installed", "devDependencies", {}),
    ("installed", "integrity", "sha512-unverified"),
    ("installed", "link", True),
    ("installed", "bin", "redirect.js"),
])
def test_packed_composition_rejects_contradictory_lock_metadata(
    packed_composition: Path, location: str, field: str, value: object,
) -> None:
    path = packed_composition / "package-lock.json"
    key = {"root-lock": "", "link": _COMPOSITION, "vendor": _VENDOR}.get(location)
    if location == "root":
        path = packed_composition / "package.json"
    elif location == "installed":
        path = packed_composition / "node_modules/.package-lock.json"
        key = _COMPOSITION

    def edit(data):
        record = data if location == "root" else data["packages"][key]
        if field == "dependency":
            record["dependencies"]["@banodoco/timeline-composition"] = value
        else:
            record[field] = value

    _edit_json(path, edit)
    with pytest.raises(RuntimeError, match="Composition"):
        gate._validate_install()


@pytest.mark.parametrize("side", [_VENDOR, _COMPOSITION])
@pytest.mark.parametrize(("field", "value"), [
    ("name", "@banodoco/other"), ("version", "0.0.8"),
    ("dependencies", {}), ("main", "./redirect.js"),
    ("exports", {".": "./redirect.js"}),
])
def test_packed_composition_rejects_changed_manifest(
    packed_composition: Path, side: str, field: str, value: object,
) -> None:
    _edit_json(packed_composition / side / "package.json",
               lambda data: data.update({field: value}))
    with pytest.raises(RuntimeError, match="Composition"):
        gate._validate_install()


@pytest.mark.parametrize("change", ["bytes", "missing", "extra", "mode", "redirect",
                                    "directory-symlink", "file-symlink", "package-symlink",
                                    "source-symlink", "source-file-symlink", "scope-symlink"])
def test_packed_composition_rejects_changed_inventory_or_paths(
    packed_composition: Path, change: str,
) -> None:
    source = packed_composition / _VENDOR
    packed = packed_composition / _COMPOSITION
    path = packed / "typescript/src/index.ts"
    if change == "bytes":
        path.write_text("// different evaluator\n")
    elif change == "missing":
        path.unlink()
    elif change == "extra":
        (packed / "extra.js").write_text("// injected\n")
    elif change == "mode":
        path.chmod(0o755)
    elif change == "redirect":
        path.rename(path.with_name("redirect.ts"))
    elif change in ("directory-symlink", "source-symlink", "package-symlink", "scope-symlink"):
        selected = {"directory-symlink": packed / "typescript/src", "source-symlink": source,
                    "package-symlink": packed,
                    "scope-symlink": packed_composition / "node_modules/@banodoco"}[change]
        moved = packed_composition / "redirected"
        selected.rename(moved)
        selected.symlink_to(moved, target_is_directory=True)
    else:
        if change == "source-file-symlink":
            path = source / "typescript/src/index.ts"
        path.unlink()
        # An internal link to identical bytes is also forbidden.
        path.symlink_to(source / "scripts/gen.ts")
    with pytest.raises(RuntimeError, match="Composition"):
        gate._validate_install()


def test_packed_composition_rejects_missing_source_file(packed_composition: Path) -> None:
    (packed_composition / _VENDOR / "typescript/src/index.ts").unlink()
    with pytest.raises(RuntimeError, match="inventory"):
        gate._validate_install()


@pytest.mark.parametrize("field", ["version", "resolved", "integrity"])
def test_packed_copy_keeps_external_lock_comparison_strict(
    packed_composition: Path, field: str,
) -> None:
    _edit_json(packed_composition / "node_modules/.package-lock.json",
               lambda data: data["packages"]["node_modules/@banodoco/timeline-schema"].update(
                   {field: "changed"}))
    with pytest.raises(RuntimeError, match=f"installed lock mismatch.*{field}"):
        gate._validate_install()


def test_install_validation_rejects_unlocked_package(packed_composition: Path) -> None:
    _edit_json(packed_composition / "node_modules/.package-lock.json",
               lambda data: data["packages"].update({"node_modules/unlocked": {"version": "1"}}))
    with pytest.raises(RuntimeError, match="absent from package-lock"):
        gate._validate_install()


def test_packed_copy_retains_direct_dependency_presence_check(packed_composition: Path) -> None:
    def edit(data):
        data["packages"][""]["dependencies"]["missing-direct"] = "1.0.0"
    _edit_json(packed_composition / "package-lock.json", edit)
    with pytest.raises(RuntimeError, match="direct dependency is absent"):
        gate._validate_install()


@pytest.mark.parametrize("record", [_COMPOSITION, _VENDOR])
def test_packed_composition_requires_both_committed_records(
    packed_composition: Path, record: str,
) -> None:
    _edit_json(packed_composition / "package-lock.json",
               lambda data: data["packages"].pop(record))
    with pytest.raises(RuntimeError, match="Composition"):
        gate._validate_install()


@pytest.mark.parametrize("field", ["version", "resolved", "dependencies", "peerDependencies"])
def test_packed_composition_requires_installed_metadata(packed_composition: Path, field: str) -> None:
    _edit_json(packed_composition / "node_modules/.package-lock.json",
               lambda data: data["packages"][_COMPOSITION].pop(field))
    with pytest.raises(RuntimeError, match="Composition"):
        gate._validate_install()


def test_packed_composition_rejects_contradictory_installed_vendor_record(
    packed_composition: Path,
) -> None:
    _edit_json(packed_composition / "node_modules/.package-lock.json",
               lambda data: data["packages"].update({_VENDOR: {"version": "0.0.8"}}))
    with pytest.raises(RuntimeError, match="installed vendor record"):
        gate._validate_install()


def test_packed_composition_rejects_changed_manifest_bytes(packed_composition: Path) -> None:
    path = packed_composition / _COMPOSITION / "package.json"
    path.write_text(path.read_text() + "\n")
    with pytest.raises(RuntimeError, match="shipped bytes"):
        gate._validate_install()


def test_packed_composition_rejects_changed_shipped_declaration(packed_composition: Path) -> None:
    for side in (_VENDOR, _COMPOSITION):
        _edit_json(packed_composition / side / "package.json",
                   lambda data: data.update({"files": ["../redirect"]}))
    with pytest.raises(RuntimeError, match="files declaration"):
        gate._validate_install()
