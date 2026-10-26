#!/usr/bin/env python3
"""Read-only D141 custody qualification against retained source evidence.

This script intentionally does not invoke the renderer or mutate any input.  It
recomputes the current 568-item map using the final-unit install/review
algorithm and recomputes the earlier placement receipt's aggregate using the
exact algorithm visible in the placement installer log.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


ORCH = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch"
)
DELIVERY = ORCH / "delivery"
INSTALLER = ORCH / "workers/rt-F-D141-final-unit-notes-install-next"
REVIEWER = ORCH / "workers/rt-F-D141-final-unit-notes-install-review-next"
PLACEMENT = ORCH / "workers/rt-F-D141-placement-note-install-0254"
PLACEMENT_REVIEW = ORCH / "design/rt-F-D141-placement-note-review-0258-source-manifest.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_map_sha(value: dict) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def current_inventory() -> dict:
    """Exact map shape used by final-unit installer/review.

    Source: final-unit installer log, ``outside_inventory``: sorted
    non-symlink directories/files, lstat mode, byte count, and file SHA-256.
    The two canonical target basenames are excluded.
    """

    result: dict[str, dict[str, object]] = {}
    for directory, dirnames, filenames in os.walk(DELIVERY, followlinks=False):
        dirnames[:] = sorted(
            name
            for name in dirnames
            if not os.path.islink(os.path.join(directory, name))
        )
        for filename in sorted(filenames):
            path = Path(directory) / filename
            relative = path.relative_to(DELIVERY).as_posix()
            if relative in {"README.template.md", "gate-results.md"}:
                continue
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode):
                raise AssertionError(f"non-regular outside entry: {relative}")
            result[relative] = {
                "bytes": info.st_size,
                "mode": oct(stat.S_IMODE(info.st_mode)),
                "sha256": sha_path(path),
            }
    return result


def placement_inventory() -> dict:
    """Exact map shape used by placement installer aggregate hashing.

    Source: placement installer log lines 4098-4427.  The published
    placement receipt hashes ``json.dumps(map, sort_keys=True,
    separators=(',', ':'))``.  This is intentionally a separate algorithm
    from the final-unit map above.
    """

    result: dict[str, dict[str, object]] = {}
    for directory, dirnames, filenames in os.walk(DELIVERY, followlinks=False):
        dirnames.sort()
        filenames.sort()
        for filename in filenames:
            path = Path(directory) / filename
            if path in {DELIVERY / "README.template.md", DELIVERY / "gate-results.md"}:
                continue
            relative = str(path.relative_to(DELIVERY))
            info = path.lstat()
            item: dict[str, object] = {
                "mode": format(stat.S_IMODE(info.st_mode), "04o"),
                "regular": stat.S_ISREG(info.st_mode),
                "symlink": path.is_symlink(),
                "sha256": sha_path(path) if stat.S_ISREG(info.st_mode) else None,
            }
            if path.is_symlink():
                item["link_target"] = os.readlink(path)
            result[relative] = item
    return result


def assert_hash(path: Path, expected: str) -> None:
    actual = sha_path(path)
    if actual != expected:
        raise AssertionError(f"{path}: expected {expected}, got {actual}")


def main() -> int:
    installer_installation_path = INSTALLER / "evidence/installation.json"
    installer_manifest_path = INSTALLER / "evidence/source-manifest.json"
    review_path = REVIEWER / "evidence/review.json"
    review_manifest_path = REVIEWER / "evidence/source-manifest.json"
    placement_manifest_path = PLACEMENT / "evidence/source-manifest.json"

    installation = load_json(installer_installation_path)
    installer_manifest = load_json(installer_manifest_path)
    review = load_json(review_path)
    review_manifest = load_json(review_manifest_path)
    placement_manifest = load_json(placement_manifest_path)
    placement_review = load_json(PLACEMENT_REVIEW)

    if review["verdict"] != "FAIL_CUSTODY_LIMIT":
        raise AssertionError("the retained independent review is not FAIL_CUSTODY_LIMIT")
    if installer_manifest["outside_inventory_equal"] is not True:
        raise AssertionError("retained installer equality field changed")
    if review_manifest["outside_manifest_scope"]["genuine_pre_post_comparison_observable"] is not False:
        raise AssertionError("retained review custody limitation changed")

    current = current_inventory()
    review_current = review_manifest["outside_manifest_scope"]["recomputed_inventory"]
    installer_before = installer_manifest["outside_files_before"]
    installer_after = installer_manifest["outside_files_after"]

    if len(current) != 568:
        raise AssertionError(f"current outside count is {len(current)}, expected 568")
    if current != review_current:
        raise AssertionError("current map differs from independent review recomputation")
    if current != installer_after:
        raise AssertionError("current map differs from retained installer after map")
    if current != installer_before:
        raise AssertionError("serialized installer before map is not current map")
    if not review_manifest["outside_manifest_scope"]["current_equals_recorded_before"]:
        raise AssertionError("review did not report current equality with serialized before field")
    if not review_manifest["outside_manifest_scope"]["current_equals_recorded_after"]:
        raise AssertionError("review did not report current equality with serialized after field")

    placement_current = placement_inventory()
    placement_expected = placement_manifest["outside_inventory"]
    placement_review_inventory = placement_review["outside_inventory"]
    if len(placement_current) != placement_expected["count"]:
        raise AssertionError("placement aggregate count mismatch")
    placement_aggregate = sha_bytes(
        json.dumps(placement_current, sort_keys=True, separators=(",", ":")).encode()
    )
    if placement_aggregate != placement_expected["sha256"]:
        raise AssertionError("current paths do not reproduce earlier placement aggregate")
    if placement_review_inventory["sha256"] != placement_expected["sha256"]:
        raise AssertionError("placement independent review aggregate changed")
    if placement_review_inventory["count"] != placement_expected["count"]:
        raise AssertionError("placement independent review count changed")

    target_results = {}
    for name, record in installation["targets"].items():
        target = Path(record["path"])
        candidate = Path(record["source"])
        backup = Path(record["backup_path"])
        target_stat = target.lstat()
        if stat.S_ISLNK(target_stat.st_mode) or not stat.S_ISREG(target_stat.st_mode):
            raise AssertionError(f"{name}: target is not regular non-symlink")
        if oct(stat.S_IMODE(target_stat.st_mode)) != "0o644":
            raise AssertionError(f"{name}: target mode is not 0644")
        if target.read_bytes() != candidate.read_bytes():
            raise AssertionError(f"{name}: current target differs from accepted candidate")
        if backup.read_bytes() != candidate.read_bytes()[: record["preimage_bytes"]]:
            raise AssertionError(f"{name}: backup is not candidate prefix")
        target_results[name] = {
            "target_sha256": sha_path(target),
            "candidate_sha256": sha_path(candidate),
            "backup_sha256": sha_path(backup),
            "target_equals_candidate": True,
            "backup_equals_declared_preimage": sha_path(backup) == record["preimage_sha256"],
            "mode": oct(stat.S_IMODE(target_stat.st_mode)),
        }

    installer_sampler_unknown = review_manifest["installer_disk_monitor_custody"]
    if any(
        installer_sampler_unknown[key] != "UNOBSERVABLE_FROM_RETAINED_INSTALLER_ARTIFACTS"
        for key in ("pid", "exit_code", "wait", "reap")
    ):
        raise AssertionError("installer sampler lifecycle was incorrectly qualified")

    output = {
        "schema": "timeline.d141.final-unit-notes-custody-return-comparison/v1",
        "task": "rt-F-D141-final-unit-notes-custody-return-1015",
        "inputs": {
            "installer_installation": str(installer_installation_path),
            "installer_installation_sha256": sha_path(installer_installation_path),
            "installer_source_manifest": str(installer_manifest_path),
            "installer_source_manifest_sha256": sha_path(installer_manifest_path),
            "independent_review": str(review_path),
            "independent_review_sha256": sha_path(review_path),
            "independent_review_source_manifest": str(review_manifest_path),
            "independent_review_source_manifest_sha256": sha_path(review_manifest_path),
            "placement_install_source_manifest": str(placement_manifest_path),
            "placement_install_source_manifest_sha256": sha_path(placement_manifest_path),
            "placement_review_source_manifest": str(PLACEMENT_REVIEW),
            "placement_review_source_manifest_sha256": sha_path(PLACEMENT_REVIEW),
        },
        "algorithm": {
            "current_map": "final-unit installer/review outside_inventory: os.walk(followlinks=False), symlink directories pruned, target basenames excluded, regular non-symlink lstat entries mapped to bytes/mode/sha256",
            "earlier_aggregate": "placement installer inventory map: sorted os.walk entries, target paths excluded, mode/regular/symlink/sha256 item fields, sha256(json.dumps(map, sort_keys=True, separators=(',', ':')))",
            "no_render_invoked": True,
        },
        "current_exact_content": {
            "outside_count": len(current),
            "current_map_sha256": canonical_map_sha(current),
            "matches_independent_review_current_map": current == review_current,
            "matches_installer_serialized_after_map": current == installer_after,
            "canonical_targets": target_results,
            "retained_render_receipt": {
                "source": str(review_path),
                "function_only": review["render"]["function_only"],
                "caller_sha256": review["render"]["caller_sha256"],
                "placeholders_resolved": review["render"]["placeholders_resolved"],
                "balanced_fences": review["render"]["balanced_fences"],
                "id_entry_count": review["render"]["id_entry_count"],
                "disclosure_occurrences": review["render"]["disclosure_occurrences"],
                "rerendered_by_this_script": False,
            },
        },
        "separate_earlier_to_current_interval": {
            "status": "QUALIFIED_AGGREGATE_ONLY",
            "earlier_receipt": str(PLACEMENT_REVIEW),
            "earlier_observation_scope": "independent placement review 0258; after the earlier placement-note installation and before the final-unit installation",
            "earlier_count": placement_expected["count"],
            "earlier_aggregate_sha256": placement_expected["sha256"],
            "current_reproduced_count": len(placement_current),
            "current_reproduced_aggregate_sha256": placement_aggregate,
            "aggregate_equal": placement_aggregate == placement_expected["sha256"],
            "not_immediate_pre_cas_evidence": True,
            "transient_changes_absence_inferred": False,
        },
        "historical_custody": {
            "status": "NOT_RECOVERABLE",
            "genuine_immediate_pre_cas_568_map": "UNKNOWN",
            "genuine_pre_post_conservation": "UNKNOWN",
            "missing_facts": [
                "The installer pre-mutation 568-item map was not durably serialized before the final-unit CAS.",
                "The retained installer before map was populated by the read-only follow-up from current bytes and is not historical pre-CAS evidence.",
                "The original installer sampler PID, exit code, wait result, and reap fact were not retained.",
            ],
            "review_sampler_is_not_installer_lifecycle": True,
        },
        "disposition": "QUALIFIED_CURRENT_CONTENT_WITH_CUSTODY_LIMIT; HISTORICAL_IMMEDIATE_PRE_CAS_CUSTODY_NOT_RECOVERABLE",
    }
    output["script_sha256"] = sha_path(Path(__file__))
    json.dump(output, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
