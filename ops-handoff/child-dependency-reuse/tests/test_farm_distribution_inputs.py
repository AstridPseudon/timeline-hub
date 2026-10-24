from __future__ import annotations

import hashlib
import json
import sys
import tarfile
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

    def probe(_root: Path, *args: str) -> str:
        if args == ("rev-parse", "--show-toplevel"):
            return f"{root}\n"
        if args == ("rev-parse", "HEAD"):
            return f"{commit}\n"
        if args == ("status", "--porcelain=v1", "--untracked-files=all"):
            return status
        if args == ("ls-files", "-s"):
            return "\n".join(f"100644 blob fixture\t{path}" for path in tracked)
        if args == ("ls-files", "-z", "--", SCHEMA_SUBDIRECTORY):
            return "\0".join(tracked) + "\0"
        if args == ("rev-parse", "HEAD^{tree}"):
            return "tree-id\n"
        raise AssertionError(args)

    return probe


def test_private_schema_fixture_produces_source_identity_not_custody(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = private_schema_fixture(tmp_path)
    monkeypatch.setattr(component, "_git", fake_schema_git(root))

    identity = validate_schema_source(root)

    assert identity["commit"] == SCHEMA_COMMIT
    assert identity["subdirectory"] == SCHEMA_SUBDIRECTORY
    assert identity["package"] == "banodoco-timeline-schema"
    assert identity["files"]


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
