# D134 root-004 identity16 finite source assessment

## Result

The exact root-004 enumeration contains 16 unique members, mapped once each.
The retained root-review2029 evidence has `EXACTMISSING` for both the first
Agent and first Runtime frame, so the retained `AssertionError` cannot prove a
product fault. The settled split is 11 `TEST_SETUP_OR_EXPECTATION_PROVED` and
5 `UNKNOWN`; product fault proved is zero and functional status is `NOTRUN` for
all 16.

## Source decision

The historical 11-case source work is present in the current Agent head via
the reviewed history5/inverse7 blobs from `a6703bba8e` / `8cd663b6a5`.
However, current integrated applicability was checked before treating those
blobs as final: D139 changed the current normal `runtime.lock.json` source
from Runtime `ab1e4f614198…` to qualified Runtime
`f103bb46866999c961a8865636f2e66d544e0c9b` (tree
`5d0cedf2e5134acf895e8d43191cc5fdc09f9883`). Its independent receipt says
all 15 canonical consumer bytes are unchanged from ab1e, so this is a
source-selection correction, not a product or pin change.

Accordingly, only three setup literals serving four members changed:

- Gate1's shared `NORMAL_RUNTIME` now names `f103…`, matching the current lock
  and `use_runtime(commit=NORMAL_RUNTIME)` selection. The schema, frontend
  routes, transcript/media inputs, assertions, and roundtrip predicates are
  untouched.
- Prepared-video's `expected_runtime_source` and `expected_runtime_tree` now
  name the same current lock/provider tuple. Preview, accept, retry, invalid,
  conflict, inverse, no-write, request, and media predicates are untouched.

The seven inverse members remain exactly on the reviewed Runtime `6634…`
tuple, because that is their observed authenticated inverse source boundary;
they must not be silently rebound to the normal lock. The other five members
have no retained evidence authorizing a faithful setup identity delta:

- two native vector members compare an in-process Agent capture to a fixture;
- the retained1-shot cohort member uses a public Runtime/provider route, but
  has no accepted-record/source identity receipt for replacement;
- the stale-anchor member's window mutation is authored topology, not a stale
  identity literal;
- the provider member uses an in-process `DetachedRealm` and ABI-only doubles.

These five remain `UNKNOWN_GATED` and `UNAPPLIED`. No assertion, authored
input/media/transcript/topology, command envelope/base/reads/idempotency field,
guard, inverse, ABA, redo, no-write predicate, provider import, shared fixture,
generated file, lock file, or product source was changed.

Original protected review, intake, inverse7, and history5 packets remain at
their existing paths and were not overwritten. Independent protected review
of this finite assessment remains the next handoff; no functional credit is
claimed.
