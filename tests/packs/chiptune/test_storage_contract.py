"""Contract-only checks: no synthesis, provider, Runtime or publication runs."""
from __future__ import annotations

import hashlib
import inspect
import json
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest

from astrid.core._shared.result_manifest import write_json_atomic, write_manifest
from astrid.core.contracts.errors import AstridError
from astrid.core.execution.generic_host import GenericPackHost
from astrid.core.foundation import atomic_io
from astrid.packs.chiptune.actions import _synth as syn
from astrid.packs.chiptune.actions.compose import planner, run

PACK = Path(__file__).resolve().parents[3] / "astrid/packs/chiptune"


def test_current_chiptune_has_no_declared_finite_storage_budget():
    host = GenericPackHost(pack_roots=[PACK])
    host.discover()
    record = host.capabilities["chiptune.compose"]
    assert record.estimated_scratch_bytes is None
    assert record.estimated_output_bytes is None
    host.preflight("chiptune.compose")
    record = host.capabilities["chiptune.compose"]
    assert record.ready  # The joined request-estimator declaration is valid.
    assert record.storage_estimate_unavailable_reason is None
    assert record.has_request_storage_estimator
    assert record.manifest()["ready"] is False  # Preparation is not ordinary ready-to-run work.
    assert record.estimated_output_bytes is None  # It still has no static byte budget.
    # This WAV lower bound alone already disproves J030's former zero ceiling.
    # It is deliberately not presented as an estimate of all three outputs.
    assert 4 * round(2 * syn.SAMPLE_RATE) + 44 == 384044
    assert 384044 < 386233  # preserved J030 actual, including JSON and manifest


def test_manifest_estimator_declaration_binds_to_existing_qualified_helper():
    host = GenericPackHost(pack_roots=[PACK])
    host.discover()
    definition = host.capabilities["chiptune.compose"].definition
    declared = definition.metadata["storage_estimator"]
    action_declaration = definition.metadata["action_declaration"]

    from astrid.packs.chiptune.actions.compose import planner

    helper = planner.estimate_compose_storage
    source_digest = "sha256:" + hashlib.sha256(
        inspect.getsource(helper).encode("utf-8")
    ).hexdigest()

    assert declared == {
        "mode": "request_estimated",
        "estimator": {
            "id": "chiptune.compose.storage",
            "version": 1,
            "implementation_digest": source_digest,
        },
        "implementation": {
            "module": "astrid.packs.chiptune.actions.compose.planner",
            "function": "estimate_compose_storage",
        },
    }
    assert declared["implementation"]["module"] == helper.__module__
    assert declared["implementation"]["function"] == helper.__name__
    assert action_declaration["metadata"]["storage_estimator"] == declared


@pytest.mark.parametrize("count", [1, 1000])
def test_accepted_structured_inputs_have_no_declared_item_count_bound(count):
    sections = [{"start_s": i * 2 / count, "end_s": (i + 1) * 2 / count,
                 "mood": "silent", "energy": 0, "caller_note": "x" * count}
                for i in range(count)]
    assert len(syn.validate_sections(sections, 2)) == count
    # run.main writes original sections into manifest.inputs, including extra
    # keys; validation cleans only the separate synthesis representation.
    assert len(json.dumps(sections)) > count * count
    assert len(syn.normalize_hits(syn.parse_hits([0.5] * count), 2)) == count
    raw_windows = [[0, 1]] * count
    assert len(run._parse_mutes(raw_windows)) == count
    assert len(run._parse_vo_mask(raw_windows)) == count
    assert len(run._parse_duck([{"start_s": 0, "end_s": 1}] * count, -10)) == count


@pytest.mark.parametrize("duration,bpm", [(0, 132), (3601, 132), (2, 29), (2, 241)])
def test_existing_duration_and_tempo_limits_still_reject_before_synthesis(duration, bpm):
    with pytest.raises(AstridError, match="must be between"):
        syn.compose_music(duration_s=duration, bpm=bpm, key="A minor", seed=424021,
                          sections=[{"start_s": 0, "end_s": 2, "mood": "wistful"}])


def test_existing_structured_input_validation_is_not_narrowed():
    with pytest.raises(AstridError, match="must not overlap"):
        syn.validate_sections([{"start_s": 0, "end_s": 2}, {"start_s": 1, "end_s": 2}], 2)
    with pytest.raises(AstridError, match="falls outside"):
        syn.normalize_hits([2], 2)
    with pytest.raises(AstridError, match="must be"):
        run._parse_mutes([[0, 1, 2]])


def _params(**overrides):
    params = {
        "duration_s": 2,
        "sections": [{"start_s": 0, "end_s": 2, "energy": 0.37, "mood": "wistful"}],
    }
    params.update(overrides)
    return params


