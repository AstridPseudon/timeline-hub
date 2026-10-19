"""Main's ownership/storage and transcript rules that the recipe must preserve."""
from __future__ import annotations

import copy
import runpy
from pathlib import Path

from astrid.core.timeline.authoring_bundle import (
    compile_authoring_candidate,
    open_authoring_bundle,
)
from astrid.sdk.media_transcript import build_transcript, transcript_document_id
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline_restructure import assert_equivalent, flatten, split

REPO = Path(__file__).resolve().parents[2]


def test_shared_source_occurrence_isolation_and_stable_materialization():
    # Reuse main's actual closure fixture, including opaque fields and shot-item
    # references. Do not replace authoring_bundle with a miniature graph model.
    fixture = runpy.run_path(str(REPO / "tests/timeline/test_authoring_bundle.py"))
    parent, shots, internals = fixture["_closure"](shared=True)
    original = copy.deepcopy((parent, shots, internals))
    bundle = open_authoring_bundle(parent, shot_revisions=shots,
                                    internal_timeline_revisions=internals)
    first, second = [row["shot_id"] for row in bundle["placements"]]
    assert first != second
    sibling = copy.deepcopy(bundle["shots"][second])
    bundle["shots"][first]["payload"]["metadata"]["settings"] = None
    one, two = compile_authoring_candidate(bundle), compile_authoring_candidate(bundle)
    assert one.as_dict() == two.as_dict()
    assert bundle["shots"][second] == sibling
    assert (parent, shots, internals) == original
    changed = {row["shot_id"]: row for row in one.publication["shot_revisions"]}
    assert changed[first]["payload"]["metadata"]["settings"] is None
    assert changed[second]["payload"]["metadata"]["settings"] == {"look": "warm"}
    # Shared intent must explicitly fan out over these independent authored
    # owners. Mutating one owner cannot implement a shared-source operation.


def test_chapters_as_shots_roundtrip_retains_parent_music_and_crossing_clip():
    fixture = runpy.run_path(str(REPO / "tests/sdk/test_timeline_restructure.py"))
    original = fixture["flat_film"]()
    stored = split(original)
    assert len(stored["placements"]) == 3
    parent_ids = {clip["id"] for clip in stored["parent"]["clips"]}
    assert {"bed", "cross"} <= parent_ids
    assert all("bed" not in {c["id"] for c in stored["shots"][row["shot_id"]]["internal_timeline"]["clips"]}
               for row in stored["placements"])
    flat = flatten(fixture["published"](stored))
    assert_equivalent(original, stored)
    assert_equivalent(original, flat)
    tl = Checkout(fixture["published"](stored))
    tl.clip("inside").data["params"]["opaque"] = None
    republished = tl.stored_document()
    assert len(republished["placements"]) == 3
    assert {c["id"] for c in republished["parent"]["clips"]} >= {"bed", "cross"}
    found = [c for row in republished["placements"]
             for c in republished["shots"][row["shot_id"]]["internal_timeline"]["clips"] if c["id"] == "inside"]
    assert len(found) == 1 and found[0]["params"]["opaque"] is None


def test_main_transcript_source_and_word_identity_are_distinct_dependencies():
    media = "sha256:" + "1" * 64
    words = [[.25, .5, "again"], [.75, 1., "again"]]
    first = build_transcript(media, "line", "again again", words)
    ids = [word["id"] for word in first["segments"][0]["words"]]
    assert len(set(ids)) == 2
    assert build_transcript(media, "line", "again again", words) == first
    second = build_transcript(media, "line", "again again", words, source_id="other")
    assert [w["id"] for w in second["segments"][0]["words"]] == ids
    assert transcript_document_id("p", media, first["source_id"]) != transcript_document_id("p", media, second["source_id"])
    moved = build_transcript(media, "line", "again again", [[.3, .5, "again"], words[1]])
    assert moved["segments"][0]["words"][0]["id"] != ids[0]
    # GAP: main's generated word ID includes timing, and source is external to
    # that ID. An anchor must pin document/source/version as well as word ID;
    # retiming is not proof of source-word continuity.
