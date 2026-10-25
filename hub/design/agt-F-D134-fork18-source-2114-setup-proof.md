# D134 setup proof

Result: finite `UNAPPLIED`; no target-file correction is faithful on the current
source.

The independent protected review (`agt-F-D134-root-review-2029`) passed. The
root-cluster packet identifies exactly 18 root-008 members, all `UNKNOWN`, with
`AuthoringBundleError`, first Agent frame `astrid/sdk/timeline/commit.py:1398`,
first Runtime frame `EXACTMISSING`, and no proven product fault. The exact member
list and immutable input hashes are recorded in `predicate-map.json` and
`source-manifest.json`.

The production trace is:

1. `capture_occurrence_fork` emits the registered `occurrence.fork` command with
   the original owner and reserved shot identity.
2. The native provider records the four ABI-1 bindings: the two collection-owner
   bindings, `fork.source`, and `fork.owner`.
3. `_commit_patch.finish` sees an active production request and appends physical
   `commit.effect` bindings for the step effects.
4. The reservation validator accepts ABI-1 only when the binding list is exactly
   the four native bindings. The extra physical bindings therefore reach the
   native schema refusal.

The genuine passing comparator is
`tests/editing_conformance/test_provider_occurrence_fork.py`. It uses the same
registered fork command and source fixture through the production provider, but
with the full C0/v2 request controls and the expected physical effects. It does
not supply an authenticated ABI-1 record and cannot substitute for root-008's
exact history predicates.

The available authenticated redo wrapper likewise creates a provider record from
the same active caller; it does not provide an existing accepted ABI-1 capture.
Changing the caller to fabricate or strip recorder history, bindings, receipts,
pins, sources, or allocations would violate the brief. Changing the active
binding production condition would be a product change outside the two assigned
files. The exact authored inputs and all assertions therefore remain untouched.

No live test was run: the protected operational route is owned by worker 2111,
and its published report identifies an exact missing fixture input.
