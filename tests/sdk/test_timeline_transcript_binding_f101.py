"""Pure F101 dependency checks; no publisher/command integration is claimed."""
import copy
import hashlib
import json

import pytest

from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.transcript_binding import bound_source_words


def source():
    content = dict(
        schema_version=1,
        subject=dict(media_object_id="synthetic-media", media_sha256="1" * 64),
        source=dict(producer_id="synthetic-test", source_id="synthetic-take-A",
                    lineage_id="synthetic-lineage-A", revision_id="synthetic-revision-A",
                    producer_digest="2" * 64),
        clock=dict(kind="media", unit="seconds", origin_seconds=0),
        words=[dict(id="opaque-alpha", text="again", start_s=.25, end_s=.5),
               dict(id="opaque-beta", text="again", start_s=.625, end_s=1.125)],
        segments=[dict(id="segment-A", word_ids=["opaque-alpha", "opaque-beta"])],
        metadata=dict(synthetic=True),
    )
    return content


def pinned(content=None):
    content = source() if content is None else content
    # These bytes are fixture-owned; production hashing/serialization is D's job.
    raw = json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                     allow_nan=False).encode()
    digest = hashlib.sha256(raw).hexdigest()
    reference = dict(schema_version=1, document=dict(id="synthetic-document", version=3,
                     content_digest="sha256:" + digest),
                     snapshot=dict(object_id="sha256:" + digest, sha256=digest),
                     **{key: copy.deepcopy(content[key]) for key in ("subject", "source", "clock")})
    binding = dict(copy.deepcopy(reference), occurrence_id="occ-A", word_ids=["opaque-beta"])
    return binding, reference, raw


def selected(binding, reference, raw, occurrence="occ-A"):
    return bound_source_words(binding, frozen_reference=reference, snapshot_bytes=raw,
                              occurrence_id=occurrence)


def test_frozen_selection_preserves_source_identity_and_seconds_without_mutation():
    binding, reference, raw = pinned()
    before = copy.deepcopy((binding, reference, raw))
    result = selected(binding, reference, raw)
    assert result == (source()["words"][1],)
    assert (binding, reference, raw) == before
    result[0]["id"] = "caller-mutated"
    assert selected(binding, reference, raw)[0]["id"] == "opaque-beta"


def test_one_snapshot_serves_two_occurrences_without_retiming_or_reminting():
    binding, reference, raw = pinned()
    other = dict(binding, occurrence_id="occ-B")
    assert selected(binding, reference, raw) == selected(other, reference, raw, "occ-B")
    assert selected(other, reference, raw, "occ-B")[0]["start_s"] == .625
    with pytest.raises(TimelineEditError, match="occurrence"):
        selected(other, reference, raw)


def test_segmentation_is_not_word_identity():
    content = source()
    before = selected(*pinned(content))
    content["segments"] = [dict(id="changed-A", word_ids=["opaque-alpha"]),
                           dict(id="changed-B", word_ids=["opaque-beta"])]
    after = selected(*pinned(content))
    assert before == after


@pytest.mark.parametrize("path,value", [
    (("document", "id"), "different-document"),
    (("document", "version"), 4),
    (("document", "content_digest"), "3" * 64),
    (("snapshot", "object_id"), "different-object"),
    (("snapshot", "sha256"), "3" * 64),
    (("subject", "media_object_id"), "other-media"),
    (("subject", "media_sha256"), "3" * 64),
    (("source", "producer_id"), "other-producer"),
    (("source", "source_id"), "other-take"),
    (("source", "lineage_id"), "other-lineage"),
    (("source", "revision_id"), "other-revision"),
    (("source", "producer_digest"), "3" * 64),
    (("clock", "unit"), "frames"),
])
def test_every_immutable_pin_must_match_accepted_history(path, value):
    binding, reference, raw = pinned()
    binding[path[0]][path[1]] = value
    with pytest.raises(TimelineEditError, match="frozen dependency"):
        selected(binding, reference, raw)


@pytest.mark.parametrize("missing", [None, {}, {"schema_version": 1}])
def test_missing_dependency_refuses_without_discovery(missing):
    binding, _, raw = pinned()
    with pytest.raises(TimelineEditError):
        selected(binding, missing, raw)


@pytest.mark.parametrize("raw", [None, b"", b"{}", b"different bytes"])
def test_missing_or_corrupt_bytes_refuse(raw):
    binding, reference, _ = pinned()
    with pytest.raises(TimelineEditError):
        selected(binding, reference, raw)