def test_unknown_storage_stays_distinct_from_static_zero_and_dynamic_estimate():
    import copy

    host = GenericPackHost(pack_roots=[PACK])
    host.discover()
    unknown = host.capabilities["chiptune.compose"]
    static_metadata = copy.deepcopy(unknown.definition.metadata)
    static_metadata.pop("storage_estimator")
    static_metadata["action_declaration"]["metadata"].pop("storage_estimator")
    static_metadata.update(estimated_scratch_bytes=0, estimated_output_bytes=0)
    zero_definition = replace(
        unknown.definition,
        metadata=static_metadata,
    )
    declared_zero = replace(unknown, definition=zero_definition)
    estimate = planner.estimate_compose_storage(_params())

    assert unknown.estimated_output_bytes is None
    assert unknown.has_request_storage_estimator
    assert unknown.storage_estimate_unavailable_reason is None
    assert declared_zero.estimated_scratch_bytes == declared_zero.estimated_output_bytes == 0
    assert declared_zero.storage_estimate_unavailable_reason is None
    assert not declared_zero.has_request_storage_estimator
    assert estimate.output_bytes > 0 and estimate.scratch_bytes > 0


def test_defaults_raw_extras_and_entry_cardinality_change_estimate():
    defaults = planner.build_composition_plan(_params())
    assert (defaults.bpm, defaults.key, defaults.seed, defaults.style) == (132.0, "A minor", 1, "nes")
    assert defaults.duck_db == -10 and defaults.master_db == -16

    one = planner.estimate_compose_storage(_params())
    many_sections = [
        {"start_s": index * 2 / 1000, "end_s": (index + 1) * 2 / 1000,
         "energy": 0, "mood": "silent"}
        for index in range(1000)
    ]
    thousand_sections = planner.estimate_compose_storage(_params(sections=many_sections))
    thousand_hits = planner.estimate_compose_storage(_params(hits=[0.5] * 1000))
    assert thousand_sections.output_bytes > one.output_bytes
    assert thousand_hits.output_bytes > one.output_bytes

    extra = "🎹\\\"\n" * 2000
    rich = planner.estimate_compose_storage(_params(
        seed=(1 << 1000) + 123456789,
        sections=[{"start_s": 0, "end_s": 2, "energy": 0.37, "mood": "wistful", "note": extra}],
        hits=[{"t": 0.5, "kind": "blip", "label": extra}],
        duck=[{"start_s": 0.2, "end_s": 0.8, "gain_db": -12, "provenance": extra}],
        vo_mask=[[0.3, 0.9]],
    ))
    assert rich.output_bytes > one.output_bytes


@pytest.mark.parametrize(
    "duration,bpm,frames",
    [
        (1.0, 30, 48_000),
        (1.0 + 0.5 / syn.SAMPLE_RATE, 240, 48_000),
        (1.0 + 1.5 / syn.SAMPLE_RATE, 132, 48_002),
        (2.0, 240, 96_000),
    ],
)
def test_wav_estimate_uses_renderer_rounding_and_tempo_grid(duration, bpm, frames):
    estimate = planner.estimate_compose_storage(_params(duration_s=duration, bpm=bpm))
    plan = planner.build_composition_plan(_params(duration_s=duration, bpm=bpm))
    assert plan.sample_count == frames
    assert estimate.output_breakdown["music_wav_bytes"] == 4 * frames + 44


@pytest.mark.parametrize(
    "params",
    [
        _params(duration_s=float("inf")),
        _params(seed=-1),
        _params(sections=[{"start_s": 0, "end_s": 2, "energy": float("nan")}]),
        _params(hits=[{"t": 0.5, "label": float("inf")}]),
        _params(duck=[{"start_s": 0, "end_s": 1, "gain_db": float("nan")}]),
        _params(sections=[{"start_s": 0, "end_s": 2, "extra": object()}]),
        _params(sections="not JSON"),
    ],
)
def test_estimator_refuses_malformed_nonfinite_and_unserializable_inputs(params):
    with pytest.raises(AstridError):
        planner.estimate_compose_storage(params)


