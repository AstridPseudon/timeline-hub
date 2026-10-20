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
from astrid.sdk.timeline.capture import capture_track_create
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
    # Historical data is authored with the pre-cut public API; measured edits
    # use the current Runtime and normal provider after reopening this realm.
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore

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
    service.create_project_shot(project, {"shot_id": "shot", "name": "Voice"},
                                idempotency_key="shot")
    voices = [{"id": "voice", "clipType": "media", "track": "vo", "asset": "take",
               "at": 1, "from": 2, "to": 6, "speed": 2}]
    if source_window is not None:
        voices[0]['source_window'] = source_window
    if reused:
        voices.append(dict(voices[0], id="other", at=4))
    # Initial untracked publication, before a commit history exists. No SQL,
    # fabricated receipts, or canonical Document aliases seed this realm.
    service.publish_parent_composition(project, "film", {
        "project_id": project, "timeline_id": "film", "expected_head": None,
        "parent_revision_id": "initial-parent",
        "internal_timeline_revisions": [{"timeline_id": "film", "revision_id": "internal",
            "payload": {"tracks": [{"id": "vo", "kind": "audio"}],
                "clips": voices,
                "registry": {"assets": {"take": {"media_id": media, "type": "audio"}}}}}],
        "shot_revisions": [{"shot_id": "shot", "revision_id": "shot-revision",
            "internal_timeline_revision_id": "internal", "payload": {"items": [],
                **(opaque if opaque_pin_scope == "shot" else {})}}],
        # The legacy publication seam only accepts numeric output.fps; main's
        # canvas retains the exact rational consumed by the timing compiler.
        "parent_composition": {"config": {"output": {"fps": 30000 / 1001},
            "theme_overrides": {"visual": {"canvas": {"fps": FPS}}},
            "tracks": [{"id": "picture", "kind": "visual"}]},
            "clips": [{"id": "card", "clipType": "am-type", "track": "picture", "at": 0,
                       "hold": 1, "app": {"astrid": {"on": DECLARATION, "for": 0.5}}}],
            **(opaque if opaque_pin_scope == "parent" else {}),
            "occurrences": [{"occurrence_id": "occ", "shot_id": "shot",
                "shot_revision_id": "shot-revision", "placement": {"start_ms": 2000, "track": "picture"},
                "duration_ms": duration_ms, "source_offset": 0, "speed": 1,
                **(opaque if opaque_pin_scope == "occurrence" else {})}]}},
        idempotency_key="initial-publication")

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
        "select": "parent", "args": {"row": {"id": "initial", "kind": "audio"}}}]), "initial")

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