@pytest.mark.parametrize("name", ["subject", "source", "clock"])
def test_hash_valid_snapshot_with_wrong_identity_refuses(name):
    binding, reference, _ = pinned()
    content = source()
    field = dict(subject="media_object_id", source="source_id", clock="unit")[name]
    content[name][field] = "different"
    _, actual, raw = pinned(content)
    for key in ("document", "snapshot"):
        binding[key] = copy.deepcopy(actual[key])
        reference[key] = copy.deepcopy(actual[key])
    with pytest.raises(TimelineEditError, match=f"snapshot {name}"):
        selected(binding, reference, raw)


@pytest.mark.parametrize("ids", [["again"], ["segment-A"], ["opaque-beta", "opaque-beta"],
                                ["opaque-beta", "opaque-alpha"], ["missing"], [False], [{}]])
def test_selection_never_uses_text_segment_ordinal_or_nearest_time(ids):
    binding, reference, raw = pinned()
    binding["word_ids"] = ids
    with pytest.raises(TimelineEditError):
        selected(binding, reference, raw)


def test_empty_selection_and_explicit_empty_source():
    content = source()
    content.update(words=[], segments=[])
    binding, reference, raw = pinned(content)
    binding["word_ids"] = []
    assert selected(binding, reference, raw) == ()


@pytest.mark.parametrize("change", ["duplicate-id", "no-id", "untimed", "negative", "backward",
                                  "boolean", "infinite"])
def test_invalid_source_words_cannot_supply_identity_or_seconds(change):
    content = source()
    row = content["words"][1]
    if change == "duplicate-id":
        row["id"] = content["words"][0]["id"]
    elif change == "no-id":
        del row["id"]
    elif change == "untimed":
        del row["start_s"]
    else:
        row["start_s"] = dict(negative=-1, backward=2, boolean=True, infinite=float("inf"))[change]
    # Infinity is invalid JSON; exercise the decoder boundary with exact pinned bytes.
    if change == "infinite":
        content["words"][1]["start_s"] = 1e308
        binding, reference, raw = pinned(content)
        raw = raw.replace(b"1e+308", b"1e+999")
        digest = hashlib.sha256(raw).hexdigest()
        for pin in (binding, reference):
            pin["snapshot"].update(sha256=digest, object_id="sha256:" + digest)
            pin["document"]["content_digest"] = "sha256:" + digest
    else:
        binding, reference, raw = pinned(content)
    with pytest.raises(TimelineEditError):
        selected(binding, reference, raw)


def test_accepted_snapshot_is_self_contained_when_document_advances():
    binding, reference, raw = pinned()
    changed = source()
    changed["source"]["revision_id"] = "later-revision"
    changed["words"][1].update(id="different-word", text="again", start_s=.7)
    _, _, later = pinned(changed)
    assert selected(binding, reference, raw)[0]["id"] == "opaque-beta"
    with pytest.raises(TimelineEditError, match="digest mismatch"):
        selected(binding, reference, later)


def test_duplicate_json_keys_refuse_even_with_matching_digest():
    binding, reference, raw = pinned()
    raw = raw.replace(b'"schema_version":1', b'"schema_version":1,"schema_version":1')
    digest = hashlib.sha256(raw).hexdigest()
    for pin in (binding, reference):
        pin["snapshot"].update(sha256=digest, object_id="sha256:" + digest)
        pin["document"]["content_digest"] = "sha256:" + digest
    with pytest.raises(TimelineEditError, match="duplicate JSON key"):
        selected(binding, reference, raw)


@pytest.mark.parametrize("target", ["binding", "dependency", "snapshot"])
def test_boolean_schema_version_is_not_version_one(target):
    if target == "snapshot":
        content = source()
        content["schema_version"] = True
        binding, reference, raw = pinned(content)
    else:
        binding, reference, raw = pinned()
        (binding if target == "binding" else reference)["schema_version"] = True
    with pytest.raises(TimelineEditError, match="schema_version"):
        selected(binding, reference, raw)


def test_dependency_version_requires_exact_type_not_boolean_equality():
    binding, reference, raw = pinned()
    binding["document"]["version"] = 1
    reference["document"]["version"] = True
    with pytest.raises(TimelineEditError, match="frozen dependency"):
        selected(binding, reference, raw)


def test_hash_valid_snapshot_cannot_use_boolean_origin():
    content = source()
    content["clock"]["origin_seconds"] = False
    binding, reference, raw = pinned(content)
    for pin in (binding, reference):
        pin["clock"]["origin_seconds"] = 0
    with pytest.raises(TimelineEditError, match="media-seconds"):
        selected(binding, reference, raw)
