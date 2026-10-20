# Agent bounded clip opacity private source proposal

Status: **SOURCE ONLY — Runtime/App2 ACK required before generation or native
consumer activation.** No generated client, Runtime/App pin, public artifact,
integration change, or writer deletion is included.

## Exact source identity

- Agent worktree: `/home/user/work/wt/agt-m2-opacity-private-source-proposal`
- Base commit: `e010e6a3868e963471244491bb6672c3e4a5135e`
- Base tree: `70414cf6875d2c97c45f33e0a5158c80bd7391d9`
- Candidate tree with this uncommitted source proposal: `ff2a0144563bb27b7a1169ae0276c3e3d1b7b195`
- Final commit SHA: **pending harness commit**; the candidate patch SHA-256 is
  `465c423fc51bf7a8a4100e359f87aedff9112f4f47d71e7caeefec4905a33a29`.
- Canonical schema:
  `astrid/core/timeline/schema/edit-command.schema.json`
- Candidate schema SHA-256:
  `110165ab9f7e4be3e9766d06b5ceacab8c5e8c7cc12e7180929005b67bcc82d6`
- Changed source file SHA-256 values:
  - `astrid/sdk/timeline/_clip_scalar_commands.py`:
    `ceff9398a45b00888c41a984913a497b11b1339370f3e18b3bbfaa6af51d00f5`
  - `tests/editing_conformance/test_recipe_clip_scalar_fields.py`:
    `c0e5466d9e036064d73327ff5f41cf7a6d3b0643618378e6d3d01e514cfe178b`

The frozen project-data/private-carrier source and ordinary floor are not
relabeled: the existing `613123b2...` and `6ba7b51e...` bytes/refs remain
immutable. This is a distinct additive schema candidate over e010's 56/30/12
source.

## Main evidence and semantic floor

The reviewed Main App path is the ordinary clip property control in
`ClipPanelBody` (the Appcensus row identifies the opacity path at the cited
Main body location). The current checked source reads `clip.opacity ?? 1` and
emits the Slider's raw numeric value; it does not read or write
`params.opacity`. Agent's current timeline model likewise declares opacity as
a top-level numeric clip field in `timeline-config.schema.json` and the
canonical clip allowlist.

This proposal therefore admits only the existing closed `clip.set@1` family:

- Stable selectors remain exactly `parent/clip:<raw-id>` and
  `occurrence:<occurrence-id>/clip:<raw-id>`; selector ownership is retained.
- `args.values.opacity` is a JSON number in the inclusive raw fraction range
  `0..1`. Boolean, null, string, non-finite, and out-of-range values refuse.
- `args.clear` additionally admits `"opacity"`; clearing removes the leaf and
  never writes null, an empty string, a default, or a percentage conversion.
- The handler writes/clears only `clip["opacity"]`. It does not alias to
  `params.opacity`, manufacture a selected-pack schema, add an operation, or
  rewrite a container.
- Existing `_target`/`_clip_basis` reads and the generic recorder continue to
  supply original identity/source/media guards, exact leaf expectations,
  authorship, unchanged writes, inverse/redo, strict A→B→A refusal, and
  disjoint-property rebase. Opaque fields, direct neighboring fields, and
  other occurrences remain untouched.
- Existing hold, asset-clear, and transition-clear meanings and their recorded
  original pin remain unchanged. No other look property is admitted here.

The exact capture shape is:

```python
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set

set_opacity = capture_clip_set(
    bundle,
    "parent/clip:f2-app-clip",
    values={"opacity": 0.4},
)
clear_opacity = capture_clip_set(
    bundle,
    "occurrence:occ-1/clip:picture-1",
    clear=["opacity"],
)
```

The Main-shaped SET is `op: "clip.set"` with
`args: {"values": {"opacity": 0.4}, "clear": []}` and an exact original
`<selector>::opacity` expectation. Clear is
`{"values": {}, "clear": ["opacity"]}`.

## Agent evidence

Added only the closed schema member, the existing capture docstring update,
and compact conformance in the existing scalar-field test module. The tests
cover Main-parity top-level capture (including a hostile `params.opacity` that
must remain unchanged), occurrence isolation/direct neighbors, absent/null/0/
value presence, exact inverse/redo, invalid values and params bypass, strict
ABA, and disjoint parameter rebase.

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_clip_scalar_fields.py
111 passed, 2 warnings

python3 -m json.tool astrid/core/timeline/schema/edit-command.schema.json
ruff check astrid/sdk/timeline/_clip_scalar_commands.py tests/editing_conformance/test_recipe_clip_scalar_fields.py
git diff --check
```

The neighboring schema/registry command was also run. It produced 178 passed
and 7 failures in exact frozen-schema/hash assertions, all caused by the
intentional new candidate schema bytes; no frozen artifact test or hash was
edited. Those failures are not evidence that the opacity command semantics
failed, and they must not be “fixed” by relabeling the old 613/6ba refs.

No full/full-* suite, root pytest, Runtime service, browser/socket journey,
generation, pin, merge, or consumer activation was run.

## ACK gate

Runtime and App2 should ACK this exact candidate tree/schema and the
top-level-`clip.opacity` contract before any private generation or native App
consumer activation. This handoff does not claim whole-writer deletion or
that the old App consumer is retired; those require the separately owned
normal matched-native gate.
