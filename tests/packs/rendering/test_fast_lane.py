"""Unit-level fast-lane timing and snapshot provenance checks."""

from __future__ import annotations

import os
import time

from astrid.core import gateway
from astrid.packs.rendering.actions.timeline_visualize.inspection_contract import render_status
from astrid.packs.rendering.actions.timeline_visualize.provenance import snapshot_label


def _snapshot(parent: str | None, *, selection: str = "explicit_historical_render", **metadata):
    canonical = {}
    if parent is not None:
        canonical["parent_revision_id"] = parent
    return {
        "metadata": {
            "selection": selection,
            "canonical_timeline": canonical,
            **metadata,
        }
    }


def test_gateway_main_stamps_the_cli_start_for_the_check_timing(monkeypatch):
    monkeypatch.delenv("ASTRID_CLI_START_MONO", raising=False)
    before = time.monotonic()
    assert gateway.main(["--version"]) == 0
    stamp = float(os.environ.pop("ASTRID_CLI_START_MONO"))
    assert stamp <= time.monotonic()
    # The first call stamps the gateway import; it is never later than this test's start by a wide margin.
    assert stamp <= before + 1.0


def test_historical_snapshot_label_uses_the_revision_actually_rendered():
    label = snapshot_label(_snapshot("R1", requested_revision_id="R2", current_head_revision_id="R2"))

    assert label == {
        "status": "committed",
        "label": "committed revision R1",
        "actual_revision_id": "R1",
        "base_revision_id": None,
    }


def test_candidate_label_is_unsaved_and_keeps_its_committed_parent():
    label = snapshot_label(
        _snapshot("R1", selection="explicit_candidate_preview", requested_revision_id="R2")
    )

    assert label == {
        "status": "candidate",
        "label": "unsaved candidate based on committed revision R1",
        "actual_revision_id": None,
        "base_revision_id": "R1",
    }


def test_requested_revision_without_actual_snapshot_identity_is_unavailable():
    label = snapshot_label(_snapshot(None, requested_revision_id="R2"))

    assert label["status"] == "unavailable"
    assert label["actual_revision_id"] is None
    assert "R2" not in label["label"]


def test_no_cache_has_no_revision_label():
    label = snapshot_label(None)

    assert label == {
        "status": "unavailable",
        "label": "revision unavailable",
        "actual_revision_id": None,
        "base_revision_id": None,
    }


def test_mismatched_requested_revision_cannot_relabel_actual_snapshot():
    snapshot = _snapshot(
        "R1",
        capture_authority={"parent_revision_id": "R1"},
        requested_revision_id="R2",
    )

    assert snapshot_label(snapshot)["label"] == "committed revision R1"


def test_renderer_outage_status_says_output_is_unavailable():
    status = render_status(lifecycle="absent", output={"timeline": "cut"}, project="demo")

    assert status["kind"] == "absent"
    assert "No successful render is available" in status["label"]
    assert status["output"]["available"] is False
