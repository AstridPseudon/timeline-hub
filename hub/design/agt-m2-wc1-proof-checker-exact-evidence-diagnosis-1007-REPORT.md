# WC1 exact proof custody diagnosis

## Verdict

**QUALIFIED, bounded to the approved WC1 native media/outbox slice.** The
current landing preserves the approved two-test snapshot and the only
proof-source/candidate semantic delta is a checker-only route predicate
tightening. The retained HTTP result is still labelled as a prior result from
its recorded source tree; this report does not relabel it as a literal
exact-tree HTTP rerun.

## Exact identities

- Current landing: `9512cce40f58bcf081aec6185b3653f263cea799`, tree
  `649d170a74304c5838596ac4baa7c127e57af9fa`.
- Approved candidate: `c7e392f19b6e6b186c632ed050d8ea6e73b55a34`, tree
  `d6aba756208419b9bdfa17e11c7b08710ad5399c`.
- Retained central proof snapshot: result
  `.../tests/agt-m2-wc1-writer-only-final-assertion-repair-0927-wc1-selected-media-http-b92-normal95-integration-1021093022-11726/`,
  `snap: tree=444e09d77f9774d0d7864c188a8f36541bc08fd1`.
- Retained result: `2 passed in 9.16s`, with Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`.

## The one checker delta

The full central-proof-source to approved-candidate diff is one file, two
insertions and one deletion:

```diff
diff --git a/tests/editing_conformance/test_commit_runtime_parent_media_swap.py b/tests/editing_conformance/test_commit_runtime_parent_media_swap.py
index 65ed693d5..66ba1bf4c 100644
--- a/tests/editing_conformance/test_commit_runtime_parent_media_swap.py
+++ b/tests/editing_conformance/test_commit_runtime_parent_media_swap.py
@@
-        and ('/composition-revisions' in record[1] or '/publish' in record[1])
+        and (record[1].endswith('/composition-revisions')
+             or record[1].endswith('/publish'))
```

The proof-source parent checker blob is `65ed693d5469bb9344feb75ecabd91b5bca85ca2`;
the approved candidate and current landing both use the reviewed
`66ba1bf4c77da3a008f762df749c74866e0e77dd`. The delta narrows matching to the
exact terminal legacy writer routes. It does not change method filtering,
product-phase filtering, request capture, or any product assertion.

## Why the retained proof is applicable

The reviewed candidate source already contains the explicit positive
`GET .../composition-revisions/{accepted_revision_id}` assertion and the
forbidden product writer checker. The reviewed planted negative includes a
fixture-phase writer and immutable GET controls. The local compact matrix
also detected all eight `POST`/`PUT`/`PATCH`/`DELETE` × exact
`/composition-revisions`/`/publish` product combinations, while ignoring the
fixture writer, immutable child GET, nested revision path, and native
`/commit`; recorded tuples remained byte-for-byte unchanged.

Thus the old substring predicate and the approved terminal predicate produce
the same classification for the retained proof trace: the observed
revision read is a GET child path, the fixture writer is outside product
phase, and native writes are `/commit`. The approved candidate is qualified
without weakening any request, body, idempotency-key, base/media pin, guard,
outbox flight/restart/retry, receipt, reload, inverse/history, opaque, or
sibling assertion.

## Fixture/body/product-source comparison

- The occurrence fixture/body blob is identical in proof, candidate, and
  landing: `857fe815bd080ec4b999de89ee4425491968ca6c`.
- The parent test blob is the exact approved reviewed blob in candidate and
  landing: `66ba1bf4c77da3a008f762df749c74866e0e77dd`.
- Relevant selected-media product source is identical across proof,
  candidate, and landing: `astrid/sdk/timeline/sync.py`
  (`cd24d096...`), `astrid/sdk/client.py` (`0e14726a...`), and
  `astrid/sdk/timeline/_command_state.py` (`85d6d62c...`).
- The current landing changes only the two approved test paths relative to
  merge parent `c4b964f6a`; no product source, pin, fixture authority, or
  live caller was changed. Candidate/proof trees contain unrelated
  rendering/sheet paths not ported by the landing; they are outside this WC1
  selected-media dependency and are not used to claim whole-tree identity.

## Checks

Passed:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_legacy_composition_writer_checker_rejects_planted_product_write` — **1 passed in 0.20s**.
- Non-HTTP checker matrix/control probe — **8 forbidden rows detected; all controls ignored; input unchanged**.
- `git diff --check` — **passed**.
- Exact blob/tree comparisons — **passed**.

The first attempted compact test omitted `PYTHONPATH=/home/user/work/runtime`
and failed during conftest import with `ModuleNotFoundError: runtime_protocol`;
the corrected command above passed. No HTTP, native, body, full, browser,
render, or install run was made in this worker. The retained central HTTP
result remains the only actual HTTP evidence.

## Callers and next step

Live callers changed: **none**. The helper is test-local; no public or
production writer path changed. The mergeable source/tree is the existing
landing tree `649d170a74304c5838596ac4baa7c127e57af9fa`, with no additional
code port required. The broader WC1/store-writer question remains open as
stated by the landing report.
