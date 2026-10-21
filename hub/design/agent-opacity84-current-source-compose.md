# Agent opacity current-source composition report

## Source and schema

This is the reviewed opacity706 semantic unit composed onto the exact current
private source `6a8dfb2286659dd67c108a230d24f14ba4599344` (the 84fc floor),
not the older 392 sibling. The original current schema floor is
`84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`; the new
unfrozen canonical schema in this worktree is SHA-256
`9b4f16f87fffc00da010e2dbea469ca6bfc021695c5b453c821d1d4553336708`.
The schema remains 59 definitions / 33 operation clauses: opacity extends the
existing `ClipSetArgs` definition and adds no operation or DTO.

Product changes are limited to:

- `astrid/core/timeline/schema/edit-command.schema.json`: top-level raw
  `clip.set` opacity, finite JSON number in inclusive `0..1`, and
  `clear: ["opacity"]`.
- `astrid/sdk/timeline/_clip_scalar_commands.py`: capture docstring updated;
  existing handler, v2/source guards, materialization, inverse, producer,
  host, and current timing behavior are unchanged.
- Existing scalar conformance and schema-union tests only; no generated files,
  Runtime/App files, pins, artifacts, or frozen sources changed.

The test-only `without_opacity()` reconstruction removes only the opacity
property, clear enum member, and description wording from an in-memory copy.
It preserves the exact 84fc floor (59/33) and reconstructs these existing
floors: 65bb voiceover, 27f group, 392 project-data, 613 carrier, 6ba
ordinary, plus the existing f802 source-bound floor.

## Capture handoff example

```python
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set

set_command = capture_clip_set(
    bundle,
    "occurrence:occ-1/clip:picture-1",
    values={"opacity": 0.4},
)
clear_command = capture_clip_set(
    bundle,
    "parent/clip:direct",
    clear=["opacity"],
)
```

The resulting args are respectively
`{"values": {"opacity": 0.4}, "clear": []}` and
`{"values": {}, "clear": ["opacity"]}`. Selectors remain the existing
parent/occurrence raw clip identities. `params.opacity`, percent strings,
null clears, and values/clear overlap are refused. Capture records the exact
prior leaf state (absent, null, zero, or value) and retains existing owner,
source, media, v2, reads, bindings, inverse, replay, and ABA guards.

## Runtime/App2 ACK provenance

This composition preserves the bounded contract reviewed in:

- Runtime: `design/runtime-opacity706-contract-review.md` — bounded source
  ACK; no Runtime pin or activation.
- App2: `design/peer-app2-opacity-source-ack-20261020T2005.md` and
  `design/ap2-m2-opacity-source-semantic-review-REPORT.md` — source ACK only;
  native App activation remains downstream work.

Those ACKs reviewed the earlier 706 source identity/schema; this report gives
the exact current-source composition and new canonical schema identity for
the same semantics. No live callers exist, and no Runtime/App generation or
adoption was performed.

## Evidence

- `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/pytest -q tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_materialization_schema_union.py` — **135 passed**.
- `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/pytest -q tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py tests/editing_conformance/test_recipe_m1_commands.py` — **165 passed** in 4:19.
- `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/_clip_scalar_commands.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_materialization_schema_union.py` — passed.
- `python3 -m json.tool astrid/core/timeline/schema/edit-command.schema.json` — passed.
- `git diff --check` — passed.

No full, HTTP, browser, renderer, generation, pin, or activation suite was
run, per task scope.