def test_estimate_matches_actual_json_writers_and_atomic_temp_overlap(tmp_path, monkeypatch):
    params = _params(
        hits=[{"t": 0.5, "kind": "blip", "caller_note": "π/🎹"}],
        duck=[{"start_s": 0.2, "end_s": 0.8, "gain_db": -11, "caller_note": "duck"}],
        vo_mask=[[0.3, 0.9]],
        mutes=[[1.1, 1.4]],
    )
    plan = planner.build_composition_plan(params)
    estimate = planner.estimate_compose_storage(params)
    sections_out = planner.build_section_outputs(plan, [(-100.123, -100.123)])
    beats = planner.build_beats_document(plan, sections_out)
    beats_text = json.dumps(beats, indent=2, sort_keys=True, allow_nan=False) + "\n"
    output_root = tmp_path / "outputs"
    output_root.mkdir()
    music_path = output_root / "music.wav"
    with music_path.open("wb") as handle:
        handle.truncate(estimate.output_breakdown["music_wav_bytes"])

    observations = []
    original_replace = atomic_io.os.replace

    def observe_replace(source, destination):
        files = {path.name: path.stat().st_size for path in output_root.iterdir() if path.is_file()}
        temp_bytes = sum(size for name, size in files.items() if name.endswith(".tmp"))
        observations.append((sum(files.values()), temp_bytes, files))
        return original_replace(source, destination)

    monkeypatch.setattr(atomic_io.os, "replace", observe_replace)
    beats_path = output_root / "beats.json"
    write_json_atomic(beats_path, beats)
    manifest = planner.build_result_manifest(
        plan,
        sections_out=sections_out,
        created=datetime.now(timezone.utc).isoformat(),
        peak_dbfs=-100.123,
        rms_dbfs=-100.123,
    )
    manifest_path = output_root / "manifest.json"
    write_manifest(manifest_path, manifest)

    actual_beats_bytes = beats_path.stat().st_size
    actual_manifest_bytes = manifest_path.stat().st_size
    assert actual_beats_bytes == len(beats_text.encode("utf-8"))
    assert actual_beats_bytes <= estimate.output_breakdown["beats_json_bytes"]
    assert actual_manifest_bytes == estimate.output_breakdown["manifest_json_bytes"]
    assert estimate.output_bytes == sum(estimate.output_breakdown.values())
    assert estimate.scratch_bytes == max(
        estimate.output_breakdown["beats_json_bytes"],
        estimate.output_breakdown["manifest_json_bytes"],
    )
    assert len(observations) == 2
    assert [temp_bytes for _, temp_bytes, _ in observations] == [
        actual_beats_bytes,
        actual_manifest_bytes,
    ]
    assert observations[0][0] == estimate.output_breakdown["music_wav_bytes"] + actual_beats_bytes
    assert observations[1][0] == (
        estimate.output_breakdown["music_wav_bytes"] + actual_beats_bytes + actual_manifest_bytes
    )
    assert max(temp_bytes for _, temp_bytes, _ in observations) <= estimate.scratch_bytes
    assert max(total for total, _, _ in observations) <= estimate.output_bytes
    manifest_temps = [
        size for name, size in observations[-1][2].items()
        if name.startswith(".manifest.json.") and name.endswith(".tmp")
    ]
    assert manifest_temps == [actual_manifest_bytes]


def test_estimator_and_renderer_metadata_share_the_same_plan_without_audio():
    params = _params(
        bpm=97,
        sections=[
            {"start_s": 0, "end_s": 0.7, "energy": 0.8, "mood": "tense", "custom": "keep"},
            {"start_s": 1.1, "end_s": 2, "mood": "silent"},
        ],
        hits=[0.25, {"t": 1.5, "kind": "thud", "extra": "preserve"}],
        mutes=[[1.2, 1.4]],
    )
    plan = planner.build_composition_plan(params)
    render_metadata = planner.build_renderer_metadata(plan)
    estimate = planner.estimate_compose_storage(params)

    assert render_metadata["beats"] == plan.beats
    assert render_metadata["downbeats"] == plan.downbeats
    assert render_metadata["bars"] == plan.bars
    assert render_metadata["sections"] == planner.build_section_metadata(plan)
    assert render_metadata["hits"] == [{"t": 0.25, "kind": "stab"}, {"t": 1.5, "kind": "thud"}]
    assert estimate.output_breakdown["beats_json_bytes"] > 0


def test_compose_compatibility_entrypoint_passes_its_plan_to_renderer(monkeypatch):
    params = _params(bpm=132, key="A minor", seed=1, hits=[0.25], mutes=[[1.2, 1.4]])
    expected_plan = planner.build_composition_plan(params)
    observed = []

    def render_without_audio(plan):
        observed.append(plan)
        return object(), planner.build_renderer_metadata(plan)

    monkeypatch.setattr(syn, "render_composition_plan", render_without_audio)
    _, metadata = syn.compose_music(**params)

    assert len(observed) == 1
    assert observed[0].beats == expected_plan.beats
    assert observed[0].planned_sections == expected_plan.planned_sections
    assert metadata == planner.build_renderer_metadata(expected_plan)
