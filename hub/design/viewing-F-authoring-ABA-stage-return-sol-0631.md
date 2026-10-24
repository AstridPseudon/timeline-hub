**PARTIAL — diagnosis complete; production qualification remains FAIL.**

Changed only [test_authoring_item_observation_boundary.py](/home/user/work/wt/vw-F-authoring-ABA-stage-return-sol-0631/tests/editing_conformance/test_authoring_item_observation_boundary.py:153): added four source-boundary diagnostics and two passing source-copy comparisons. All existing 89 controls remain, including four unmarked positive failures. Production code and original tests, including the 59 ABA assertions, are unchanged.

Agent base: `71e8231debe39f1be574a9ed4a40537409e889ef`  
Runtime: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`

**Source findings**

The caller remains connected: publish emitter → `capture_occurrence_swap_media` → `TimelineSession.undo` → provider-loaded `AcceptedRecords` → inverse item translation → `CommitPatch.after` → Runtime sequential/stage validation. The exact accepted records reach completed projection; no missing-authority forwarding repair is justified.

Two independent Runtime representation limits are confirmed:

- **Item identity:** historical native captures address `item_id:item-1`. The published copied shot addresses `item_id:shot-item-placement-cb1bf5d05853ca0713af2d9450cfbb2f3d41bbda49e6b17c2d62b854e0b1c993`. Agent resolves their exact placement-local correspondence. Current spelling observes the item but fails strict historical membership at [timeline_commit_auth.py:1160](/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py:1160). Restoring historical spelling passes membership but fails sequential observation because that item path is absent.
- **Shared-root restoration:** independently, ordinary media without items reaches [timeline_commit_auth.py:1332](/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py:1332). The original shot/internal roots exist at both inverse boundaries because `occ-b` retains them. Only `occ-a` returns to them. Subsequent checks also require singleton ownership and an unchanged shot ID, whereas authenticated history contains both owners and reversal of a placement-copy identity.

| Control | Native range | Effect range | Result, accept and preview |
|---|---:|---:|---|
| Shared native item | `[0,6]` | `[0,4]` | Membership refusal |
| Shared ordinary media | `[0,5]` | `[0,4]` | Exclusive-turnover refusal |
| Single occurrence | Complete | Complete | Pass |
| Retained source-copy inverse | Complete | Complete | Pass through the same Runtime validator |

New diagnostics preserve complete recorder copies, reads, reversed writes, ranges, owner lists, revision/digest pins, sibling edges, stored local IDs, and unchanged sibling images. Existing corrupt mapping, foreign owner/revision, order, range, history, equal-byte retargeting, and ABA negatives remain passing.

**Runtime owner handoff**

The existing owner seam is [TimelineCommitStore._inverse_stage_history](/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:855), feeding `_inverse_stage_history`, `_inverse_stage_ranges`, and `_inverse_stage_boundaries`.

The smallest safe **preparatory** hunk I can justify makes the exact historical input available privately:

```diff
--- a/runtime_protocol/timeline_commit_store.py
+++ b/runtime_protocol/timeline_commit_store.py
@@
-        return {publication: self.history_entry(project, timeline, publication, allow_archived=allow_archived)
-                for publication in publications}
+        history = {}
+        for publication in publications:
+            entry = self.history_entry(
+                project, timeline, publication, allow_archived=allow_archived)
+            previous = entry.get("previous")
+            if entry.get("intent") != "recorded" or not isinstance(previous, dict):
+                reject("history_unavailable", "inverse source input is unavailable")
+            history[publication] = {
+                **entry,
+                "_inverse_source_input": self.revision_closure(
+                    project, timeline, previous["revision_id"],
+                    allow_archived=allow_archived),
+            }
+        return history
```

**This hunk is unapplied, untested, and insufficient alone.** Runtime still needs source-authenticated item-site projection and per-consumer restoration to retained roots, preserving strict ordered membership, source pins, sibling edges, sequential values, and complete effect coverage. These legacy native records do not contain `materialization.source` allocation dependencies. I cannot honestly supply a complete qualified Runtime repair from this bounded Agent investigation.

**Validation**

All Python commands used worktree-first `PYTHONPATH="$PWD:/home/user/work/runtime"`, `PYTHONDONTWRITEBYTECODE=1`, and private scratch `TMPDIR`.

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_authoring_landing_projection.py tests/editing_conformance/test_headless_root_mirror_effects.py tests/editing_conformance/test_authoring_undo_projection.py tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_authoring_item_observation_boundary.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py
# 4 failed, 275 passed in 29.60s

/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_authoring_item_observation_boundary.py
# Final focused tree: 4 failed, 91 passed in 10.49s

/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/inverse.py astrid/sdk/timeline/native_occurrence_media_commands.py tests/editing_conformance/test_authoring_item_observation_boundary.py
# All checks passed

/home/user/work/venv-agent/bin/python -m mypy --cache-dir "$TMPDIR/mypy" --follow-imports=silent astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/inverse.py astrid/sdk/timeline/native_occurrence_media_commands.py tests/editing_conformance/test_authoring_item_observation_boundary.py
# Success: 4 source files

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
# ok runtime.lock.json

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# artifacts.json is current

git diff --check
# passed
```

No Runtime edits, guard weakening, full/live/browser runs, or original-packet qualification. Prior 0622 supplied WIP/raw logs, not a D30 report.

Recommend independent review of these source facts, then a Runtime-owner repair before further qualification. `commit-msg` and bounded-completion `DONE` were written.