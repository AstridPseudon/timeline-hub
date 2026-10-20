# Final native word-anchor acceptance review

**APPROVE the bounded source in `tl/agt-m2-word-anchor-acceptance-fix`,
`9f474fec9d28b7d2e20dd2d5058f40f672e246e9`, for additive composition.**
The two original source-boundary findings and complete-S2 schema finding are
resolved. This approves neither a published Agent/Runtime tuple nor a word-schema
freeze. No product changes are requested by this review.

The reviewer read PLAN, AGENTS, the prior rejection from
`tl/agt-review-word-anchor-native:design/agent-review-word-anchor-native.md`, its
external report/probes, and the authored-reference contract. The prior review file
is on that branch; it was not present at the analogous ORCH/design path.

## Original counterexamples and boundaries

The independent public-API reproducer selects the second stable `again` ID from
`occurrence:occ/clip:voice`, declaration `"again"`, without offsets:

| Case | Fresh result |
| --- | --- |
| Ordinary source | Accepts at `3.4701333333333335` seconds |
| Occurrence at 2 s, duration 100 ms | Refuses `bound word is outside the half-open occurrence interval`; complete resource and accepted history unchanged |
| Raw `voice.source_window={"from":20,"to":30}` | Refuses `word source requires an explicit supported source map`; complete resource and accepted history unchanged |
| Native removal of the bound occurrence | Refuses missing/ambiguous source; head unchanged |

Both original defects also have permanent normal-Runtime regression tests that
assert `invalid_anchor` / `refused`, unchanged resource/history, zero declaration
writes and unchanged declaration input. The native test file adds 81 lines and
removes none of its original passing assertions. The fixture changes only add
source-window/duration options and preserve the old defaults.

A selected word ending exactly at the occurrence end remains valid through A/B
selection, inverse, restart and revision-only restore. A selected onset at the
exclusive end refuses. Missing/nonfinite occurrence windows refuse before
recorded writes. A native source move, stale replay and inverse restoring an
invisible reference refuse; restoring the complete earlier valid revision works.
The adapter checks literal-source occurrence geometry before writing, and the
pure kernel independently checks the derived interval after evaluation. Raw
source maps refuse in both places. These are bounded literal-map checks, not a
new map codec or a renderer claim.

## Stable meaning and complete S2

Fresh key probes preserve same-echo A/B choices as different authored revisions
and content digests. Revision-only restore recovers the chosen IDs and timing
across restart. A fresh compiler process receives canonical JSON and verified
transcript JSON only. The exact-ID path survives stale/invalid/missing echoes
with text search replaced by a failing tripwire. First-use hydration retains V1;
a normal V2 update removing its words, restart, exact retry and a later unrelated
native commit continue to use V1. Accepted history supplies provenance, not word
selection or film meaning.

An independent comparison with the authoritative git object proves the canonical
schema equals **complete frozen S2 `26ef2bbb` plus exactly the unchanged original
`WordAnchor`, `ClipAnchorArgs` and `clip.anchor` conditional**. It has **50
definitions / 23 operations**. S2 raw SHA256 is
`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`;
candidate raw SHA256 is
`db6ac5f815abc76b5d39f60585832ba7ebf9f8e8b5876c3c80bdca21bdfe1723`.
All six permanent full-floor comparisons pass. Producer, selected-element,
recording, rebase and outbox implementations are byte-equal to S2; shared
commands/provider changes relative to S2 add the word operation/hooks and
first-use transcript hydration. No S2 replacement with the narrower word parent
is approved.

## Current kernel and required port discipline

At initial inspection integration was `01926d03`; it advanced during review to
`7970544b`, merging the independent facade fix `167012c4`. The candidate compiler
is byte-equal to both. Relative to the integrated evaluator, the word change adds
only raw `source_window` refusal and occurrence-interval tracking/checking.

The candidate still spells the new private helper `_number`. **Preserve the
already integrated `_timing_number` definition and every local reference when
porting the word changes.** Do not transplant the candidate evaluator over
current integration. A private composition of the exact candidate and exact
`167012c4` rename passes 86 facade/compiler/cycle/native-facade tests and all four
new native acceptance/window cases. The old candidate alone reproduces the known
facade identity failure; it is separate from the corrected word semantics.
`workers/agt-review-word-acceptance-final/notes/current-kernel-word-addition.diff`
contains the narrow evaluator addition against `7970544b`, preserving the rename.
No integration tree was changed by this review.

## Fresh evidence and limits

- Original counterexample/A-B/restore/no-search/V1/window key probes: **12 passed,
  42 deselected in 18.37 s**.
- Focused occurrence/window/schema-floor checks: **19 passed, 68 deselected in
  2.34 s**.
- Word candidate plus facade rename: **86 passed in 15.92 s**; native new cases
  on that composition: **4 passed, 50 deselected in 6.75 s**.
- Independent public acceptance reproducer and authoritative schema/source
  diagnostic: exit 0.
- Ordinary private Runtime generation and `--check`: exit 0; all 13 outputs
  independently match fingerprint
  `5f349e6d49be426dcb5e40d14cd710c4d04f0a3efcc7feb8346991c0435032cb`.

Runtime base is unpublished private `c0dcd3871d78c405184506eb6735565592498c77`,
base tree `5f86f0ef9ad6c4c5bec21f41a8a1781c6a687c6d`, normally regenerated from
the complete canonical schema. Historical fixture seed is
`80973d34ae10e498d7213c30287012c9876f4b1a`. These probes use real CAS,
main-v1 transcripts, normal provider registration and in-process Runtime services.
Historical data is published through its public API. There is no runtime raw
schema override, legacy SQL seed, PreparedProvider, fake acceptance or fabricated
receipt in the two counterexamples, independent reproducer or new boundary cases.
The older source-trim probe uses its explicitly test-local operation; it is not
claimed as native trim qualification.

As requested, reuse the prior independent **50 native Runtime passes / 453
portable-neighbor passes** and the implementation's subsequent preservation
results; do not rerun those entire files. No new concern requires broader testing.
Exact commands, logs, source preparation and the one setup correction are in
`workers/agt-review-word-acceptance-final/notes/report.md`.

No full/full* suite, make check, browser/socket/localhost lane, consumer generated
client pin, live transport, UI/CLI/sheet picker, preview/export parity, macOS or
document-deletion qualification was performed. No broad default compiler migration
or one-writer completion is claimed. Public tuple qualification and coordinated
normal generation/publication remain the orchestrator's next work, after additive
composition preserves current provider/kernel/producer/element changes. No task
blocker remains. This review writes only its authorized ORCH review/report files;
product, tests, pins, integration, ledgers and shared dependencies are unchanged.
