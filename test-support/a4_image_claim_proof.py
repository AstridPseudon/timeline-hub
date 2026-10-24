"""Offline causal proof for the saved A4 image boundary.

This reads only the worker's retained source-bound evidence, replays the
registered Agent provider against that exact canonical document, and invokes
Runtime's claim validator.  It does not call a service or write a realm.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_auth import validate_claims

from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document

CORE_FIELDS = ("schema_version", "op", "version", "select", "args")


def load(root: Path, name: str) -> Any:
    return json.loads((root / name).read_text(encoding="utf-8"))


def digest_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field_map(submitted: dict[str, Any], recorded: dict[str, Any]) -> dict[str, Any]:
    return {
        key: {
            "submitted": submitted.get(key),
            "recorded": recorded.get(key),
            "equal": submitted.get(key) == recorded.get(key),
        }
        for key in CORE_FIELDS
    } | {
        "created": {
            "submitted": submitted.get("created", []),
            "recorded": recorded.get("created", []),
            "equal": submitted.get("created", []) == recorded.get("created", []),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    root = args.evidence
    app_output = load(root, "app-output.json")
    source = load(root, "runtime-source-facts.json")
    producer = load(root, "producer-input.json")
    request = app_output["request"]
    submitted = request["commands"][0]
    plan = execute(
        bundle_from_document(producer["canonicalDocument"]),
        request["commands"],
        verified_media=[source["verified_media"]],
        commit_request=request,
        evaluated_head={
            "revision_id": request["base_revision_id"],
            "publication_id": request["base_publication_id"],
        },
    )
    recorded = plan.records[0]["command"]
    failure: dict[str, Any] | None = None
    try:
        validate_claims(request, {"commands": plan.records})
    except CommitRejected as exc:
        failure = exc.failure
    if failure is None:
        raise AssertionError("Runtime claim validation unexpectedly accepted the saved boundary")

    output = {
        "source": {
            "agent_commit": source["agent_commit"],
            "runtime_commit": source["runtime_commit"],
            "app_source_commit": source["app_source_commit"],
            "input_sha256": source["input_sha256"],
            "input_file_sha256": digest_bytes(root / "producer-input.json"),
            "output_file_sha256": digest_bytes(root / "app-output.json"),
        },
        "command": field_map(submitted, recorded),
        "provider_metadata": {
            "recorded_claim_keys": sorted(set(recorded) - set(CORE_FIELDS)),
            "created_refs": recorded["created"],
        },
        "steps": {
            "submitted": request["steps"][0],
            "recorded": plan.steps[0],
            "recorded_patch_paths": [
                {"ref": item["ref"], "path": item["path"]}
                for item in plan.steps[0]["patch"]
            ],
            "recorded_dependency_count": len(plan.steps[0]["dependencies"]),
        },
        "runtime_validation": {
            "code": failure["code"],
            "message": failure["message"],
            "reason": failure["details"]["reason"],
        },
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
