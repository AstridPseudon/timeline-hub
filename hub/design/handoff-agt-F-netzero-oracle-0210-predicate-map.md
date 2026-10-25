# F-D86 net-zero oracle evidence

## Decision

Corrected only the net-zero inverse command-record oracle in
`tests/sdk/test_timeline_commit_provider_add_delete_runtime.py`.
The accepted authored record remains unchanged. The inverse record now requires
the complete sequential native pair:

1. `parent/clip:first-clip`: absent -> present, with the full `present(row)`;
2. the same ref: present(row) -> absent;
3. `created == [created]`, retaining the typed historical restoration fact.

This follows C0 `commit-v2.md` §2 (intermediate effects are retained even when
the final value equals the input), §2 provider-generated effects (ordered
native recorder facts remain alongside boundary projections), and §5 (inverse
uses sequential boundary states and preserves allocation/restoration facts).

## Predicate conservation

Unchanged: parameterization `[True, False]` and ids `net-zero` /
`replace-existing`; all imports, fixture inputs, AST branches, helper bodies,
Runtime/provider registration, request/base fields, command envelopes, track
and clip captures, opaque/literal row data, publication cardinality/history
prefix, accepted command echo, command-op ordering, authored `created` and
`writes`, final canonical-document assertions, idempotent retry, identity
collision refusals, reservation checks before/after undo and redo, reload
equality, immutable original record check, intervening-write refusal and
no-history-change assertion, durable restart/history equality, post-restart
reuse refusal, no-reexecution retry tripwires, and final service close.

Changed only in the `if net_zero` inverse-record block: the old coalesced
`absent -> absent`/empty-created expectation is replaced by the exact
sequential write pair and typed restoration `created` fact. The
`replace-existing` parameter and its body are untouched; its historical
Runtime auth failure remains a separate Runtime-owned seam.

## Genuine retained facts

- Original rehearsal XML: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-core-rehearsal-2234/evidence/OWN-REHEARSAL-SUITE.xml`
  SHA-256 `af1b309f43afcbcf6ba6953ad9d430c37b05b58b84e3eabe7bc712ff1bc49f7a`.
- Its net-zero failure shows the full retained absent -> present literal row
  at the old inverse assertion; it is not an absent -> absent record.
- Retained source-backed provider trace records the complete native inverse
  writes as `(absent, present)` then `(present, absent)` and retains the clip
  restoration `created` fact. No new fixture, source image, or authority was
  introduced.

## Checks

- `py_compile`: passed for the assigned test.
- Scoped Ruff: passed (`All checks passed!`).
- Scoped mypy candidate and `--shadow-file` baseline: both stopped before
  target checking on the identical NumPy `__init__.pyi:737` Python-version
  syntax diagnostic; no target-specific difference.
- `git diff --check`: passed.
- No pytest, collection, test/helper/fixture execution, service, build,
  browser, render, socket, or probe was run.

## Proposed existing behavior-log entry

“F-D86 net-zero native recorder oracle corrected: retained C0 sequential
inverse facts are absent→present(full literal row), present→absent, with the
typed restoration `created` fact; final document remains unchanged and the
coalesced boundary remains absent→absent. Add/delete/restart/redo,
identity-collision, ABA/intervening-write, no-write, ABI, and history
predicates remain intact. Replace-existing remains a separate Runtime auth
seam; no product/runtime change or functional qualification claimed.”
