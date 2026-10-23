"""Bounded G5/R2r historical fixture authoring adapter.

This file is capture evidence, not Runtime product code.  It executes the
old public publication once against a disposable restored pre-cut realm, then
qualifies the resulting authenticated backup with the current Runtime reader.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tarfile
import uuid
from pathlib import Path


OLD_COMMIT = "0ba9622a3e98a85577ef893be85988ba7f203b88"
OLD_TREE = "c0bbd76656ac21439d11bf928eb970d60fe6e690"
CURRENT_COMMIT = "d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b"
EXPECTED_DIGEST = "sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb"
FIXTURE_KEY = bytes.fromhex(
    "00112233445566778899aabbccddeeff"
    "ffeeddccbbaa99887766554433221100"
)


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def git_value(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def assert_old_source(old_root: Path, old_repo: Path) -> dict:
    commit = git_value(old_repo, "rev-parse", OLD_COMMIT)
    tree = git_value(old_repo, "rev-parse", f"{OLD_COMMIT}^{{tree}}")
    assert commit == OLD_COMMIT, (commit, OLD_COMMIT)
    assert tree == OLD_TREE, (tree, OLD_TREE)
    compile_targets = (
        old_root / "runtime_protocol/service.py",
        old_root / "runtime_protocol/backup.py",
        old_root / "tests/precut_realm_fixture.py",
    )
    for path in compile_targets:
        compile(path.read_text(), str(path), "exec")
    sys.path[:0] = [str(old_root), str(old_root / "packages/python"), str(old_root / "tests")]
    import runtime_protocol.service as service_module

    service_origin = Path(service_module.__file__).resolve()
    assert service_origin.is_relative_to(old_root.resolve()), service_origin
    return {
        "commit": commit,
        "tree": tree,
        "service_module": str(service_origin),
        "compiled": [str(path) for path in compile_targets],
    }


def assert_parent_shape(parent: dict, expected: dict) -> None:
    assert digest(parent) == EXPECTED_DIGEST, digest(parent)
    assert parent == expected, "public old writer normalized the target parent unexpectedly"
    assert parent["clips"][0]["app"]["until"] is None
    assert parent["clips"][0]["app"]["astrid"]["until"] is None
    assert parent["clips"][0]["app"]["astrid"]["opaque"] == [None, {"keep": True}]
    other = parent["clips"][1]
    assert "app" not in other and "volume" not in other and "effects" not in other
    assert other["extension"]["opaque"] == [None, {"keep": True}]


def target_parent(original: dict) -> dict:
    parent = copy.deepcopy(original)
    parent["config"]["tracks"].append({"id": "music-other", "kind": "audio"})
    parent["clips"][0]["app"] = {
        "on": "word:word-1",
        "until": None,
        "until_film_end": True,
        "astrid": {
            "on": "word:word-1",
            "until": None,
            "until_film_end": True,
            "fixed_start": False,
            "for": 5.5,
            "opaque": [None, {"keep": True}],
        },
    }
    parent["clips"].append({
        "id": "music-other",
        "clipType": "audio",
        "asset": "music-bed",
        "track": "music-other",
        "at": 0,
        "hold": 5.5,
        "extension": {"opaque": [None, {"keep": True}]},
    })
    parent["config"]["clips"] = copy.deepcopy(parent["clips"])
    return parent


def _read_object(service, digest_value: str) -> bytes:
    return service.cas.read(digest_value.removeprefix("sha256:"))


def run_capture(old_root: Path, old_repo: Path, expectation_path: Path, work_root: Path) -> dict:
    source_facts = assert_old_source(old_root, old_repo)
    from precut_realm_fixture import FIXTURE_BACKUP_KEY, load_precut_realm_fixture
    from runtime_protocol.backup import create_backup, verify_backup
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_baseline import verify_baseline

    assert FIXTURE_BACKUP_KEY == FIXTURE_KEY
    expectation = read_json(expectation_path)
    expectation_manifest = read_json(expectation_path.with_suffix(".manifest.json"))
    expected_parent = expectation["required_parent"]["payload"]
    loader_root = work_root / "loader"
    loader_root.mkdir(parents=True, exist_ok=True)
    fixture = load_precut_realm_fixture(loader_root)
    duplicate = fixture.copy_roots[1]
    service = RuntimeService(duplicate)
    publication = None
    try:
        before = verify_baseline(
            service.store.conn,
            fixture.pins["project_id"],
            fixture.pins["timeline_id"],
            read_object=lambda value: _read_object(service, value),
        )
        original = service.get_project_parent_composition_revision(
            fixture.pins["project_id"], fixture.pins["timeline_id"], fixture.pins["parent_revision_id"]
        )
        assert original["content_digest"] == expectation_manifest["derivation"]["source_parent"]["source_parent_digest"]
        original_parent = copy.deepcopy(original["payload"])
        parent = target_parent(original_parent)
        assert_parent_shape(parent, expected_parent)
        immutable_before = {
            "occurrences": copy.deepcopy(original_parent["occurrences"]),
            "registry": copy.deepcopy(original_parent["registry"]),
            "media_ids": tuple(sorted(fixture.pins["media_ids"])),
            "shots": copy.deepcopy(before["canonical_document"]["shot_revisions"]),
            "internal_timelines": copy.deepcopy(before["canonical_document"]["internal_timeline_revisions"]),
        }
        revision_id = uuid.uuid4().hex
        idempotency_key = uuid.uuid4().hex
        publication = service.publish_parent_composition(
            fixture.pins["project_id"],
            fixture.pins["timeline_id"],
            {
                "project_id": fixture.pins["project_id"],
                "timeline_id": fixture.pins["timeline_id"],
                "expected_head": fixture.pins["parent_revision_id"],
                "parent_revision_id": revision_id,
                "parent_composition": parent,
            },
            idempotency_key=idempotency_key,
        )
        assert isinstance(publication, dict) and isinstance(publication.get("receipt"), dict)
        after = verify_baseline(
            service.store.conn,
            fixture.pins["project_id"],
            fixture.pins["timeline_id"],
            read_object=lambda value: _read_object(service, value),
        )
        actual_parent = after["canonical_document"]["parent_revision"]["payload"]
        assert_parent_shape(actual_parent, expected_parent)
        assert after["head"]["revision_id"] == revision_id
        assert after["head"]["publication_id"] == publication["receipt"]["receipt_id"]
        assert len(after["entries"]) == 2, after["entries"]
        latest = after["entries"][-1]
        assert latest["revision_id"] == revision_id
        assert latest["publication_id"] == after["head"]["publication_id"]
        assert latest["receipt"]["receipt_id"] == publication["receipt"]["receipt_id"]
        assert latest["previous"] == {
            "revision_id": fixture.pins["parent_revision_id"],
            "publication_id": before["head"]["publication_id"],
        }
        assert actual_parent["occurrences"] == immutable_before["occurrences"]
        assert actual_parent["registry"] == immutable_before["registry"]
        assert after["canonical_document"]["shot_revisions"] == immutable_before["shots"]
        assert after["canonical_document"]["internal_timeline_revisions"] == immutable_before["internal_timelines"]
        assert tuple(sorted(fixture.pins["media_ids"])) == immutable_before["media_ids"]
        for media_id in fixture.pins["media_ids"]:
            assert _read_object(service, media_id)
        backup_dir = work_root / "backup"
        backup_result = create_backup(service.store, backup_dir, key=FIXTURE_KEY)
        verified_backup = verify_backup(backup_dir, key=FIXTURE_KEY)
        assert verified_backup["manifest"] == backup_result["manifest"]
        backup_manifest = verified_backup["manifest"]
    finally:
        service.close()

    archive_path = work_root / "archive.tar.gz"
    with tarfile.open(archive_path, "w:gz") as archive:
        archive.add(backup_dir, arcname="backup")
    return {
        "source": source_facts,
        "fixture_pins": fixture.pins,
        "before": before,
        "after": after,
        "publication": publication,
        "backup_manifest": backup_manifest,
        "backup_verification": {"manifest": verified_backup["manifest"], "doctor": verified_backup["doctor"]},
        "archive_path": str(archive_path),
        "archive_sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
        "archive_bytes": archive_path.stat().st_size,
        "revision_id": revision_id,
        "idempotency_key": idempotency_key,
        "expected_digest": EXPECTED_DIGEST,
    }


def extract_archive(archive_path: Path, destination: Path) -> Path:
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            assert member.name == member.name.lstrip("/") and ".." not in Path(member.name).parts
            assert not member.issym() and not member.islnk()
        archive.extractall(destination)
    return destination / "backup"


def run_current_read(current_root: Path, archive_path: Path, work_root: Path) -> dict:
    import runtime_protocol.service as service_module
    from runtime_protocol.backup import restore_backup, verify_backup
    from runtime_protocol.timeline_commit_baseline import verify_baseline
    from runtime_protocol.service import RuntimeService
    from precut_realm_fixture import _read_pins

    origin = Path(service_module.__file__).resolve()
    assert origin.is_relative_to(current_root.resolve()), origin
    assert git_value(current_root, "rev-parse", "HEAD") == CURRENT_COMMIT
    extracted = extract_archive(archive_path, work_root / "current-archive")
    verified = verify_backup(extracted, key=FIXTURE_KEY)
    restored = work_root / "current-restored"
    restore_result = restore_backup(extracted, restored, key=FIXTURE_KEY)
    pins = _read_pins(restored)
    service = RuntimeService(restored)
    try:
        facts = verify_baseline(
            service.store.conn,
            pins["project_id"],
            pins["timeline_id"],
            read_object=lambda value: service.cas.read(value.removeprefix("sha256:")),
        )
    finally:
        service.close()
    assert facts["head"]["revision_id"]
    assert digest(facts["canonical_document"]["parent_revision"]["payload"]) == EXPECTED_DIGEST
    assert facts["canonical_document"]["parent_revision"]["payload"] == read_json(EXPECTATION_PATH)["required_parent"]["payload"]
    return {
        "runtime_service_module": str(origin),
        "runtime_commit": git_value(current_root, "rev-parse", "HEAD"),
        "verified_manifest": verified["manifest"],
        "restore": restore_result,
        "facts": facts,
    }


def main() -> None:
    global EXPECTATION_PATH
    if sys.argv[1] == "--current":
        current_root = Path(sys.argv[2]).resolve()
        archive_path = Path(sys.argv[3]).resolve()
        expectation_path = Path(sys.argv[4]).resolve()
        work_root = Path(sys.argv[5]).resolve()
        EXPECTATION_PATH = expectation_path
        result = run_current_read(current_root, archive_path, work_root)
        write_json(work_root / "current-readback.json", result)
        print(json.dumps(result, sort_keys=True))
        return
    old_root = Path(sys.argv[1]).resolve()
    old_repo = Path(sys.argv[2]).resolve()
    expectation_path = Path(sys.argv[3]).resolve()
    current_root = Path(sys.argv[4]).resolve()
    work_root = Path(sys.argv[5]).resolve()
    EXPECTATION_PATH = expectation_path
    work_root.mkdir(parents=True, exist_ok=True)
    captured = run_capture(old_root, old_repo, expectation_path, work_root)
    child_env = os.environ.copy()
    child_env["PYTHONPATH"] = os.pathsep.join((str(current_root), str(current_root / "tests")))
    current_command = [
        sys.executable,
        __file__,
        "--current",
        str(current_root),
        captured["archive_path"],
        str(expectation_path),
        str(work_root),
    ]
    subprocess.run(current_command, check=True, env=child_env)
    current = read_json(work_root / "current-readback.json")
    assert current["verified_manifest"] == captured["backup_manifest"]
    assert current["facts"]["canonical_document"] == captured["after"]["canonical_document"]
    captured["current"] = current
    write_json(work_root / "capture-readback.json", captured)
    print(json.dumps({
        "archive": captured["archive_path"],
        "archive_sha256": captured["archive_sha256"],
        "archive_bytes": captured["archive_bytes"],
        "revision_id": captured["revision_id"],
        "publication_id": captured["after"]["head"]["publication_id"],
        "parent_digest": captured["after"]["document_digest"],
        "current_restore": current["restore"]["destination"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
