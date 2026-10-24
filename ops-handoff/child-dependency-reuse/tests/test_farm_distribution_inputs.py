from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest

PACKET = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/artifacts/bootstrap-wheel-input-0932-"
    "443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz"
)
CANDIDATE = Path(__file__).parents[1] / "candidate"
sys.path.insert(0, str(CANDIDATE))

import verify_farm_distribution_inputs as component
from verify_farm_distribution_inputs import (
    APPROVED_WHEELS,
    SCHEMA_COMMIT,
    SCHEMA_DECLARATION,
    SCHEMA_SUBDIRECTORY,
    SCHEMA_VERSION,
    ValidationError,
    validate_farm_distribution_inputs,
    validate_schema_source,
    validate_wheel_inputs,
)


def reviewed_wheelhouse(tmp_path: Path) -> Path:
    assert PACKET.is_file(), "the reviewed original input packet is required"
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.parent.mkdir(parents=True, exist_ok=True)
    wheelhouse.mkdir()
    prefix = "timeline-bootstrap-wheel-input-0932/wheelhouse/"
    with tarfile.open(PACKET, "r:gz") as archive:
        for member in archive.getmembers():
            if member.name.startswith(prefix) and member.isfile():
                target = wheelhouse / Path(member.name).name
                target.write_bytes(archive.extractfile(member).read())  # type: ignore[union-attr]
    return wheelhouse


def forged_additional_wheel(path: Path) -> component.WheelInput:
    files = {
        "evilpkg/__init__.py": b"FORGED = True\n",
        "evilpkg-1.0.dist-info/METADATA": (
            b"Metadata-Version: 2.1\nName: evilpkg\nVersion: 1.0\n"
        ),
        "evilpkg-1.0.dist-info/WHEEL": b"Wheel-Version: 1.0\nTag: py3-none-any\n",
    }
    record_rows = []
    for name, data in files.items():
        digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")
        record_rows.append(f"{name},sha256={digest},{len(data)}")
    record_rows.append("evilpkg-1.0.dist-info/RECORD,,")
    files["evilpkg-1.0.dist-info/RECORD"] = ("\n".join(record_rows) + "\n").encode()
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    data = path.read_bytes()
    return component.WheelInput(
        path=path,
        filename=path.name,
        name="evilpkg",
        version="1.0",
        sha256=hashlib.sha256(data).hexdigest(),
        size=len(data),
        role="additional-test",
        source="caller-forged",
    )


