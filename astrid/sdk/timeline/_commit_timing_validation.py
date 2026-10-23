"""Validate a complete canonical candidate through the existing timing kernel."""
from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from astrid.core.timeline import moments
from astrid.core.timeline.authoring_bundle import compile_authoring_candidate
from astrid.core.timeline.shot_composition_projection import _placement_speed
from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline.compiler import TimingCompileError, TimingInputs, compile_timing
from astrid.sdk.timeline.native_word_anchor import binding, legacy_binding
from astrid.sdk.timeline.units import _time_fraction


def validate_candidate_timing(candidate: Mapping[str, Any]) -> None:
    """Compile a detached validation view, leaving authored JSON and pins intact.

    The canonical compiler guards changes to occurrence source maps. As in
    shot_composition_projection._project_clip, retained occurrence speed and
    source_offset are provenance, while child windows supply timing. Only that
    placement representation is adapted; no clip or declaration is discarded.
    """
    publication = compile_authoring_candidate(candidate).publication
    projection = copy.deepcopy(dict(candidate))
    config = projection["parent"]["config"]
    output = config.get("output") or {}
    if "fps" in output:
        canvas = config
        for key in ("theme_overrides", "visual", "canvas"):
            if canvas.get(key) is None:
                canvas[key] = {}
            canvas = canvas[key]
        canvas.setdefault("fps", copy.deepcopy(output["fps"]))
    projection["placements"] = copy.deepcopy(publication["parent_composition"]["occurrences"])
    for row in projection["placements"]:
        path = f"candidate.placements[{row['occurrence_id']!r}]"
        _placement_speed(row.get("speed"), path=f"{path}.speed")
        offset = row.get("source_offset")
        if isinstance(offset, Mapping):
            for key in ("start", "end"):
                if key in offset:
                    _time_fraction(offset[key], f"{path}.source_offset.{key}")
        elif offset is not None:
            _time_fraction(offset, f"{path}.source_offset")
        row["speed"], row["source_offset"] = 1, 0

    sources = candidate.get("source_mapping", {}).get("pinned_documents", [])
    bindings = []
    for shot in projection["shots"].values():
        for clip in shot["internal_timeline"]["clips"]:
            refs = intent._app(clip).get("word_anchors", {})
            if not isinstance(refs, dict) or set(refs) - {"on", "until"}:
                raise TimingCompileError("invalid authored word anchor fields")
            if refs:
                raise TimingCompileError("word anchors require parent ownership")
    for clip in projection["parent"]["clips"]:
        declarations = intent._app(clip)
        refs = declarations.get("word_anchors", {})
        if not isinstance(refs, dict) or set(refs) - {"on", "until"}:
            raise TimingCompileError("invalid authored word anchor fields")
        for field in ("on", "until"):
            target = "parent/clip:" + clip["id"]
            if field in refs:
                selected = binding(projection, target, field, refs[field], sources)
            elif declarations.get(field) and isinstance(declarations[field], str) and moments.parse(
                    declarations[field]).kind == "word":
                selected = legacy_binding(projection, target, field, declarations[field], sources)
            else:
                continue
            bindings.append(selected)
            # The existing binding adapter supplies the private kernel spelling
            # from exact word IDs. The authored echo remains in the candidate.
            app = clip.setdefault("app", {})
            if app.get("astrid") is None:
                app["astrid"] = {}
            app["astrid"][field] = selected.declaration
    compile_timing(TimingInputs(
        projection,
        sources=[row for row in sources if row["document"]["kind"] == "media.transcript"],
        bindings=bindings,
    ))
