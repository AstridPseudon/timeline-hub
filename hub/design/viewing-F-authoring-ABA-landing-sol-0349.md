**FAIL / BLOCKED — mismatch reproduced; repair requires unassigned source plumbing.**

Base: `8657e83653f48c935f52f209516456bcb5a36282`. Added only [test_authoring_landing_projection.py](/home/user/work/wt/vw-F-authoring-ABA-landing-sol-0349/tests/editing_conformance/test_authoring_landing_projection.py). No production functions or existing tests changed.

The offline accept/preview cases exercise `RuntimeCommitService.commit → execute → CommitPatch → private capture → accept/preview`. They persist complete capture/prepared values before enforcing Runtime’s exact output comparison.

The causal difference is:

- Boundary projection calls `document_from_bundle` without selected inverse records, retains introduced media `sha256:222…`, and derives parent revision `authoring-parent-revision-6acb…`.
- Preparation supplies authenticated `AcceptedRecords`, removes that introduced pin, and restores the complete baseline at `parent-1`.
- The positive authority control passes with those records; an unbound list of identical recorder rows is rejected.

This reproduces the **13559 failure class** using existing offline fixtures. These values are **not the missing original packet**. No repaired newGREEN result is claimed.

The passing legacy publication/undo path reaches the correct final compiler without exercising this v2 private-output comparison. Contract request/reply shapes, six-key capture, Runtime checks, original oracle, materialization and reorder/history behavior remain unchanged.

Agent R1/R2 owns the required forwarding seams; coordinate with Agent0339. Proposed hunks, **not applied**:

```diff
--- astrid/sdk/timeline/commands.py
+++ astrid/sdk/timeline/commands.py
@@
-        metadata.after(ctx)
+        metadata.after(ctx, inverse_records=inverse_records)
```

```diff
--- astrid/sdk/timeline/_doc_patch.py
+++ astrid/sdk/timeline/_doc_patch.py
@@
-    def __init__(self, bundle, *, source_bundles=()):
+    def __init__(self, bundle, *, source_bundles=(), inverse_records=()):
@@
-        self.document = document_from_bundle(bundle, source_bundles=source_bundles)
+        self.document = document_from_bundle(
+            bundle, source_bundles=source_bundles, inverse_records=inverse_records)
```

The accompanying `_commit_patch.py` change must carry that exact selected object into the completed inverse boundary, step output and private output projection while preserving intermediate stage boundaries. Copying prepared output into the carrier would conceal the missing authority.

All commands used `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime"` and `/home/user/work/venv-agent/bin/python`:

```bash
-m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 \
  --basetemp="$TMPDIR/acceptance-final" \
  tests/editing_conformance/test_authoring_landing_projection.py \
  tests/editing_conformance/test_authoring_undo_projection.py \
  tests/editing_conformance/test_private_sequential_capture.py \
  tests/editing_conformance/test_provider_step_undo_v2.py
```

**2 failed, 51 passed in 7.14s.** The two new parity cases remain RED. Existing source/ref/history/owner/digest/range/ABA controls passed.

```bash
-m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 \
  --basetemp="$TMPDIR/media-final" \
  tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_whole_payload_read_allows_exact_undo_redo \
  tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_payload_still_guards_all_other_input
```

**5 passed in 1.31s.**

```bash
-m ruff check --no-cache astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/_commit_preview.py tests/editing_conformance/test_authoring_landing_projection.py
-m mypy --cache-dir "$TMPDIR/mypy" --follow-imports=silent astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/_commit_preview.py
scripts/vendor_lock.py check runtime.lock.json
scripts/artifact_manifest.py --check
git diff --check
```

All passed; mypy reported **zero diagnostics**.

Commit message and `BLOCKED` written; no `DONE`. Next: Agent expands ownership for the forwarding repair, reruns these controls, then owns the sole next original live qualification. No live/full/browser run or Git mutation occurred.