"""Real Runtime fixture using first-use transcript capture by the native provider."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.timeline import moments
from astrid.core.timeline.authoring_bundle import _digest
from astrid.sdk.media_transcript import build_transcript, transcript_document_id
from astrid.sdk.timeline import commit as agent
from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.compiler import WordBinding
from astrid.sdk.timeline.units import source_to_timeline_time
from tests.helpers.runtime import runtime_checkout, use_runtime

TARGET = ('parent', '', 'card')
DECLARATION = '\"again\" in line #2 +1f'
FPS = {'numerator': 30000, 'denominator': 1001}

def first_selection(bundle):
    """Select once from this fixture's sole verified source using main's grammar.

    No binding is accepted from a caller. This intentionally has no replay
    mode: the tests expose why re-running selection is insufficient for replay.
    """
    captures = bundle["source_mapping"]["pinned_documents"]
    assert len(captures) == 1
    capture = captures[0]
    pin, document = capture["pin"], capture["document"]
    declaration = bundle["parent"]["clips"][0]["app"]["astrid"]["on"]
    moment = moments.parse(declaration)
    words = []
    for row in bundle["placements"]:
        assert row["source_offset"] == 0 and row["speed"] == 1
        internal = bundle["shots"][row["shot_id"]]["internal_timeline"]
        for clip in internal["clips"]:
            asset = internal["registry"]["assets"][clip["asset"]]
            assert asset["media_id"] == document["content"]["media_id"]
            owner = (row["occurrence_id"], row["shot_id"], clip["id"])
            origin = Fraction(row["placement"]["start_ms"], 1000) + Fraction(str(clip["at"]))
            for segment in document["content"]["segments"]:
                for index, word in enumerate(segment["words"]):
                    if not clip["from"] <= word["start"] < word["end"] <= clip["to"]:
                        continue
                    times = {key: source_to_timeline_time(Fraction(str(word[key])),
                        source_start=Fraction(str(clip["from"])), timeline_start=origin,
                        speed=clip["speed"]) for key in ("start", "end")}
                    words.append(SimpleNamespace(**dict(word, **times), segment=segment["id"],
                                                 index=index, owner=owner))
    words.sort(key=lambda word: (word.start, word.owner, word.id))
    hits = moments.find_words(moment, words)
    assert moment.n is not None or len(hits) == 1
    chosen = hits[(moment.n or 1) - 1]
    assert len({word.owner for word in chosen}) == 1
    return WordBinding(TARGET, "on", declaration, chosen[0].owner, pin["document_id"],
                       pin["version"], pin["content_digest"], tuple(word.id for word in chosen))


def seed(root, reused, *, duration_ms=10000, source_window=None, opaque_pin_scope=None):
    # Source documents are ordinary Runtime data.  The timeline fixture is
    # bootstrapped through the live commit provider below, not the retired
    # parent-composition publisher.
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path

    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline.emitter import emit_document_commands
    from astrid.sdk.timeline.native_initialize import capture_initialize
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create

    root = Path(root)
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project({"slug": "timing", "name": "Timing"})["id"]
    media = service.ingest(project, b"timing-source", media_type="audio/wav",
                           original_name="voice.wav", idempotency_key="voice")["data"]["object_id"]
    content = build_transcript(media, "line", "again again stop", [
        [2, 2.5, "again"], [3, 3.5, "again"], [5.5, 6, "stop"],
    ])
    document_id = transcript_document_id(project, media, content["source_id"])
    source = service.create_document(project, {"document_id": document_id,
        "kind": "media.transcript", "content": content}, idempotency_key="transcript-v1")["data"]
    pin = {"document_id": document_id, "version": 1, "content_digest": _digest(content)}
    opaque = {"opaque_transcript": {"pin": pin, "raw": [None, False, 0, 0.0, {}, [], ""]}}

    service.register_timeline_commit_provider(agent.create_runtime_commit_service())
    service.create_timeline(project, "film", idempotency_key="timeline")

    def head():
        value = service.get_project_timeline(project, "film")
        return {"revision_id": value["head_revision_id"],
                "publication_id": value["head_publication_id"]}

    def submit(commands, key):
        current = head()
        result = service.commit_timeline(
            project, "film", {
                "api_version": 1, "project_id": project, "timeline_id": "film",
                "base_revision_id": current["revision_id"],
                "base_publication_id": current["publication_id"],
                "commands": commands,
            }, idempotency_key=key, publisher="timing-editor",
            invocation_path=route_path(project, "film"), authorize=lambda: None,
        )
        return result["data"]["canonical_document"]

    bootstrap = service.get_project_parent_composition_revision(
        project, "film", head()["revision_id"])
    empty = {
        "schema_version": 1, "project_id": project, "timeline_id": "film",
        "parent_revision": {key: bootstrap[key] for key in
                             ("revision_id", "content_digest", "payload")},
        "shot_revisions": [], "internal_timeline_revisions": [],
        "dependency_manifest": bootstrap["dependency_manifest"],
    }
    bundle = bundle_from_document(empty)
    initialize = capture_initialize(
        bundle, name="Voice", slug="film", output={
            "resolution": "1280x720", "fps": 30, "file": "output.mp4",
            "background": None, "background_scale": None,
        },
    )
    initialized = execute(bundle, [initialize]).bundle
    parent_track = capture_track_create(initialized, "parent", {
        "id": "picture", "kind": "visual",
    })
    tracked = execute(initialized, [parent_track]).bundle
    card = capture_clip_add(tracked, "parent", {
        "id": "card", "clipType": "am-type", "track": "picture", "at": 0,
        "hold": 1, "app": {"astrid": {"on": DECLARATION, "for": 0.5}},
    })
    carded = execute(tracked, [card]).bundle
    occurrence = capture_occurrence_create(
        carded, "occ", "shot", name="Voice", track="picture", on=2, duration=duration_ms / 1000,
    )
    occurred = execute(carded, [occurrence]).bundle

    voices = [{"id": "voice", "clipType": "media", "track": "vo", "asset": "take",
               "at": 1, "from": 2, "to": 6, "speed": 2}]
    if source_window is not None:
        voices[0]['source_window'] = source_window
    if reused:
        voices.append(dict(voices[0], id="other", at=4))
    after = copy.deepcopy(occurred)
    # timeline.init accepts only its supported bootstrap fps; retain the exact
    # authored rational output through the emitter's guarded before/after patch.
    after["parent"]["config"]["output"]["fps"] = copy.deepcopy(FPS)
    after["parent"]["config"]["theme_overrides"] = {"visual": {"canvas": {"fps": FPS}}}
    after["shots"]["shot"]["payload"].update(
        {"items": [], **(opaque if opaque_pin_scope == "shot" else {})})
    internal = after["shots"]["shot"]["internal_timeline"]
    internal["tracks"] = [{"id": "vo", "kind": "audio"}]
    internal["clips"] = voices
    internal["registry"] = {"assets": {"take": {"media_id": media, "type": "audio"}}}
    if opaque_pin_scope == "parent":
        after["parent"]["opaque"] = copy.deepcopy(opaque)
    if opaque_pin_scope == "occurrence":
        after["placements"][0]["opaque"] = copy.deepcopy(opaque)
    changes = emit_document_commands(occurred, after)
    # occurrence.create quantizes its input placement.  The fixture's source
    # contract retains the original literal 2000ms placement, so carry that
    # authored field through the generic patch path with its exact guard.
    placement_start = occurred["placements"][0]["placement"]["start_ms"]
    changes[0]["args"]["changes"].insert(0, {
        "op": "set", "ref": "parent",
        "path": ["occurrences", "occurrence:occ", "placement", "start_ms"],
        "before": {"state": "present", "value": placement_start}, "value": 2000,
    })
    media_admission = {
        "schema_version": 1, "op": "media.admit", "version": "1", "select": None,
        "args": {"inputs": [{"pin": {"media_id": media, "content_digest": media}}]},
    }
    submit([initialize, parent_track, card, occurrence, media_admission, *changes], "initial-commit")

    service.close()
    return {'project': project, 'pin': pin, 'source': source}


@pytest.fixture
def retained(tmp_path, monkeypatch, request):
    use_runtime()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_port import route_path

    root = tmp_path / 'realm'
    historical = (Path(os.environ['ASTRID_WORD_ANCHOR_SEED_RUNTIME'])
                  if os.environ.get('ASTRID_WORD_ANCHOR_SEED_RUNTIME')
                  else runtime_checkout('80973d34ae10e498d7213c30287012c9876f4b1a'))
    script = """
