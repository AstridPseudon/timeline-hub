"""Private setup for the genuine-audio public journey fixture.

The captured ``film`` timeline is retained as historical evidence.  This
helper adds a sibling publication to the caller-owned realm before the
journey captures its head, receipt, and event baseline.  Only the source CAS
pin changes; the authored closure remains byte-for-byte the captured closure.
"""

from __future__ import annotations

import copy
import io
import wave
from pathlib import Path
from types import SimpleNamespace

from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_baseline import verify_baseline
from timeline_commit_film_fixture import FilmFixture


_TIMELINE_ID = "historical-audio-pcm"
_SEED_PARENT_REVISION_ID = "historical-audio-pcm-parent-v1"
_PARENT_REVISION_ID = "historical-audio-pcm-parent-v2"
_AUDIO_NAME = "music-bed.wav"
_AUDIO_IDEMPOTENCY_KEY = "historical-audio-pcm-source"
_SEED_PUBLICATION_IDEMPOTENCY_KEY = "historical-audio-pcm-publication-v1"
_PUBLICATION_IDEMPOTENCY_KEY = "historical-audio-pcm-publication-v2"
_MALFORMED_AUDIO = b"synthetic-music-bed"


def _pcm_wav() -> bytes:
    """Return six seconds of genuine mono 8 kHz, 16-bit PCM audio."""
    stream = io.BytesIO()
    with wave.open(stream, "wb") as output:
        output.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
        output.writeframes(b"\x00\x00" * 48000)
    return stream.getvalue()


def assert_malformed_audio_metadata_unavailable(tmp_path: Path) -> None:
    """Keep the captured 19-byte control visibly unknown to Main's reader.

    The control is a temporary local input only: it is not ingested, attached
    to a timeline, accepted, or left as a draft.  ``media_seconds`` is Main's
    existing raw-media duration helper and reports ``None`` for this input.
    """
    from astrid.sdk.timeline.store import media_seconds

    tmp_path.mkdir(parents=True, exist_ok=True)
    malformed = tmp_path / "historical-audio-malformed19.bin"
    malformed.write_bytes(_MALFORMED_AUDIO)
    try:
        assert media_seconds("", malformed) is None
    finally:
        malformed.unlink(missing_ok=True)
    assert not malformed.exists()


def _cloned_parent_body(canonical: dict, *, project_id: str, audio_id: str) -> dict:
    old_parent = canonical["parent_revision"]["payload"]
    old_audio_id = old_parent["registry"]["assets"]["music-bed"]["object_id"]
    parent = copy.deepcopy(old_parent)
    parent["registry"]["assets"]["music-bed"]["object_id"] = audio_id
    assert "duration" not in parent["registry"]["assets"]["music-bed"]

    # ``documents`` is a read-side closure field, not an accepted publication
    # input.  Runtime derives the child closure and normalizes its media pins.
    manifest = {
        key: copy.deepcopy(canonical["dependency_manifest"][key])
        for key in ("shots", "internal_timelines", "media")
    }
    for item in manifest["media"]:
        if item["media_id"] == old_audio_id:
            item["media_id"] = audio_id
            item["content_digest"] = audio_id

    return {
        "project_id": project_id,
        "timeline_id": _TIMELINE_ID,
        "expected_head": None,
        "parent_revision_id": _SEED_PARENT_REVISION_ID,
        "internal_timeline_revisions": copy.deepcopy(
            canonical["internal_timeline_revisions"]
        ),
        "shot_revisions": copy.deepcopy(canonical["shot_revisions"]),
        "parent_composition": parent,
        "dependency_manifest": manifest,
    }


