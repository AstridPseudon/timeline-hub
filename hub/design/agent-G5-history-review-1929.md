# G2/G5 retained sheet historical-basis review — 1929

## Verdict

**PASS for the minimal retained-history source repair.** The ordinary history
leaf is eligible for the orchestrator's merge decision after this review.
This does **not** approve G5 deletion/retirement, whole-G5 activation, P1, or
the original FOUR/first-node qualification. G5 remains DRAFT and P1 remains
NO-GO.

## Scope and source decision

Reviewed `697c8fd3b51562fb18e45dedecc56723984db2eb` against `89c38c9355f5d4bcc68597ec74e4729435a7a07a`.
The exact delta is three paths: `astrid/sdk/timeline/checkout.py`,
`astrid/sdk/timeline_sheet.py`, and the new six-case
`tests/sdk/test_g5_retained_sheet_basis.py`. There are 100 insertions and 3
deletions. `store.py`, commit/inverse sources, runtime lock, artifacts, and
the original Runtime-history test are unchanged.

The captured corrected-1907 closure and `cause.json` establish a product
cause, not a bad assertion or fabricated fixture: retained history rows carry
both revision and publication, but `find_version` previously reopened by
revision only. The two real construction paths differ only at
`/base_parent/publication_id`; the original head has
`txn-11c90075be6c4c8bb9e2627366f0fe4f`, while the unbound historical read has
that field absent. The repaired call passes the exact row pair through
`Checkout.open(..., publication_id=...)` to the existing `store.fetch_bundle`
and public closure reader.

The patch does not infer identity from equal bytes, substitute the current
head, alter `store.fetch_bundle`, weaken historical reads, change auth/source
ownership, or add a new approval gate. The existing reader continues to reject
an unavailable/wrong publication and verifies the exact closure, owner pins,
digest, and canonical source document.

## Evidence run

Collection was 143 nodes: six new retained-basis cases, 121 neighboring
history/sheet/current controls, and 16 authentic current-pair controls.

```text
PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-2a9e347f \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  --basetemp=$TMPDIR/agt-G5-history-review-1929/nonintegration \
  tests/sdk/test_g5_retained_sheet_basis.py \
  tests/sdk/test_timeline_checkout_history.py \
  tests/sdk/test_timeline_checkout_history_boundaries.py \
  tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_sheet_native.py \
  tests/sdk/test_remote_timeline_owner_scope.py \
  tests/sdk/test_timeline_checkout.py::test_first_draft_pins_the_fetched_bundle_for_edit_diffs
=> 127 passed in 14.57s

PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-2a9e347f \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f \
ASTRID_AUTHENTIC_LEGACY_ARCHIVE=/home/user/timeline-hub/hub/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  --timeout=30 --basetemp=$TMPDIR/agt-G5-history-review-1929/current-pair \
  -m integration tests/editing_conformance/test_current_pair_reader.py
=> 16 passed in 3.46s
```

The first non-integration attempt only failed during pytest setup because its
private basetemp parent did not exist; no test body ran. The parent was then
created and the same selector passed. No original FOUR, first-node, c271,
HTTP/browser/live-socket, full, redo, or prohibited historical Runtime test
was run.

Quality and integrity checks:

- Ruff ratchet: **2148 current = 2148 baseline**.
- Mypy ratchet: **1911 current = 1911 baseline**.
- New regression: Ruff clean; mypy clean.
- Scoped production diagnostics: only the inherited 7 Ruff / 1 mypy findings;
  no new diagnostic identity.
- Vendor lock, artifact manifest, and `git diff --check`: **PASS**.
- Credential-shaped scan: **0 findings**.
- Original body/source locks remain exact (`all_match=true` in the retained
  corrected-1907 packet); no original test body/assertion/recipe was changed.

Runtime identity was checked independently: imports resolve under
`/home/user/work/wt/rt-pin-2a9e347f`, whose actual HEAD is
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` and tree is
`f79a2355cfb39d9ada7721978bd20d5702105778`, including `auth.py` and
`timeline_commit_auth.py`. The stale configured `d9e2…` string is not treated
as execution proof. The new tests use the real detached provider commit path
and real public closure reader with immutable transport reads faked; they do
not claim a live detached Runtime transport or daemon qualification.

## Limits and next step

This is a source and bounded-behavior PASS for the exact retained sheet basis
pair. It is not approval of the broader G5 retirement, the original four
Runtime-authentic bodies, or P1. The manager/orchestrator may separately decide
whether to run the permitted original qualification; no such run is included
here. Recommended next step: merge this ordinary history leaf only through the
normal queue after orchestrator review, while keeping G5 deletions and
activation blocked.
