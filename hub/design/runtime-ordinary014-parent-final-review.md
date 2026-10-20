# Runtime ordinary014 parent final-cohort review

## Verdict

**APPROVE for the reviewed unpublished candidate; release-ready only after the
test-only current-integration delta is forwarded.** No adoption, publication,
pin, or activation is authorized by this review.

## Reviewed identity

- Candidate: `tl/rt-m2-ordinary014-parent-actual-current-finish`
- Commit: `616d2111f35937f311330ffebc8610d21bf80f74`
- Candidate tree: `8e7b22f073b4ff3f21e684af9cf853b07672ea2a`
- Parent/base: `d1ea66bb749ce4f696fec440eb6dc0b5ad86bd87`
- Base tree: `3bf3ac159580cece24e3321ffc6c3a44b42bf67b`

The candidate diff is limited to the approved ordinary014 generated/artifact
cohort, the frozen-union contract test, and the two parent-boundary test
changes. All 20 generated/artifact paths match the approved `a0dca169…`
producer blobs exactly. No private613/392 material, new wire surface, release
pin, or product implementation change is present.

## Contract and fixture checks

Read-only immutable-object checks passed:

- `contract/artifacts.json`: 75 entries, zero declared-byte/hash mismatches;
  artifact version `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`.
- Shared command schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
  55 definitions and 29 operation branches; the Runtime bundle embeds the
  same schema.
- Runtime contract version: `0.2.14`.
- `tests/fixtures/published-command-schemas/agent-26ef2bbb.json` is byte-
  identical to the base public013 fixture (`sha256:a6f1aaa9…a190ef`).
- `contract/artifacts.json` SHA-256:
  `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.

## Parent-boundary assertion review

The target changes the current-schema refusal test to an explicit frozen
public013 fixture validation of `intent.ownership == "parent"` against the
`["shared", "occurrence"]` enum. It removes the private schema-boundary
exception helper and does not weaken the refusal.

The ordinary014 parent-swap positive keeps the original command construction,
commit, accepted/rebased status assertion, and canonical parent-asset
assertion. Its only boundary change is direct execution through the ordinary
0.2.14 provider; it is not marked xfail or skipped. The unrelated retired
direct-route xfail remains unchanged.

## Existing exact evidence

No unchanged suite was rerun, per the brief. The exact central evidence already
recorded for this committed candidate is:

```text
env ASTRID_RUNTIME_CHECKOUT=$PWD \
    ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-7b3e1205 \
    PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-7b3e1205 \
    PYTHONDONTWRITEBYTECODE=1 \
    /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
    -m integration \
    tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_replaces_parent_media \
    tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_refuses_parent_ownership_on_public013_schema
```

Result: **2 passed in 2.65s**, on candidate tree `8e7b22f…`; the native parent
positive executed and the public013 refusal executed separately. No deselection
or xfail was involved.

The following are separate exact proofs and are not relabelled as proof of
this Runtime candidate:

- App Gate 5 normal014: `1020195447-8973`, **1 passed (32.4s)**, exact
  Agent3c4/Runtime202/a0/f021/schema6ba/Composition13 tuple; lost ACK, newer
  local intent, exact retry, restart, undo, and zero-legacy traffic.
- Agent registered native cohort: `1020194213-7012`, **2 passed in 300.96s**,
  exact Agent7b3 source with Runtime7d and Composition13; registered proposal,
  requester/outbox retry and restart, historical render admission, CAS/ffprobe,
  and guarded undo.

Those App/Agent results are corroborating consumer proofs only. They do not
change the reviewed Runtime candidate identity or authorize adoption.

## Adoption prerequisite

Current integration later advanced to `a020a1c77a07aa657efb60b0442450209e55e470`.
Relative to base `d1ea66b`, that merge contains only the test file and the
test-only commit `5988a3b38293a82175052e84a2717ae5578b61dd`, adding
`test_rt02_project_shot_crud_native_replacement_retries_after_restart`.
The Runtime product guard/history files remain byte-identical to the base, so
this is not a wire or product change. Forward that test-only delta onto the
ordinary014 candidate and qualify the resulting adoption tree before
adoption. Do not treat the current `a020` merge as already qualified for the
ordinary014 generated cohort.

No full, render, browser, pin, publication, or adoption operation was run.
