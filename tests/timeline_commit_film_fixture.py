"""Small API-built film-shaped realm used by the publication baseline tests.

The source realm is built through ``RuntimeService`` and copied only after its
owner is closed.  Tests then open the copy, so a provenance failure cannot
change an original or an owner's realm.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore


@dataclass(frozen=True)
class FilmFixture:
    source_root: Path
    duplicate_root: Path
    project_id: str
    timeline_id: str
    parent_revision_id: str
    media_ids: tuple[str, ...]
    transcript_document_id: str
    text_binding_id: str


def _media(service: RuntimeService, project_id: str, data: bytes, name: str, media_type: str) -> str:
    return service.ingest(
        project_id,
        data,
        media_type=media_type,
        original_name=name,
        idempotency_key=f"film-media-{name}",
    )["data"]["object_id"]


def _transcript(media_id: str) -> dict:
    return {
        "schema": "media.transcript/v1",
        "media_id": media_id,
        "source_id": "edit-transcript-v1",
        "segments": [{
            "id": "segment-1",
            "start": 0.25,
            "end": 1.5,
            "text": "Open on the river",
            "speaker": "narrator",
            "words": [
                {"id": "word-1", "start": 0.25, "end": 0.7, "text": "Open"},
                {"id": "word-2", "start": 0.75, "end": 1.5, "text": "on the river"},
            ],
        }],
    }


def _binding_descriptor(binding: dict, text: str) -> dict:
    return {
        "binding_id": binding["binding_id"],
        "project_id": binding["project_id"],
        "shot_id": binding["shot_id"],
        "kind": binding["kind"],
        "slot": binding["slot"],
        "event_stream_id": binding["event_stream_id"],
        "head": binding["head"],
        "media_id": binding["media_id"],
        "content_hash": binding["content_hash"],
        "mime_type": binding["mime_type"],
        "byte_size": binding["byte_size"],
        "text": text,
    }


def _publication(project_id: str, timeline_id: str, *, video_ids: tuple[str, ...], music_id: str,
                 shots: tuple[dict, ...], binding: dict, transcript_document_id: str) -> dict:
    internal_revisions = []
    shot_revisions = []
    occurrences = []
    for index, shot in enumerate(shots, 1):
        shot_id = shot["shot_id"]
        internal_id = f"film-internal-{index}"
        shot_revision_id = f"film-shot-revision-{index}"
        source_media = video_ids[index - 1]
        text_bindings = []
        if index == 1:
            text_bindings.append(_binding_descriptor(binding, "Open on the river"))
        internal_revisions.append({
            "timeline_id": timeline_id,
            "revision_id": internal_id,
            "payload": {
                "tracks": [{"id": "picture", "kind": "visual"}],
                "clips": [{
                    "id": f"clip-{index}",
                    "clipType": "media",
                    "asset": f"picture-{index}",
                    "at": 0,
                    "hold": 1.8,
                    "track": "picture",
                    "elementRef": ({
                        "kind": "text",
                        "binding_id": binding["binding_id"],
                        "anchor": {"document_id": transcript_document_id, "word_id": "word-1"},
                    } if index == 1 else None),
                    "transition": ({"type": "crossfade", "duration": 0.2} if index == 2 else None),
                }],
                "effects": [],
                "audio": [],
                "layout": {},
                "registry": {"assets": {
                    f"picture-{index}": {
                        "object_id": source_media,
                        "type": "video",
                    },
                }},
                "assets": [],
            },
        })
        # ``None`` is an omitted authored field, not a semantic null value.
        clip = internal_revisions[-1]["payload"]["clips"][0]
        if clip["elementRef"] is None:
            del clip["elementRef"]
        if clip["transition"] is None:
            del clip["transition"]
        shot_revisions.append({
            "shot_id": shot_id,
            "revision_id": shot_revision_id,
            "internal_timeline_revision_id": internal_id,
            "payload": {
                "metadata": {
                    "title": shot["name"],
                    "transcript_anchor": ({
                        "document_id": transcript_document_id,
                        "segment_id": "segment-1",
                        "word_id": "word-1",
                    } if index == 1 else None),
                },
                "items": [],
                "pools": [],
                "selected_variants": {},
                "provenance": {"source_media": source_media},
                "generation_inputs": {},
                "audio_bindings": [],
                "text_bindings": text_bindings,
            },
        })
        if shot_revisions[-1]["payload"]["metadata"]["transcript_anchor"] is None:
            del shot_revisions[-1]["payload"]["metadata"]["transcript_anchor"]
        occurrences.append({
            "occurrence_id": f"occurrence-{index}",
            "shot_id": shot_id,
            "shot_revision_id": shot_revision_id,
            "placement": {"start_ms": (index - 1) * 1650, "track": "picture"},
            "source_offset": 0,
            "duration_ms": 1800,
            "speed": 1,
            "track": "picture",
            "transform": {},
            "gain": 1,
            "mute": False,
            "provenance": {"editorial_role": "picture"},
        })

    return {
        "project_id": project_id,
        "timeline_id": timeline_id,
        "expected_head": None,
        "parent_revision_id": "film-parent-v1",
        "internal_timeline_revisions": internal_revisions,
        "shot_revisions": shot_revisions,
        "parent_composition": {
            "config": {
                "output": {"fps": 24},
                "tracks": [
                    {"id": "picture", "kind": "visual", "role": "output"},
                    {"id": "music", "kind": "audio"},
                ],
                "playback": {"music_bed": "music-bed", "fade": {"in": 0.25, "out": 0.4}},
            },
            "registry": {"assets": {
                "music-bed": {"object_id": music_id, "type": "audio"},
            }},
            "clips": [{
                "id": "music-bed",
                "clipType": "audio",
                "asset": "music-bed",
                "at": 0,
                "hold": 5.5,
                "track": "music",
                "volume": 0.65,
                "effects": [{
                    "id": "music-fade",
                    "type": "fade",
                    "params": {"direction": "in", "duration": 0.25},
                }],
            }],
            "occurrences": occurrences,
        },
    }


def build_film_fixture(tmp_path: Path) -> FilmFixture:
    """Build and duplicate a compact, renderer-free film-shaped realm."""
    source_root = tmp_path / "film-source-realm"
    duplicate_root = tmp_path / "film-duplicate-realm"
    RealmStore.initialize(source_root, display_name="Synthetic Film Fixture", realm_id="synthetic-film-realm").close()
    service = RuntimeService(source_root)
    try:
        project = service.create_project(
            {"slug": "synthetic-film", "name": "Synthetic Film Fixture"},
            idempotency_key="film-project",
        )
        project_id = project["id"]
        timeline_id = "film"
        service.create_timeline(project_id, timeline_id, name="Film Assembly", idempotency_key="film-timeline")

        video_ids = tuple(
            _media(service, project_id, f"synthetic-picture-{index}".encode(), f"shot-{index}.mp4", "video/mp4")
            for index in range(1, 4)
        )
        music_id = _media(service, project_id, b"synthetic-music-bed", "music-bed.wav", "audio/wav")
        transcript_content = _transcript(video_ids[0])
        transcript_document_id = service._transcript_document_id(
            project_id, transcript_content["media_id"], transcript_content["source_id"]
        )
        service.create_document(
            project_id,
            {"document_id": transcript_document_id, "kind": "media.transcript", "content": transcript_content},
            idempotency_key="film-transcript",
        )

        shots = tuple(
            service.create_project_shot(
                project_id,
                {"shot_id": f"shot-{index}", "name": f"Shot {index}", "metadata": {"scene": index}},
                idempotency_key=f"film-shot-{index}",
            )["data"]
            for index in range(1, 4)
        )
        binding = service.set_project_shot_text_binding(
            project_id,
            {
                "shot_id": shots[0]["shot_id"],
                "kind": "transcript",
                "text": "Open on the river",
                "expected_head": 0,
            },
            idempotency_key="film-shot-1-transcript-binding",
        )["data"]
        publication = service.publish_parent_composition(
            project_id,
            timeline_id,
            _publication(
                project_id,
                timeline_id,
                video_ids=video_ids,
                music_id=music_id,
                shots=shots,
                binding=binding,
                transcript_document_id=transcript_document_id,
            ),
            idempotency_key="film-parent-publication",
        )
        assert publication["data"]["new_head"] == "film-parent-v1"
    finally:
        service.close()

    shutil.copytree(source_root, duplicate_root)
    return FilmFixture(
        source_root=source_root,
        duplicate_root=duplicate_root,
        project_id=project_id,
        timeline_id=timeline_id,
        parent_revision_id="film-parent-v1",
        media_ids=(*video_ids, music_id, binding["media_id"]),
        transcript_document_id=transcript_document_id,
        text_binding_id=binding["binding_id"],
    )


def read_object_from_realm(realm_root: Path, digest: str) -> bytes:
    bare = digest.removeprefix("sha256:")
    return (realm_root / "cas" / "sha256" / bare[:2] / bare[2:]).read_bytes()


def fixture_facts(service: RuntimeService, fixture: FilmFixture) -> dict:
    """Return small API/read facts used by tests and handoff documentation."""
    parent = service.get_project_parent_composition_revision(
        fixture.project_id, fixture.timeline_id, fixture.parent_revision_id
    )
    transcript = service.get_document(fixture.project_id, fixture.transcript_document_id)
    binding = service.get_project_shot_text_binding(fixture.project_id, fixture.text_binding_id)
    return {
        "parent": parent,
        "transcript": transcript,
        "binding": binding,
        "realm_id": service.store.realm["id"],
        "cas_ids": tuple(sorted(fixture.media_ids)),
    }
