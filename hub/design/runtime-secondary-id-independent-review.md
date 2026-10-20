# APPROVE — Runtime secondary-ID independent review

Reviewed `ade60f3225aa3b6b6db1aee683bc33e09084a4fa` (tree
`06a68e47968f1c64774e05608e004d8edbf7ca65`) relative to recovered carrier
`3c917378a6dc2b48362fd1bc152cb13a5fd6b84a`. This is an internal source
review only; it is not activation, merge, release, or native/public-wire
qualification.

## Verdict

**APPROVE the recovered source fix.** The removed `item_id != id` assertion was
a false refusal. The patch is minimal and preserves the intended identity
boundary:

- `item_id` is canonical, with `id` used only when `item_id` is absent;
- a distinct secondary `id` remains opaque payload and is not allocated,
  projected, remapped, or treated as authority;
- duplicate/missing canonical identities still refuse;
- global `shot_items.id` occupancy, retained-revision SQL occupancy, source
  joins, materialization ownership, and authenticated source proofs remain in
  place.

The Runtime paths agree with Main and the reviewed Agent codec. Runtime
validation/projection use the canonical selection in `service.py`; recovery
uses the same selection in the store and materialization join. The SQL
`COALESCE(item_id, id)` lookup is only a canonical-identity lookup. No
`foreign_item_id` or other opaque payload field supplies allocation authority.

The new ownership controls are appropriately narrow. They cover missing,
equal, and distinct mirrors; the distinct case uses a secondary ID equal to a
pre-existing bystander ID and verifies the canonical destination projection
while leaving the bystander ownership intact. The accepted canonical document
equals the complete input item, so raw item fields are retained. The separate
occupied-canonical test uses a free secondary ID and still refuses before
persistence, with the full Runtime snapshot unchanged. Existing duplicate,
empty/malformed, cross-owner, and retained-ID refusal controls remain.

The unchanged audit probe is the stronger preservation evidence: current2cb
accepted both distinct-secondary cases while recovered3c917 refused them; the
probe found no source/bystander row theft. Its full SQL/CAS and closure checks
showed source and bystander rows, raw payloads, old closures, and exact retry
state unchanged except for normal acceptance tables on positive copies. The
probe was not edited by this change.

## Evidence

Fresh local runs from this review worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-m2-secondary-id-independent-review-ownership tests/test_timeline_projection_ownership.py
51 passed, 2 deselected in 41.77s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-m2-secondary-id-independent-review-join tests/test_timeline_materialization_join.py tests/test_timeline_materialization_authority_review.py
141 passed, 2 xfailed in 91.41s

git diff --check
passed; assigned worktree clean
```

Central named integration evidence for this exact source tree:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/test_timeline_commit_integration.py
9 passed in 16.60s

env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -m integration tests/test_timeline_materialization_continuation.py
17 passed in 25.73s
```

The two original schema-boundary tests in
`tests/test_timeline_materialization_join.py` remain strict xfails. Public
013 still lacks typed item references, so the native typed source/join positive
is not claimed. No public schema, codec normalization, ID renaming, pin,
publication, or full suite was performed.

## Qualification boundary and next steps

This approval covers only the recovered Runtime source and its internal
controls. Activation/merge/release still require the matched reviewed Agent
full-S2 schema/core/version and native qualification, including a normally
generated typed item-ref artifact. Keep the two strict xfails until that
carrier exists and is independently qualified. Do not cite this review as
proof of native/public-wire support or as a substitute for the cross-repo
qualification gates.
