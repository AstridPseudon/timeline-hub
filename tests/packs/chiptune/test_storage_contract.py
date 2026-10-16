"""Contract-only checks: no synthesis, provider, Runtime or publication runs."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from astrid.core.contracts.errors import AstridError
from astrid.core.execution.generic_host import GenericPackHost
from astrid.packs.chiptune.actions import _synth as syn
from astrid.packs.chiptune.actions.compose import run

PACK = Path(__file__).resolve().parents[3] / "astrid/packs/chiptune"


def test_current_chiptune_has_no_declared_finite_storage_budget():
    host = GenericPackHost(pack_roots=[PACK])
    host.discover()
    record = host.capabilities["chiptune.compose"]
    assert record.estimated_scratch_bytes is None
    assert record.estimated_output_bytes is None
    host.preflight("chiptune.compose")
    record = host.capabilities["chiptune.compose"]
    assert not record.ready
    assert "estimated_output_bytes" in record.preflight["storage_estimate"]["reason"]
    # This WAV lower bound alone already disproves J030's former zero ceiling.
    # It is deliberately not presented as an estimate of all three outputs.
    assert 4 * round(2 * syn.SAMPLE_RATE) + 44 == 384044
    assert 384044 < 386233  # preserved J030 actual, including JSON and manifest


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
