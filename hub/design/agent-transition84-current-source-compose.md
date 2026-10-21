# Agent transition source handoff

Status: **SOURCE ONLY — Runtime/App2 ACK requested; no generation, pin, freeze,
activation, or public release.**

## Exact source

- Current Agent base: `6a8dfb2286659dd67c108a230d24f14ba4599344` (`6a8` private floor).
- Current pre-change schema SHA-256: `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`.
- Working schema SHA-256 after the additive transition fields:
  `77d379467fc622a7de75ad13af4235b9778d538fdf9e43983ac9acfc1e25de55`.
- The exact source tree identity will be the harness commit; this handoff
  intentionally does not invent a commit or alter refs.

## Closed carrier

The existing ordinary `clip.set`, versioned by the current command path, is
the carrier. A transition SET requires one atomic `values` pair:

```json
{
  "transition": {
    "type": "<transition id>",
    "duration": "<positive authored seconds>",
    "revision": "<exact descriptor revision>",
    "params": "<optional complete literal params>",
    "<other keys>": "<opaque JSON>"
  },
  "elementRef": {
    "id": "<same transition id>",
    "kind": "transition",
    "revision": "<same exact revision>",
    "packId": "<selected pack owner when present>"
  }
}
```

Compiled-only `id`, `durationFrames`, `align`, and `incomingPolicy` are
schema-refused. Known selected properties use the exact retained declaration;
unknown nested values remain opaque. `schema_source` is required only for an
admitted project-pack transition and is hydrated through the existing document
pin path.

Explicit associated removal is `clear: ["transition", "elementRef"]`. It
requires the stored transition and every stored `elementRef`/legacy
`element_ref` spelling to match transition kind/id/revision, then clears both
spellings atomically. The existing `clear: ["transition"]` remains a
transition-only clear and preserves unrelated component/effect references.

## Recorded guards and repaired controls

- The destination's recorded `transition.predecessor` is the immediate
  same-track predecessor, stable by authored collection order for equal starts;
  other tracks are independent.
- SET admission matches Main's literal controls: predecessor end and target
  start must be within `< 0.001` seconds, and duration frames must fit the
  shorter adjacent clip with `+ 0.0001` tolerance. No clamping, renderer
  policy, successor policy, or new transition alias was added.
- The existing raw clip basis, rational FPS, source bindings, occurrence
  owner/map/window checks, opaque values, and strict v2 write/inverse/replay
  machinery remain unchanged.
- Same-reference selected project-pack `clip.set` updates join the existing
  retained selected-authority chain and must prove the original accepted P1
  source/snapshot. A caller-supplied later P2 is refused atomically. Explicit
  `clip.set-element` remains the reselection operation.

## Schema/floor scope

Only the existing `ClipSetArgs` definition gained transition, paired
`elementRef` clear, and `schema_source` fields. Definition/operation counts
remain 59/33. Floor tests strip only these transition additions and reconstruct
the exact 84fc schema and all prior published floors; no 48-definition/22-
operation schema was copied over the current source.

## Evidence

All commands used the worktree source plus the shared Runtime source on
`PYTHONPATH`; no shared dependency was modified.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider \
  --basetemp=/tmp/agt-transition84-probes \
  tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'transition'
  17 passed, 87 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider \
  --basetemp=/tmp/agt-transition84-authority \
  tests/sdk/test_timeline_transition_schema.py
  1 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider \
  --basetemp=/tmp/agt-transition84-scalar \
  tests/editing_conformance/test_recipe_clip_scalar_fields.py \
  tests/sdk/test_timeline_clip_scalar_provider.py \
  tests/sdk/test_timeline_commit_provider_scalar.py
  146 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider \
  --basetemp=/tmp/agt-transition84-authority-neighbor \
  tests/sdk/test_timeline_selected_param_authority.py
  27 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider \
  --basetemp=/tmp/agt-transition84-schema-neighbor \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/sdk/test_timeline_transition_schema.py
  57 passed
```

No full suite, HTTP, browser, renderer, live Runtime, normal generation,
release, pin, or activation was run. Runtime and App2 should ACK this exact
carrier, removal split, predecessor/fit guards, and retained-P1 behavior
before any consumer artifact work.
