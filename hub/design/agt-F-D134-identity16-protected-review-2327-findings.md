# D134 identity16 root-004 protected source review

## Verdict

PASS for the finite source assessment and the two claimed setup-only deltas.
This is not a functional qualification: all 16 members remain `NOTRUN`.

The exact root-004 membership is 16 unique IDs, mapped once each. The
historical split is preserved as 11 `TEST_SETUP_OR_EXPECTATION_PROVED` and 5
`UNKNOWN`; product fault proved, functional PASS, retirement, and count
deduction are all zero.

## Delta decisions

Gate1’s `NORMAL_RUNTIME` changes only from the old history5 Runtime source
`ab1e4f6141987706132916e2da16477f5a019464` to the current Agent lock source
`f103bb46866999c961a8865636f2e66d544e0c9b`. The fixture still asserts the
schema digest and exact lock equality, then calls `use_runtime(commit=...)` and
loads the Runtime provider. The production-facing path remains the real
daemon/provider route: `TimelineSession`, Python `Checkout`, CLI command-file,
and `NativeSheet`, with the existing commit/undo/restart guards.

Prepared-video changes only `expected_runtime_source` and
`expected_runtime_tree` to the same current lock/provider tuple. The test
still derives `runtime_pin` from `vendored_runtime_commit()`, selects it with
`use_runtime(commit=runtime_pin)`, and asserts Runtime `HEAD` and `HEAD^{tree}`
exactly before entering the public managed-media/provider route.

These are authorized as setup-only because D139’s independent receipt records
the current normal source and 15/15 canonical consumer bytes unchanged from
the old source, and direct Git-object/hash checks reproduce all 15 equalities.
The lock match was not treated as sufficient on its own. The relevant provider,
validation, and Runtime test-fixture blobs are also byte-identical between
`ab1e` and `f103`. No observed command, transcript/media input, C0 envelope,
assertion, refusal boundary, or authenticated inverse pin was changed.

The Runtime `6634a17f3f...` inverse tuple remains exact. The seven inverse
members reuse the already homed inverse7/history5 evidence; no duplicate
ownership or false old-receipt retarget was introduced.

## UNKNOWN cases retained

Members 11–13, 15, and 16 remain `UNKNOWN_GATED` and `UNAPPLIED`:

- native vector `a` and `b`: in-process Agent fixture capture/equality, with
  no Runtime/provider identity evidence;
- retained1-shot cohort: public Runtime/provider route exists, but no
  authenticated accepted-record/source receipt authorizes a replacement tuple;
- stale-anchor recipe: the narrowed source window is authored topology, not a
  proven stale identity literal;
- stale-head provider test: `DetachedRealm` and in-process doubles, with no
  supported public Runtime source selection to retarget.

The protected root review’s missing first Agent/Runtime frames and missing
accepted-record/caller evidence remain missing; no source fault was inferred.

## Scope and conservation

The candidate is one commit over current normal Agent `41ad656529fa...` and
changes only the two allowed member files. Read-only AST normalization over all
seven allowed files is equal after normalizing only the old/new Runtime identity
strings. Assertions, raises, calls, assignments, control flow, input metadata,
command fields, C0 request/reply fields, and guarded inverse/ABA/redo/no-write
predicates are conserved.

The five UNKNOWN cases and the original source/evidence hashes are recorded in
`member-map.json`; the source, canonical15, and environmental checks are in
`source-manifest.json` and `validation.md`.

## Caveat

The shared Runtime worktree was observed at `0ca306d...`, while the Agent lock
selects immutable Runtime `f103bb...`. Accordingly, live `vendor_lock.py check`
against that shared worktree fails its expected-HEAD check. This is an external
worktree freshness issue, not a candidate-file delta; it was not changed here.
D140/Farm must resolve or explicitly bind that tuple before any functional
qualification.
