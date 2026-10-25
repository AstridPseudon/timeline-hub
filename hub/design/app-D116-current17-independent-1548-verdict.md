# D116/D118d current17 independent source review

Verdict: **FINITE_SOURCE_FINDINGS**.

The live Agent source at base `20177e66564f9f91735ed1a11bac821682d60edf` / tree
`68433c5f77be90063b1f43d3e8f1407346a50675` supports the submitted applicability
conclusion, but the supplied source map is not custody-qualified as written.
The map records a 65-character digest for `test_commit_runtime_scalar.py`:

```text
map:    691046ff5ac6919745c221ab992cb362b5153a8099f441c5d8dd57661351c9618
actual: 691046ff5ac691974c221ab992cb362b5153a8099f441c5d8dd57661351c9618
```

The valid 64-character digest is also present in the supplied D118 handoff and
other prior custody records. This is an input/report defect; no source change
was made.

## Applicability checks

- JSON parsed successfully.
- The exact-safe 27-row map minus approved D107 ten is exactly ordinals
  `1143, 1147, 1152, 1159, 1165, 1171, 1180, 2913, 2923, 2927, 2940,
  2958, 2996, 3649, 3651, 3653, 3654`.
- All 17 selectors match the safe-map selector strings and exactly one live AST
  function; both `[False]`/`[True]` parametrized pairs were checked.
- The historical source remains on the `m1.film` route with authored
  `word:word-1`; no fixture, manifest, archive, pin, original test, or body
  was changed.
- `current_word_baseline_fixture.retained` is exactly the alias of
  `native_word_anchor_fixture.current_retained`. The current seed uses the
  genuine registered Runtime provider, pinned transcript/document input, target
  `parent/clip:card`, declaration `"again" in line #2 +1f`, and
  `clip.anchor` followed by retain-and-clear.

## Per-selector preserved purpose and missing current evidence

The following is source evidence only. It does not approve replacement,
retirement, or functional qualification.

| Ordinal | Preserved authored purpose/timing/grouping | Exact missing current topology/caller evidence |
|---:|---|---|
| 1143 | move `on=1`; queued trim `(1,4)`/hold `3`; lost ACK/restart; disjoint `music-other on=2`; suffix; reload; undo/redo/guard | current authenticated `music-bed` binding and current media/music-bed/music-other topology |
| 1147 | same move/trim sequence with touching peer trim `(0,5)` and conflict/no-write | same target topology plus an independently current touching-peer conflict baseline |
| 1152 | commands-file CLI ingress; opaque `[null,false,0]`; authored unchanged setter; clear; undo; conflict against first publication | authenticated current target/document carrying the opaque parent field; current commands-file caller path |
| 1159 | Gate3 occurrence-free/text-card setup; renderer-off tripwire; `on=1`; reload/undo; exact visualize-unavailable reply | pinned/bound current occurrence-free text-card topology; renderer/capability assertions remain unchanged |
| 1165 | NativeSheet export/apply to `1`; lost ACK; immutable draft; trim suffix `(1,4)`; reads/bindings; restart without recapture; disjoint peer/rebase | current target binding plus NativeSheet adapter input over the same authenticated document |
| 1171 | same sheet sequence with touching peer trim `(0,5)` and conflict/pending state | independent current target/peer conflict setup; not covered by 1165 |
| 1180 | checkout-first sheet refusal while ACK is pending; exact draft/outbox bytes; retry key/body; original-basis refusal | authenticated current target plus current sheet pending-intent refusal setup |
| 2913 | trim-ready media; `clip.set` clear `asset`; exact rationale/key/body; lost-ACK retry; undo to original | current pin/binding carried through the trim-ready parent variant; current seed has no music-bed target |
| 2923 | authored `crossfade/.25`; disjoint peer move; clear transition; retry; peer preservation; undo | same current authenticated pin/binding on the transition variant; do not substitute 2913 |
| 2927 | peer move; exact trim literals `1.0000004`/`4.0000006`; quantized result; lost ACK/rebase; undo | current pinned/bound trim variant retaining exact numeric inputs and target topology |
| 2940 | speed `2`; split at `1`; right id `music-bed-right`; created list; right `from=2,to=5.5,hold=3.5`; peer label; rebase/undo | authenticated split variant retaining source window/speed and target binding |
| 2958 | occurrence-free delete; exact `clip.delete`; lost ACK/rebase; peer move; absence; undo restoration | current pin/binding on the occurrence-free variant; no blanket transfer from ordinary seed |
| 2996 | duplicate display ID across parent/occurrence; unqualified refusal; qualified parent move plus mixed text refusal; draft/outbox/history unchanged | authenticated current duplicate-owner closure; this negative topology is not covered by positive M1 path |
| 3649 | grouped `track.create` V3 opaque `[null,false]` plus music-bed move; exact grouping/readback; reload undo/redo | current pinned/bound baseline retaining full parent topology and grouped target; seed only has card/voice |
| 3651 | move `1`; parent-track label `Music`; disjoint `music-other=2`; guarded inverse removes only label; closure/media pins preserved | authenticated current target binding plus label/move music/music-other topology |
| 3653 | native CLI empty-label lost ACK; Python clear-label suffix; restart retry; disjoint move; exact bases/keys; undo | current pin/binding plus native CLI-to-Python suffix setup; Python-only route is insufficient |
| 3654 | lost-ACK move; scalar track label; restart handoff; exact serialization/readback; undo/redo; occurrence params with literal null/opaque JSON | current pin/binding on m1 target plus occurrence-parameter topology |

The current seed is therefore a shared authenticated source/pin/provider seam
only. It is not an `m1.film` transplant and does not establish selector
completeness, retirement, or functional GO. No pytest, Runtime service, socket,
browser, replay, full, family, P2, P4, probe, collector, build, profile, or
acquisition run was made.

Evidence files:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D116-current17-independent-1548/evidence/verdict.json`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D116-current17-independent-1548/evidence/source-custody.json`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D116-current17-independent-1548/evidence/commands-results.md`