import json, sys
from tests.editing_conformance.native_word_anchor_fixture import seed
options = json.loads(sys.argv[2])
print(json.dumps(seed(sys.argv[1], options.pop('reused', False), **options)))
"""
    options = getattr(request, 'param', False)
    options = options if isinstance(options, dict) else {'reused': options}
    seeded = subprocess.run([sys.executable, '-c', script, str(root),
        json.dumps(options)], text=True, capture_output=True, check=True,
        env={**os.environ, 'PYTHONPATH': str(Path(__file__).resolve().parents[2]) + os.pathsep + str(historical),
             'PYTHONDONTWRITEBYTECODE': '1'}, cwd=tmp_path)
    values = json.loads(seeded.stdout)
    project, pin, source = (values[key] for key in ('project', 'pin', 'source'))
    service = RuntimeService(root)
    case = SimpleNamespace(service=service, root=root, project=project, pin=pin, source=source,
                           hydrated=[], documents={})

    class NoSceneImports:
        def find_spec(self, fullname, path=None, target=None):
            if fullname.startswith(('composition', 'remotion', 'astrid.sdk.authoring_render_preview')) or '.scene' in fullname:
                raise AssertionError('commit imported scene evaluation: ' + fullname)

    def no_renderer(*args, **kwargs):
        raise AssertionError('commit evaluated a scene with the renderer off')

    import runtime_protocol.service as service_module
    import runtime_protocol.visual_seam as visual_seam

    monkeypatch.setattr(sys, 'meta_path', [NoSceneImports(), *sys.meta_path])
    monkeypatch.setattr(service_module, 'evaluate_closure', no_renderer)
    monkeypatch.setattr(visual_seam, 'evaluate_closure', no_renderer)

    def head():
        value = case.service.get_project_timeline(project, "film")
        return {"revision_id": value["head_revision_id"], "publication_id": value["head_publication_id"]}

    def request(commands, base=None):
        base = base or head()
        return {"api_version": 1, "project_id": project, "timeline_id": "film",
                "base_revision_id": base["revision_id"], "base_publication_id": base["publication_id"],
                "commands": commands}

    def submit(body, key, authorize=lambda: None):
        result = case.service.commit_timeline(project, "film", body, idempotency_key=key,
            publisher="timing-editor", invocation_path=route_path(project, "film"), authorize=authorize)
        document = result["data"]["canonical_document"]
        case.documents[document["parent_revision"]["revision_id"]] = document
        return result

    service.register_timeline_commit_provider(agent.create_runtime_commit_service())
    hydrate = agent._hydrate

    def observed(port, bundle, calls=(), **kwargs):
        result = hydrate(port, bundle, calls, **kwargs)
        case.hydrated.append(copy.deepcopy(bundle))
        return result

    monkeypatch.setattr(agent, "_hydrate", observed)
    case.seed = submit(request([{"schema_version": 1, "op": "track.create", "version": "1",
        "select": "parent", "created": ["parent/track:initial"],
        "args": {"row": {"id": "initial", "kind": "audio"}}}]), "initial")

    def restart(provider=None):
        case.service.close()
        case.service = RuntimeService(root)
        case.service.register_timeline_commit_provider(provider or agent.create_runtime_commit_service())

    def create(track, base=None):
        base = base or head()
        bundle = agent.bundle_from_document(case.documents[base["revision_id"]])
        bundle["source_mapping"]["pinned_documents"] = copy.deepcopy(
            case.hydrated[-1]["source_mapping"].get("pinned_documents", []))
        command = capture_track_create(bundle, "parent", {"id": track, "kind": "audio"})
        return request([command], base)

    case.head, case.request, case.submit, case.restart, case.create = head, request, submit, restart, create
    try:
        yield case
    finally:
        case.service.close()