def prepare_pcm_historical_audio_film(film, tmp_path):
    """Seed and read back a genuine audio sibling before journey capture."""
    assert_malformed_audio_metadata_unavailable(tmp_path)
    audio_bytes = _pcm_wav()
    prepared = None

    for root in (film.fixture.source_root, film.fixture.duplicate_root):
        service = RuntimeService(root)
        try:
            old_baseline = verify_baseline(
                service.store.conn,
                film.fixture.project_id,
                film.fixture.timeline_id,
                read_object=service.cas.read,
            )
            old_document = copy.deepcopy(old_baseline["canonical_document"])
            audio = service.ingest(
                film.fixture.project_id,
                audio_bytes,
                media_type="audio/wav",
                original_name=_AUDIO_NAME,
                idempotency_key=_AUDIO_IDEMPOTENCY_KEY,
            )
            audio_id = audio["data"]["object_id"]
            service.create_timeline(
                film.fixture.project_id,
                _TIMELINE_ID,
                idempotency_key=f"{_TIMELINE_ID}-create",
            )
            body = _cloned_parent_body(
                old_document,
                project_id=film.fixture.project_id,
                audio_id=audio_id,
            )
            service.publish_parent_composition(
                film.fixture.project_id,
                _TIMELINE_ID,
                body,
                idempotency_key=_SEED_PUBLICATION_IDEMPOTENCY_KEY,
            )
            second_body = copy.deepcopy(body)
            second_body["expected_head"] = _SEED_PARENT_REVISION_ID
            second_body["parent_revision_id"] = _PARENT_REVISION_ID
            publication = service.publish_parent_composition(
                film.fixture.project_id,
                _TIMELINE_ID,
                second_body,
                idempotency_key=_PUBLICATION_IDEMPOTENCY_KEY,
            )

            sibling = verify_baseline(
                service.store.conn,
                film.fixture.project_id,
                _TIMELINE_ID,
                read_object=service.cas.read,
            )
            sibling_document = sibling["canonical_document"]
            expected_parent = copy.deepcopy(old_document["parent_revision"]["payload"])
            expected_parent["registry"]["assets"]["music-bed"]["object_id"] = audio_id
            assert sibling_document["parent_revision"]["payload"] == expected_parent
            assert sibling_document["shot_revisions"] == old_document["shot_revisions"]
            assert sibling_document["internal_timeline_revisions"] == old_document[
                "internal_timeline_revisions"
            ]
            expected_manifest = copy.deepcopy(old_document["dependency_manifest"])
            for item in expected_manifest["media"]:
                if item["media_id"] == old_document["parent_revision"]["payload"][
                    "registry"
                ]["assets"]["music-bed"]["object_id"]:
                    item["media_id"] = audio_id
                    item["content_digest"] = audio_id
            expected_manifest["media"].sort(key=lambda item: item["media_id"])
            assert sibling_document["dependency_manifest"] == expected_manifest
            assert "duration" not in sibling_document["parent_revision"]["payload"][
                "registry"
            ]["assets"]["music-bed"]
            assert service.object_location(film.fixture.project_id, audio_id)["verified"]
            assert service.cas.read(audio_id.removeprefix("sha256:")) == audio_bytes

            # The historical timeline's accepted history and closure remain
            # unchanged; setup only added the private sibling publication.
            assert verify_baseline(
                service.store.conn,
                film.fixture.project_id,
                film.fixture.timeline_id,
                read_object=service.cas.read,
            ) == old_baseline

            if root == film.fixture.duplicate_root:
                receipt = sibling["entries"][-1]["receipt"]
                prepared = SimpleNamespace(
                    fixture=FilmFixture(
                        source_root=film.fixture.source_root,
                        duplicate_root=film.fixture.duplicate_root,
                        project_id=film.fixture.project_id,
                        timeline_id=_TIMELINE_ID,
                        parent_revision_id=_PARENT_REVISION_ID,
                        media_ids=tuple(sorted({*film.fixture.media_ids, audio_id})),
                        transcript_document_id=film.fixture.transcript_document_id,
                        text_binding_id=film.fixture.text_binding_id,
                    ),
                    publication={"data": receipt["result"], "receipt": receipt},
                    original_events=[
                        tuple(row)
                        for row in service.store.conn.execute(
                            "SELECT * FROM timeline_events ORDER BY id"
                        )
                    ],
                )
        finally:
            service.close()

    assert prepared is not None
    return prepared