def test_reviewed_packet_validates_as_exact_role_partition(tmp_path: Path) -> None:
    receipt = validate_wheel_inputs(reviewed_wheelhouse(tmp_path))

    assert receipt["roles"] == {
        "bootstrap3": [
            "pip-26.2.1-py3-none-any.whl",
            "setuptools-80.9.0-py3-none-any.whl",
            "wheel-0.46.3-py3-none-any.whl",
        ],
        "test2": [
            "execnet-2.1.2-py3-none-any.whl",
            "pytest_xdist-3.8.0-py3-none-any.whl",
        ],
        "additional": [],
    }
    assert len(receipt["distributions"]) == 5
    assert receipt["component_identity"] == hashlib.sha256(
        json.dumps(
            {key: value for key, value in receipt.items() if key != "component_identity"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    for distribution in receipt["distributions"]:
        assert distribution["record"]
        assert all(row["path"] in receipt["ownership"] for row in distribution["record"])


def test_reviewed_packet_rejects_tampering_and_unknown_files(tmp_path: Path) -> None:
    wheelhouse = reviewed_wheelhouse(tmp_path)
    target = wheelhouse / "execnet-2.1.2-py3-none-any.whl"
    target.write_bytes(target.read_bytes() + b"tamper")
    with pytest.raises(ValidationError, match="approved bytes"):
        validate_wheel_inputs(wheelhouse)

    wheelhouse = reviewed_wheelhouse(tmp_path / "second")
    (wheelhouse / "unreviewed.whl").write_bytes(b"unknown")
    with pytest.raises(ValidationError, match="set mismatch"):
        validate_wheel_inputs(wheelhouse)


def test_packet_rejects_symlink_escape(tmp_path: Path) -> None:
    wheelhouse = reviewed_wheelhouse(tmp_path)
    outside = tmp_path / "outside.whl"
    outside.write_bytes((wheelhouse / APPROVED_WHEELS[0].filename).read_bytes())
    (wheelhouse / APPROVED_WHEELS[0].filename).unlink()
    (wheelhouse / APPROVED_WHEELS[0].filename).symlink_to(outside)
    with pytest.raises(ValidationError, match="non-file or symlink"):
        validate_wheel_inputs(wheelhouse)


def test_required_schema_source_is_fail_closed_before_maker_receipt(tmp_path: Path) -> None:
    wheelhouse = reviewed_wheelhouse(tmp_path)
    with pytest.raises(ValidationError, match="schema source"):
        validate_farm_distribution_inputs(
            schema_source=tmp_path / "missing-agent-source",
            wheelhouse=wheelhouse,
        )


def test_current_source_snapshot_cannot_be_relabelled_as_selected_schema_source() -> None:
    current_agent = Path("/home/user/work/agent")
    if not current_agent.is_dir():
        pytest.fail("the reviewed Agent checkout is required for this refusal test")
    with pytest.raises(ValidationError, match="selected Agent commit"):
        validate_schema_source(current_agent)


def test_schema_identity_is_exact_and_does_not_conflate_repository_urls() -> None:
    assert SCHEMA_COMMIT == "242f9c4306bf3b501222cb041a9eb246ef47bc85"
    assert SCHEMA_SUBDIRECTORY == "packages/timeline-schema/python"
    assert SCHEMA_VERSION == "0.0.2"
    assert "astrid-agent.git" in SCHEMA_DECLARATION
    assert "ArtAgents.git" not in SCHEMA_DECLARATION


def private_schema_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "agent-source"
    package = root / SCHEMA_SUBDIRECTORY / "banodoco_timeline_schema"
    package.mkdir(parents=True)
    (root / "pyproject.toml").write_text(
        "[project.optional-dependencies]\n"
        f'test = [{SCHEMA_DECLARATION!r}]\n'
    )
    (root / SCHEMA_SUBDIRECTORY / "pyproject.toml").write_text(
        '[project]\nname = "banodoco-timeline-schema"\nversion = "0.0.2"\n'
    )
    (package / "__init__.py").write_text("PACKAGE = True\n")
    return root


def fake_schema_git(root: Path, *, commit: str = SCHEMA_COMMIT, status: str = ""):
    tracked = [
        "packages/timeline-schema/python/banodoco_timeline_schema/__init__.py",
        "packages/timeline-schema/python/pyproject.toml",
    ]

    # Synthetic Git authority ONLY: cannot establish the pinned real commit.
    # The production _git backend also hashes the selected commit object.
    tree_entries = {}
    contents = {}
    for relative in ["pyproject.toml", *tracked]:
        path = root / relative
        contents[relative] = path.read_bytes() if path.is_file() else b""

    def make_tree(prefix):
        names = sorted(
            {
                path[len(prefix) :].split("/", 1)[0]
                for path in contents
                if path.startswith(prefix)
            }
        )
        raw = []
        serialized = bytearray()
        for name in names:
            path = prefix + name
            if path in contents:
                mode, kind = "100644", "blob"
                oid = component._git_object_digest("blob", contents[path])
            else:
                mode, kind = "040000", "tree"
                oid = make_tree(path + "/")
            raw.append(f"{mode} {kind} {oid}\t{name}\0")
            serialized.extend(
                mode.lstrip("0").encode()
                + b" "
                + name.encode()
                + b"\0"
                + bytes.fromhex(oid)
            )
        oid = component._git_object_digest("tree", bytes(serialized))
        tree_entries[oid] = "".join(raw)
        return oid

    tree = make_tree("")

    def probe(_root: Path, *args: str) -> str:
        if args == ("rev-parse", "--show-toplevel"):
            return f"{root}\n"
        if args == ("rev-parse", "HEAD"):
            return f"{commit}\n"
        if args == ("rev-parse", f"{SCHEMA_COMMIT}^{{commit}}"):
            return f"{SCHEMA_COMMIT}\n"
        if args == ("status", "--porcelain=v1", "--untracked-files=all"):
            return status
        if args == ("ls-files", "-s"):
            return "\n".join(f"100644 blob 0\t{path}" for path in tracked)
        if args == ("ls-files", "-s", "--", SCHEMA_SUBDIRECTORY):
            return "\n".join(f"100644 blob 0\t{path}" for path in tracked)
        if args == ("rev-parse", "HEAD^{tree}"):
            return f"{tree}\n"
        if args == ("rev-parse", f"{SCHEMA_COMMIT}^{{tree}}"):
            return f"{tree}\n"
        if args == ("cat-file", "commit", SCHEMA_COMMIT):
            return f"tree {tree}\n\nSynthetic fixture, not original custody.\n"
        if len(args) == 3 and args[:2] == ("ls-tree", "-z"):
            return tree_entries[args[2]]
        raise AssertionError(args)

    return probe


def test_private_schema_fixture_produces_source_identity_not_custody(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The monkeypatched Git probe exercises receipt shape, not source custody."""

    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))

    identity = validate_schema_source(root)

    assert identity["commit"] == SCHEMA_COMMIT
    assert identity["subdirectory"] == SCHEMA_SUBDIRECTORY
    assert identity["package"] == "banodoco-timeline-schema"
    assert identity["files"]


def test_caller_forged_additional_wheel_has_no_independent_authority(tmp_path: Path) -> None:
    wheelhouse = reviewed_wheelhouse(tmp_path)
    forged = forged_additional_wheel(wheelhouse / "evilpkg-1.0-py3-none-any.whl")
    with pytest.raises(ValidationError, match="additional wheel authority"):
        validate_wheel_inputs(wheelhouse, additional_wheels=(forged,))


def test_ignored_schema_escape_link_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = private_schema_fixture(tmp_path)
    outside = tmp_path / "outside.py"
    outside.write_text("ESCAPE = True\n")
    (root / SCHEMA_SUBDIRECTORY / "banodoco_timeline_schema" / "ignored.py").symlink_to(
        outside
    )
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    with pytest.raises(ValidationError, match="symlink"):
        validate_schema_source(root)


def test_ignored_schema_extra_file_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = private_schema_fixture(tmp_path)
    (root / SCHEMA_SUBDIRECTORY / "ignored.py").write_text("EXTRA = True\n")
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    with pytest.raises(ValidationError, match="unowned file"):
        validate_schema_source(root)


def test_ignored_schema_extra_directory_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = private_schema_fixture(tmp_path)
    (root / SCHEMA_SUBDIRECTORY / "ignored-dir").mkdir()
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    with pytest.raises(ValidationError, match="unowned directory"):
        validate_schema_source(root)


def test_schema_tree_must_match_the_selected_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = private_schema_fixture(tmp_path)

    def forged_tree_git(_root: Path, *args: str) -> str:
        result = fake_schema_git(root)(_root, *args)
        if args == ("rev-parse", "HEAD^{tree}"):
            return "wrong-tree\n"
        return result

    monkeypatch.setattr(component, "_git", forged_tree_git)
    with pytest.raises(ValidationError, match="tree is not bound"):
        validate_schema_source(root)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("commit", "selected Agent commit"),
        ("dirty", "tree is not clean"),
        ("url", "exact selected schema declaration"),
        ("package", "metadata name/version"),
        ("subpath", "schema package source tree is incomplete"),
    ],
)
def test_private_schema_fixture_rejects_wrong_source_identity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutation: str,
    message: str,
) -> None:
    root = private_schema_fixture(tmp_path)
    commit = "0" * 40
    status = " M pyproject.toml\n"
    if mutation == "url":
        (root / "pyproject.toml").write_text(
            '[project.optional-dependencies]\ntest = ["banodoco-timeline-schema @ '
            "git+https://github.com/banodoco/ArtAgents.git@"
            f'{SCHEMA_COMMIT}#subdirectory={SCHEMA_SUBDIRECTORY}"]\n'
        )
    elif mutation == "package":
        (root / SCHEMA_SUBDIRECTORY / "pyproject.toml").write_text(
            '[project]\nname = "wrong-schema"\nversion = "9.9.9"\n'
        )
    elif mutation == "subpath":
        (root / SCHEMA_SUBDIRECTORY / "banodoco_timeline_schema").rename(
            root / "wrong-package"
        )
    monkeypatch.setattr(
        component,
        "_git",
        fake_schema_git(
            root,
            commit=commit if mutation == "commit" else SCHEMA_COMMIT,
            status=status if mutation == "dirty" else "",
        ),
    )
    with pytest.raises(ValidationError, match=message):
        validate_schema_source(root)

@pytest.mark.parametrize(
    "relative",
    [
        ".",
        "packages",
        "packages/timeline-schema",
        SCHEMA_SUBDIRECTORY,
        f"{SCHEMA_SUBDIRECTORY}/banodoco_timeline_schema",
    ],
)
@pytest.mark.parametrize("mode", [0o775, 0o777])
def test_schema_refuses_writable_directories(tmp_path, monkeypatch, relative, mode):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    (root / relative).chmod(mode)
    with pytest.raises(ValidationError, match="mode|writable"):
        validate_schema_source(root)


@pytest.mark.parametrize(
    "relative",
    [
        ".",
        "..",
        "packages",
        f"{SCHEMA_SUBDIRECTORY}/banodoco_timeline_schema",
        f"{SCHEMA_SUBDIRECTORY}/banodoco_timeline_schema/__init__.py",
        "pyproject.toml",
    ],
)
@pytest.mark.parametrize("field", ["st_uid", "st_gid"])
def test_schema_refuses_foreign_filesystem_ownership(
    tmp_path, monkeypatch, relative, field
):
    root = private_schema_fixture(tmp_path)
    target = root / relative
    node = target.stat()
    original_stat = os.stat
    original_fstat = os.fstat

    def foreign(info):
        if (info.st_dev, info.st_ino) != (node.st_dev, node.st_ino):
            return info
        values = list(info)
        values[4 if field == "st_uid" else 5] += 12345
        return os.stat_result(values)

    def fake_stat(*args, **kwargs):
        return foreign(original_stat(*args, **kwargs))

    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    monkeypatch.setattr(os, "stat", fake_stat)
    monkeypatch.setattr(os, "fstat", lambda fd: foreign(original_fstat(fd)))
    with pytest.raises(ValidationError, match="owner|group"):
        validate_schema_source(root)


@pytest.mark.parametrize("mode", [0o664, 0o666, 0o4644])
def test_schema_refuses_unsafe_file_modes(tmp_path, monkeypatch, mode):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    (root / SCHEMA_SUBDIRECTORY / "banodoco_timeline_schema/__init__.py").chmod(mode)
    with pytest.raises(ValidationError, match="mode"):
        validate_schema_source(root)


@pytest.mark.parametrize("mode", [0o775, 0o777, 0o1777])
def test_schema_refuses_writable_external_ancestor(tmp_path, monkeypatch, mode):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    tmp_path.chmod(mode)
    with pytest.raises(ValidationError, match="mode"):
        validate_schema_source(root)


@pytest.mark.parametrize(
    "relative",
    [
        "packages",
        SCHEMA_SUBDIRECTORY,
        f"{SCHEMA_SUBDIRECTORY}/banodoco_timeline_schema",
        "pyproject.toml",
    ],
)
def test_schema_refuses_symlinked_custody_paths(tmp_path, monkeypatch, relative):
    root = private_schema_fixture(tmp_path)
    probe = fake_schema_git(root)
    target = root / relative
    moved = tmp_path / "moved"
    target.rename(moved)
    target.symlink_to(moved, target_is_directory=moved.is_dir())
    monkeypatch.setattr(component, "_git", probe)
    with pytest.raises(ValidationError, match="symlink"):
        validate_schema_source(root)


@pytest.mark.parametrize(
    "relative",
    ["pyproject.toml", f"{SCHEMA_SUBDIRECTORY}/banodoco_timeline_schema/__init__.py"],
)
def test_schema_refuses_hardlinked_source_files(tmp_path, monkeypatch, relative):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    os.link(root / relative, tmp_path / "linked")
    with pytest.raises(ValidationError, match="physical entry"):
        validate_schema_source(root)


@pytest.mark.parametrize(
    "relative",
    ["pyproject.toml", f"{SCHEMA_SUBDIRECTORY}/banodoco_timeline_schema/__init__.py"],
)
def test_clean_index_cannot_authorize_changed_blob(tmp_path, monkeypatch, relative):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    (root / relative).write_bytes(b"changed despite clean status\n")
    with pytest.raises(ValidationError, match="committed blob"):
        validate_schema_source(root)


@pytest.mark.parametrize(
    ("directory_mode", "file_mode"),
    [
        (0o700, 0o600),
        (0o750, 0o640),
        (0o755, 0o644),
        (0o500, 0o400),
        (0o550, 0o440),
        (0o555, 0o444),
    ],
)
def test_normal_private_copy_modes_and_receipt(
    tmp_path, monkeypatch, directory_mode, file_mode
):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    for path in [root, *root.rglob("*")]:
        path.chmod(directory_mode if path.is_dir() else file_mode)
    receipt = validate_schema_source(root)
    assert receipt["custody"]["uid"] == os.getuid()
    assert receipt["custody"]["gid"] == os.getgid()
    assert receipt["custody"]["root"] == str(root)
    assert all(entry["blob"] and entry["sha256"] for entry in receipt["files"])
    assert any(
        entry["path"] == str(root / SCHEMA_SUBDIRECTORY)
        for entry in receipt["custody"]["nodes"]
    )


@pytest.mark.parametrize("replacement", ["file", "symlink", "directory", "ancestor"])
def test_source_substitution_during_open_is_refused(tmp_path, monkeypatch, replacement):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    target = root / SCHEMA_SUBDIRECTORY / "banodoco_timeline_schema/__init__.py"
    original_open = os.open
    attacked = False

    def racing_open(path, flags, *args, **kwargs):
        nonlocal attacked
        if path == target.name and not attacked:
            attacked = True
            if replacement == "file":
                moved = tmp_path / "substitute.py"
                moved.write_bytes(target.read_bytes())
                moved.replace(target)
            elif replacement == "symlink":
                target.rename(tmp_path / "original.py")
                target.symlink_to(tmp_path / "original.py")
            else:
                directory = target.parent if replacement == "directory" else root
                directory.rename(tmp_path / "original-directory")
                directory.mkdir()
        return original_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(os, "open", racing_open)
    with pytest.raises(ValidationError, match="changed|custody refused"):
        validate_schema_source(root)
    assert attacked


def test_source_mutation_after_read_is_refused(tmp_path, monkeypatch):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    original_finish = component._SourceCustody.finish

    def changed_before_finish(custody):
        (root / "pyproject.toml").write_text("tampered after hashing and parse\n")
        return original_finish(custody)

    monkeypatch.setattr(component._SourceCustody, "finish", changed_before_finish)
    with pytest.raises(ValidationError, match="changed during validation"):
        validate_schema_source(root)


def test_copied_snapshot_without_object_authority_names_missing_interface(tmp_path):
    root = private_schema_fixture(tmp_path)
    with pytest.raises(
        ValidationError,
        match="missing interface: authenticated selected Agent Git object source",
    ):
        validate_schema_source(root)


def test_schema_file_mode_is_checked_before_any_source_content_read(
    tmp_path, monkeypatch
):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    (root / SCHEMA_SUBDIRECTORY / "banodoco_timeline_schema/__init__.py").chmod(0o666)

    def forbidden_read(*args, **kwargs):
        pytest.fail("unsafe source content must not be read")

    monkeypatch.setattr(component._SourceCustody, "read", forbidden_read)
    with pytest.raises(ValidationError, match="mode"):
        validate_schema_source(root)


def test_source_mutation_while_reading_is_refused(tmp_path, monkeypatch):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    target = root / SCHEMA_SUBDIRECTORY / "banodoco_timeline_schema/__init__.py"
    original_fdopen = os.fdopen

    class MutatingReader:
        def __init__(self, fd):
            self.stream = original_fdopen(fd, "rb")

        def __enter__(self):
            return self

        def read(self):
            data = self.stream.read()
            target.write_bytes(b"changed while reading\n")
            return data

        def __exit__(self, *args):
            self.stream.close()

    monkeypatch.setattr(os, "fdopen", lambda fd, mode: MutatingReader(fd))
    with pytest.raises(ValidationError, match="changed while reading"):
        validate_schema_source(root)


def test_git_backend_uses_pinned_cwd_and_refuses_forged_commit_bytes(
    tmp_path, monkeypatch
):
    import subprocess

    root = private_schema_fixture(tmp_path)
    observed = []
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "attacker"))
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.worktree")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", str(tmp_path / "attacker"))

    def backend(argv, **kwargs):
        observed.append((argv, kwargs))
        return subprocess.CompletedProcess(argv, 0, b"tree forged\n", b"")

    monkeypatch.setattr(component.subprocess, "run", backend)
    with component._SourceCustody(root) as custody:
        fd = custody.directory(root)
        with pytest.raises(
            ValidationError, match="commit content cannot be authenticated"
        ):
            component._git(fd, "cat-file", "commit", SCHEMA_COMMIT)
    argv, kwargs = observed[0]
    assert "--no-replace-objects" in argv
    assert kwargs["cwd"] == f"/proc/self/fd/{fd}"
    assert kwargs["pass_fds"] == (fd,)
    assert "GIT_DIR" not in kwargs["env"]
    assert "GIT_CONFIG_COUNT" not in kwargs["env"]
    assert kwargs["env"]["GIT_CONFIG_GLOBAL"] == os.devnull


def test_tree_listing_cannot_relabel_different_committed_bytes(tmp_path, monkeypatch):
    root = private_schema_fixture(tmp_path)
    probe = fake_schema_git(root)

    def forged_listing(fd, *args):
        result = probe(fd, *args)
        if args[:2] == ("ls-tree", "-z"):
            return result.replace("100644", "100755")
        return result

    monkeypatch.setattr(component, "_git", forged_listing)
    with pytest.raises(
        ValidationError, match="tree content does not match committed identity"
    ):
        validate_schema_source(root)


@pytest.mark.parametrize("mode", [0o1755, 0o2755, 0o4755])
def test_schema_rejects_special_directory_modes(tmp_path, monkeypatch, mode):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    (root / SCHEMA_SUBDIRECTORY).chmod(mode)
    with pytest.raises(ValidationError, match="mode"):
        validate_schema_source(root)


def test_owner_change_between_stat_and_open_is_refused(tmp_path, monkeypatch):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    target = root / SCHEMA_SUBDIRECTORY / "banodoco_timeline_schema/__init__.py"
    node = target.stat()
    original_fstat = os.fstat

    def foreign_fstat(fd):
        info = original_fstat(fd)
        if (info.st_dev, info.st_ino) == (node.st_dev, node.st_ino):
            values = list(info)
            values[4] += 12345
            return os.stat_result(values)
        return info

    monkeypatch.setattr(os, "fstat", foreign_fstat)
    with pytest.raises(ValidationError, match="changed while opening"):
        validate_schema_source(root)


def test_byte_identical_substitution_after_read_is_refused(tmp_path, monkeypatch):
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))
    original_finish = component._SourceCustody.finish
    target = root / "pyproject.toml"

    def substitute_before_finish(custody):
        substitute = tmp_path / "same-bytes.toml"
        substitute.write_bytes(target.read_bytes())
        substitute.replace(target)
        return original_finish(custody)

    monkeypatch.setattr(component._SourceCustody, "finish", substitute_before_finish)
    with pytest.raises(ValidationError, match="changed during validation"):
        validate_schema_source(root)
