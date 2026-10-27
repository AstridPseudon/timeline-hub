# OPS H bounded findings

## Verdict and custody

The packet is valid documentary evidence, but L15 acceptance is **FAIL**.
The reviewer JSON used here is the authentic file at the actual author root:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-H-sprite-wholepath-2048/evidence/review.json`

The reviewer overwrote the author's `report.md`, `evidence/findings.md`,
`evidence/source-map.json`, `evidence/validation.md`, and `evidence/handoff.md`
and added `evidence/review.json` there. Those current files, plus the author
and reviewer raw `log.txt` files, were not modified or restored. Any original
author preimage not present in exact retained raw bytes is unavailable; this
packet invents none.

## Exact L15 source framing

- `astrid/sdk/timeline_restructure.py:59-166` performs renderer-normalized
  cut-safety checks. At `:816-830`, unsafe cuts disable cutting; at `:855-916`,
  an intact visual can be retained on a generated `-over` row and marked as
  `timeline_restructure_over`. This is consistent with shot-layering plan
  §§4.2/7 for clips that cannot be cut faithfully. It is static source
  evidence, not behavior proof.
- `tests/packs/rendering/test_sprite_scene_capability.py:14,32` imports and
  calls `project_shot_composition` in `prepared_props`. The managed production
  path is different: `managed_timeline.py:962-981` calls
  `project_runtime_parent_composition`, and `:1133-1158` uses that projected
  config for the managed render snapshot. The modified sprite SSR test is
  therefore not a production-caller proof. A separate passing sibling using
  the runtime projection does not transfer credit.
- Exact L15 removed
  `@pytest.mark.parametrize("host_project", ["0.0.13"], indirect=True)` from
  the broad cross-seam test at `test_sprite_scene_capability.py:147`; the
  marker appears instead on the separate half-frame fallback test at `:198`.
  The default fixture is `0.0.12`; the broad production `0.0.13` matrix is
  missing in L15. The retained 87-pass run cannot qualify that matrix.

## Retained observations and causal limit

Runs `22278` and `16353` each retain `86 passed, 1 failed`, with the broad
test failing at `intervals[0]`; run `23676` retains `87 passed`. The logs do
not print the case tuple, `plan()` reason, fallback identity/track, or a
rendered intact-fallback comparison. Therefore the empty interval is
source-consistent with a clip routed to the intact `-over` fallback, but the
exact causal case is **UNKNOWN**, not measured and not a behavior PASS.

The broad test's `intervals[0]` access is at L15 `:183`. The half-frame test's
fallback lookup and full-range comparison are at `:216-227`; that one case and
assertion do not replace the broad matrix.

## L16 and ownership boundary

`/home/user/work/wt/H-crosser-L16` is separate, dirty H-owned WIP. It is not
retargeted into L15 evidence and receives no L15 credit. L16 may already
address the known issues. H keeps all repair and integration ownership. This
packet proposes no product fix, new behavior, test, or source change.

## Contract boundary

`design/commit-v2.md` §§1-4 define v2 request/reply semantics, including
complete request bodies and accepted/merged/conflict/invalid/preview shapes.
The retained test-service `request` files are suite envelopes, not v2 request
bodies, and their results are not commit-v2 behavior evidence.

