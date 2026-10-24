#!/usr/bin/env python3
"""Lossless, read-only D54a classification of the retained service XML."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
INPUT = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
    "/scratchpad/orch/workers/agt-F-core-rehearsal-2234/evidence"
)
XML = INPUT / "OWN-REHEARSAL-SUITE.xml"
SERVICE_LOG = INPUT / "service-log.txt"
SERVICE_SUMMARY = INPUT / "service-summary"
OUT = ROOT / "evidence"

BOARD = Path("/home/user/timeline-hub/hub/design/BOARD-HEADER.md")
HELD = Path("/home/user/timeline-hub/hub/design/agt-F-core-held-inputs-1338.md")
D23 = Path("/home/user/timeline-hub/hub/design/agent-G5-D23-publisher-audit-1416.md")
STATUS = Path("/home/user/timeline-hub/hub/status/agent.md")


def node_id(testcase: ElementTree.Element) -> str:
    return f"{testcase.attrib['classname']}::{testcase.attrib['name']}"


def trace(testcase: ElementTree.Element) -> str:
    failure = next(child for child in testcase if child.tag == "failure")
    return f"{failure.attrib.get('message', '')}\n{failure.text or ''}"


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def owner_family(test: str, body: str) -> tuple[str, str]:
    if any(key in body for key in ("FileNotFoundError", "unsupported loader/interpreter")):
        return "environment", "rehearsal-toolchain-launch"
    if "effects.generated.ts" in body:
        return "environment", "render-registry-provisioning"
    if "test_d13_installed_native_preflight" in test:
        return "Runtime", "d13-installed-tuple"
    if "native_word_anchor" in test or "word_binding_recipe" in test:
        return "Agent", "native-word-binding"
    if "timing_retained_inputs" in test or "timeline_helper_capture" in test:
        return "Agent", "relational-timing-capture"
    if "native_batch_ingress" in test:
        return "Agent", "native-batch-ingress"
    if "commit_runtime_" in test or "native_sheet_current_runtime" in test:
        return "Runtime", slug(test.split("::", 1)[0].split(".")[-1])
    if "historical_shared_redo_authority" in test:
        return "Runtime", "historical-redo-authority"
    if "owned_move_publish_runtime" in test or "prepared_video_birth" in test:
        return "Runtime", "commit-rebase-custody"
    if "test_wc6_completion_capture" in test:
        return "Agent", "wc6-completion-capture"
    if "test_timeline_commit_provider" in test or "semantic_reservations" in test:
        return "Agent", "commit-provider-custody"
    if "test_timeline_selected_schema_runtime" in test:
        return "Runtime", "selected-schema-inverse"
    if "test_timeline_commit_graph_roots" in test:
        return "Runtime", "semantic-history-authority"
    if "packs.timeline" in test:
        return "Agent", "cli-document-commit"
    if "test_authoring_media" in test or "doc_patch" in test:
        return "Agent", "document-patch-emitter"
    if "packs.video_editing" in test:
        return "Runtime", "publication-route"
    if "packs.rendering" in test or "scene_real_public" in test:
        return "Rendering", "rendering-adapter"
    if "test_host_bootstrap_source_identity" in test:
        return "environment", "remotion-host-bootstrap"
    module = test.split("::", 1)[0].split(".")[-1]
    return "Agent", slug(module)


def classify(test: str, body: str) -> tuple[str, str, str, str, str]:
    # These are exact named exceptions, never inferred from a matching word.
    if test == (
        "tests.sdk.test_timeline_helper_capture::"
        'test_cut_nudge_restart_merges_other_cut["second"]'
    ):
        return (
            "deferred",
            "DEFERRED",
            "Agent",
            "d23-relational-timing",
            "D23 exact selector: child-on-second word binding remains visibly deferred; no automatic relational timing.",
        )
    if test == "tests.packs.video_editing.test_runtime_publication_chain::test_d13_installed_native_preflight":
        return (
            "env",
            "ENV",
            "Runtime",
            "d13-installed-tuple",
            "D67 exact D13 environment gap: the approved installed source/profile/binding/tool tuple was not supplied; the unchanged preflight reports the named missing inputs.",
        )
    if test == "tests.editing_conformance.test_p4_ten_note_v2_runtime::test_http_ten_note_commit_per_step_inverse_and_redo":
        return (
            "core",
            "KNOWN-P4-TEN-NOTE",
            "Runtime",
            "p4-ten-note-history-cost",
            "Known P4 ten-note record retained separately; exact 45-second timeout is not reclassified as a generic regression or environment cause.",
        )

    if "FileNotFoundError" in body and any(
        token in body for token in ("'node'", "'ffmpeg'", "'ffprobe'")
    ):
        return (
            "env",
            "ENV",
            "environment",
            "rehearsal-missing-executable",
            "Authentic service traceback stops at a missing executable before the promised assertion; this is an exact service-environment observation, not a product diagnosis.",
        )
    if "unsupported loader/interpreter overrides" in body:
        return (
            "env",
            "ENV",
            "environment",
            "rehearsal-launch-overrides",
            "Authentic service traceback stops in Remotion launch validation on forbidden loader/interpreter overrides; no test body reaches its product assertion.",
        )
    if "effects.generated.ts" in body and "required" in body:
        return (
            "env",
            "ENV",
            "environment",
            "render-registry-provisioning",
            "Authentic service assertion reports the pinned generated registry file absent; this is setup/provisioning evidence, not a dead behavior claim.",
        )

    owner, family = owner_family(test, body)
    return (
        "core",
        "CORE-OPEN",
        owner,
        family,
        "Current promised behavior failed in the authentic rehearsal, but no exact upstream PASS, approved D52/D72 dead-scope ledger entry, or named deferral applies; causal explanation remains unproved and the row stays open.",
    )


def main() -> None:
    root = ElementTree.parse(XML).getroot()
    all_cases = list(root.iter("testcase"))
    failures = [case for case in all_cases if any(c.tag == "failure" for c in case)]
    errors = [case for case in all_cases if any(c.tag == "error" for c in case)]
    ids = [node_id(case) for case in failures]
    if len(ids) != 308 or len(set(ids)) != 308:
        raise SystemExit(f"expected 308 unique failures, got {len(ids)} / {len(set(ids))}")
    if len(errors) != 242:
        raise SystemExit(f"expected 242 excluded errors, got {len(errors)}")

    rows: list[dict[str, str]] = []
    for case in failures:
        test = node_id(case)
        body = trace(case)
        classification, disposition, owner, family, reason = classify(test, body)
        refs = [f"{XML}::{test}", f"{SERVICE_LOG}::{family}", str(BOARD)]
        if classification == "deferred":
            refs.extend((str(HELD), str(D23)))
        elif classification == "env" and family == "d13-installed-tuple":
            refs.extend((str(HELD), str(STATUS)))
        elif disposition == "KNOWN-P4-TEN-NOTE":
            refs.extend((str(STATUS), str(SERVICE_SUMMARY)))
        rows.append(
            {
                "node": test,
                "status": "failed",
                "scope": "core",
                "classification": classification,
                "disposition": disposition,
                "owner": owner,
                "family": family,
                "reason": reason,
                "evidence": ";".join(refs),
            }
        )

    output_ids = [row["node"] for row in rows]
    if output_ids != ids:
        raise SystemExit("classified order/set does not equal XML failure order/set")

    TSV = OUT / "d54a-failures.tsv"
    JSON = OUT / "d54a-failures.json"
    COUNTS = OUT / "d54a-failure-counts.txt"
    fields = list(rows[0])
    with TSV.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    category_counts = Counter(row["classification"] for row in rows)
    disposition_counts = Counter(row["disposition"] for row in rows)
    family_counts = Counter(f"{row['owner']}::{row['family']}" for row in rows)
    duplicates = Counter(output_ids)
    duplicate_rows = {key: value for key, value in duplicates.items() if value > 1}
    payload = {
        "schema": "timeline.agent.d54a.failure-classification.v1",
        "task": "agt-F-rehearsal-failures-2305",
        "read_only_classification": True,
        "source": {
            "service": "agent-OWN-REHEARSAL-SUITE-1024224113-23499",
            "xml": str(XML),
            "xml_sha256": hashlib.sha256(XML.read_bytes()).hexdigest(),
            "service_log": str(SERVICE_LOG),
            "service_log_sha256": hashlib.sha256(SERVICE_LOG.read_bytes()).hexdigest(),
            "summary": str(SERVICE_SUMMARY),
            "result": "8713 passed, 308 failed, 242 errors, 86 warnings, 173 subtests",
        },
        "membership": {
            "assigned_status": "failure",
            "assigned_total": 308,
            "classified_total": len(rows),
            "excluded_error_total": len(errors),
            "duplicate_testcase_ids": duplicate_rows,
        },
        "counts": {
            "classification": dict(sorted(category_counts.items())),
            "disposition": dict(sorted(disposition_counts.items())),
            "families": dict(sorted(family_counts.items())),
        },
        "rules": {
            "regression": "not claimed without exact upstream PASS for the same selector and current FAIL",
            "pre_existing": "not claimed from an unexplained or merely similar failure",
            "dead_scope": "not claimed from a retired-interface error without exact ledger plus replacement behavior evidence",
            "core_open": "current promised behavior with no applicable named env/defer/dead decision remains CORE-OPEN",
            "d23": "only the exact named child-on-second selector is deferred",
            "d13": "only the exact named installed-native-preflight selector uses D67 environment disposition",
        },
        "rows": rows,
    }
    JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    with COUNTS.open("w") as stream:
        stream.write("source_result=8713 passed, 308 failed, 242 errors, 86 warnings, 173 subtests\n")
        stream.write("assigned_failure_records=308\n")
        stream.write("classified_failure_records=308\n")
        stream.write("excluded_error_records=242\n")
        stream.write("duplicate_testcase_ids=0\n")
        for key, value in sorted(category_counts.items()):
            stream.write(f"classification.{key}={value}\n")
        for key, value in sorted(disposition_counts.items()):
            stream.write(f"disposition.{key}={value}\n")
        stream.write("regression=0\npre_existing=0\ndead_scope=0\n")
        stream.write("teardown_outcome_duplicates=0\n")
        stream.write("note=known P4 ten-note is retained separately from ordinary CORE-OPEN rows\n")


if __name__ == "__main__":
    main()
