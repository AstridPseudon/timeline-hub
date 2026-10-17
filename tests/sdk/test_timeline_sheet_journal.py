"""Sheet creation retains authored anchors in the journal and exact history."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk import timeline_checkout as tc
from astrid.sdk.timeline import journal, store
from astrid.sdk.timeline.apply_file import apply_file
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline_sheet import render_sheet


@pytest.fixture
def draft(tmp_path, monkeypatch):
    fixture = Path(__file__).resolve().parents[1] / "fixtures/timeline_editing/tiny.json"
    bundle = json.loads(fixture.read_text(encoding="utf-8"))
    namespace = bundle["parent"]["config"].setdefault("app", {}).setdefault("astrid", {})
    namespace["cut_id_high_water"] = {"number": 2, "suffixes": {}}
    namespace["future-journal-control"] = {"keep": [None, {"value": 17}]}
    bundle["shots"]["A"]["internal_timeline"]["clips"][1]["future-clip-control"] = {"keep": True}
    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", str(tmp_path / "data"))
    monkeypatch.setattr(tc, "resolve_ids", lambda *args, **kwargs: ("p", "t", "rev-0"))
    monkeypatch.setattr(tc, "fetch_bundle", lambda *args, **kwargs: copy.deepcopy(bundle))
    return Checkout.draft("P", "t")


@pytest.mark.parametrize("on", ['"now"', None])
def test_sheet_add_journals_its_authored_start_and_restores_exact_history(tmp_path, draft, on):
    tl = draft
    before = tl.document()
    records_before = journal.read(journal.journal_path("p", "t"))
    history = store._history_dir(Path(tl.path))
    steps_before = set(history.glob("*.json"))
    relation = f" on {on}" if on is not None else ""
    sheet = render_sheet(tl, cuts=["c2"])
    sheet += f"         sprite pin sprite R{relation} for 1.5s x=600 y=300\n"
    source = tmp_path / "add.sheet"
    source.write_text(sheet, encoding="utf-8")

    assert apply_file(tl, source)
    after = tl.document()
    pin = tl.clip("c2.pin")
    assert pin.start == pytest.approx(tl.time(on) if on is not None else tl.cut("c2").start)
    assert pin.duration == pytest.approx(1.5)
    assert (pin.get("x"), pin.get("y"), pin.asset) == (600, 300, "R")
    assert after["parent"] == before["parent"]
    assert after["shots"]["A"] == before["shots"]["A"]
    records = journal.read(journal.journal_path("p", "t"))
    assert len(records) == len(records_before) + 1
    assert set(history.glob("*.json")) - steps_before == {history / records[-1].undo_step}
    adds = [call for call in records[-1].calls if call["op"] == "timeline.add"]
    assert len(adds) == 1
    add = adds[0]
    assert add["args"]["at"] == (on if on is not None else tl.cut("c2").start)
    assert add["args"]["anchor"] is (on is not None)
    assert add["bindings"] == ({'"now"': "word:s2:1"} if on is not None else {})

    assert len(tl.undo()) == 1
    assert tl.document() == before
    assert len(tl.redo()) == 1
    assert tl.document() == after
    records = journal.read(journal.journal_path("p", "t"))
    assert [record.kind for record in records] == [record.kind for record in records_before] + ["save", "undo", "redo"]
    assert records[-2].before == records[-1].after == records[-3].after
    assert records[-2].after == records[-1].before == records[-3].before


@pytest.mark.parametrize("invalid", [False, True])
def test_sheet_property_mapping_preserves_authored_values_and_atomic_refusal(tmp_path, draft, invalid):
    from astrid.sdk.timeline_sheet import SheetError

    before = draft.document()
    path = Path(draft.path)
    journal_path = journal.journal_path("p", "t")
    document_bytes, journal_bytes = path.read_bytes(), journal_path.read_bytes()
    history = store._history_dir(path)
    history_before = {p.name: p.read_bytes() for p in history.glob("*.json")}
    source = tmp_path / "properties.sheet"
    # The rocket row is valid; the later c2 plate's fractional zoom is refused.
    # No earlier setter may survive the enclosing file transaction.
    sheet = render_sheet(draft).replace("x=60", "x=180 y=300")
    if invalid:
        sheet = sheet.replace("snap-plate  Q", "snap-plate  Q zoom=1.5")
    source.write_text(sheet, encoding="utf-8")
    if invalid:
        with pytest.raises(SheetError):
            apply_file(draft, source)
        assert draft.document() == before
        assert path.read_bytes() == document_bytes
        assert journal_path.read_bytes() == journal_bytes
        assert {p.name: p.read_bytes() for p in history.glob("*.json")} == history_before
        return

    assert apply_file(draft, source)
    after = draft.document()
    assert (draft.clip("c1.rocket").get("x"), draft.clip("c1.rocket").get("y")) == (180, 300)
    assert after["parent"] == before["parent"]
    rocket = next(clip for clip in after["shots"]["A"]["internal_timeline"]["clips"] if clip["id"] == "a-rocket")
    assert rocket["future-clip-control"] == {"keep": True}
    record = journal.read(journal_path)[-1]
    assert [call["args"] for call in record.calls if call["op"] == "clip.set"] == [{"x": 180, "y": 300}]
    assert len(draft.undo()) == 1
    assert draft.document() == before
    assert len(draft.redo()) == 1
    assert draft.document() == after
