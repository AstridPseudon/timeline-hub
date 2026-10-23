# P4 first new seam: faithful expected-plan correction

Result: **test-boundary mistake, independently reviewed PASS**. No product defect found at this seam. Only `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` changed: reconstruct the provider's input from the original verified `base_document` before executing the expected plan. The full recorded request and original evaluated head remain unchanged. No production/helper/schema/client/generated/pin/lock/suite/launcher/fixture edits; no deletion or dependency ancestry import.

## Exact source

- Agent base commit: `d8ab46e235e1ab5d2a1f9f9a37e0508235c5b2de`.
- Agent base tree: `c591008824526acd614df4afb3bbd3137c5b9edb`.
- Candidate tree (calculated from Git tree encoding without writing Git objects): `b07b812ac26d793f26b2edf37efd724d94a0ac3a`.
- Candidate test blob: `033482ec2b94c5ae4a6b5c456e2d9fab3f454022`.
- Candidate test SHA-256: `8239ad0c3ac7de05d7ab0efac7b12c34532df33f7f22f33c9c270f0aeb30f213`.
- Runtime source: `/home/user/work/wt/rt-pin-34eac004`, commit `34eac0041b0891e9011966b39bcbd26053fde5bc`, tree `9853574865f25e08284e82ffb26c0bdecaa16a30`, matching Agent `runtime.lock.json`.
- Historical service run: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-P4-show-fixed-source-port-0539-p4-v2-http-nodes-1023054639-18513/`. Complete `log.txt`, `snap`, `request`, and `summary` read. Source tree is the exact Agent base above. Run failed at line 231 after its accepted/canonical/steps/receipt/show/history metadata assertions. The old log truncates nested difference output; its execution snapshot is deleted.

## Complete difference and cause

The offline actual-provider differential found exactly one missing key, with every other nested value equal:

`records.commands[0].dependencies[1].pin.parent.publication_id`

Old oracle: `txn-52ed09cc24884ce5a404669b1a6b66b8`; authentic persisted recorder: key absent. The dependency is `key: move.images`, `kind: entity`, `policy: exact`. Both sides retain `revision_id: p4-cli-sheet-baseline` and `content_digest: sha256:4c26f78a127e0e66f8293ada611c71ed0cc575553d5e78f15bbd0de00ac2268f` (also the parent digest visible in service18513). This publication ID is the fresh offline witness's real seed receipt, not a reconstruction of the deleted run.

Actual path:

1. Production CLI `cli_native.commit_edit` opens public `TimelineSession`; `NativeSheet.load(...).apply` calls `commit_many` with `via=sheet`, label and per-command sheet steps. Runtime `service.commit_timeline` validates the request and scope, binds authenticated publisher/invocation/hash, and enters `CommitExecutionCoordinator` and `RequestCommitPort`.
2. Provider `RuntimeCommitService.commit` (`commit.py:899`) calls `_load` (`:417`). The port authenticates base ancestry, reads `revision_closure`, and the provider returns `bundle_from_document(document)`. There is no client publication annotation in that bundle.
3. Public `RemoteTimelines.open_bundle` (`_remote_timeline.py:119-158`) separately authenticates the publication/receipt, attaches `_runtime_document`, and adds `base_parent.publication_id` for the caller. This client-facing annotation is correct and remains explicitly checked in the test.
4. `capture._provenance` (`capture.py:105`) deep-copies `base_parent` into `move.images`. Executing the oracle on the public annotated bundle therefore invents an extra nested dependency field relative to the actual provider input.
5. `commands.execute` records effects/bindings/dependencies; `_commit_preview.prepared_records` copies the complete recorder. `RequestCommitPort.accept` and Runtime auth/store validate it. `TimelineCommitStore._publish` stores canonical `records_json` and an event `records_digest`; `history_entry` calls `_verify_accepted` before returning it. Runtime does not strip this publication key: it was never present in the provider's bundle. The discrepancy predates persistence/JSON normalization.

Correction: `execute(bundle_from_document(base_document), ..., commit_request=request, evaluated_head=base_head)`. The immutable original closure and full original pair remain bound through request/head and binding boundaries. No IDs are updated to a latest head, and no dependency, binding, metadata or guard is stripped from an actual record. Full `item["records"]["commands"] == expected_plan.records` remains intact, as do complete steps and canonical-document equality.

## Offline diagnostic and results

Bounded diagnostic source: `/tmp/w-e8c65da2e2/records_witness.py` (SHA-256 `21cec77916e0c29e01891a389c79316a758632c43626ad56371078549d4b8ac5`). It initializes a private fresh realm, registers the actual fixed provider, reuses `_seed_initial_bundle` with the original `initial_bundle` and trusted seeding helper, captures the same a0→5 command, and supplies the complete sheet request shape (scope/base pair/commands/label/steps/merge/source/dry_run, reads omitted). It directly invokes `RuntimeService.commit_timeline`, thereby using the actual coordinator, request port, authorization callbacks, provider, auth validation, durable SQLite acceptance and authenticated history read. No HTTP handler, daemon, sockets or integration test body is executed. It compares persisted complete records recursively to the old and corrected expected plans.

Exact command, exit 0:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-e8c65da2e2 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python /tmp/w-e8c65da2e2/records_witness.py > /tmp/w-e8c65da2e2/records-witness.log 2>&1
```

Result: exactly the one difference above; `persisted_records == corrected.records`; result/history/recorded steps all equal corrected steps; old/corrected/result canonical documents equal; history previous equals original base; 11 actual authorization callback checks. Full context includes request, base document, both input bundles, actual result/history, both full record arrays and recursive differences:

- `/tmp/w-e8c65da2e2/records-context.json`, SHA-256 `a2066e63119debe00a8daf867ce9092c8df67dbad5533ad784317e5f93a2caca`.
- `/tmp/w-e8c65da2e2/records-witness.log`, SHA-256 `957414698bffd50fb331326d294f33c1c93980881d88dd73cbcfcafac9098433`.

The old public annotation is reproduced from the inspected production boundary; it is not supplied to the authoritative provider. The fresh witness cannot recover byte-identical ephemeral request IDs/principals from the deleted service snapshot. Its full request shape/command/fixture/source and original parent digest match the historical seam; the exact cause is independently confirmed by code and the full differential.

## Required checks

Run from `/home/user/work/wt/ap2-P4-history-records-sol-0548`:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-e8c65da2e2 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-34eac004 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q -m integration tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
```

Exit 0: exactly **1 test collected** in 1.04s; existing warning `Unknown config option: timeout`. Collection only, no body run.

```sh
ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
mypy --cache-dir /tmp/w-e8c65da2e2/mypy-cache tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
git diff --check
```

All exit 0: Ruff all checks passed; mypy no issues in 1 source file; clean diff check. Private cache used. A read-only AST comparison of every `ast.Assert` against HEAD found all **66 assertion expressions unchanged**; `git diff --name-only` contains exactly the allowed file. Existing a0→5, b0/café/order/raw/full authored closure, accepted/request/steps/effects/physical bindings/dependencies, receipt, show/history/head constraints remain. No undo, merged/conflict/invalid, or neighbouring tests changed or executed; their existing constraints are untouched.

## Independent review, limits, owner and next step

Explicitly requested independent Luna review `/root/luna_review`: **PASS** after read-only inspection of the candidate diff, full test body, production `_load`/public reader path and supplied full offline context. Review states that original assertions remain, the exact full records comparison is retained, and this does not establish an HTTP pass. Review response is saved alongside this report as `review.md`.

Classification owner: P4 proof/test lane (ap2). No source-owner fix required for this mismatch. No blockers to this bounded classification/correction task. No HTTP/live/socket/service/full/browser/build run was launched or requested. No claim of P4 completion, downstream HTTP assertions, ten-note/undo qualification, or broader integration success. Next: orchestrator may stage this independently reviewed test-only delta and separately authorize the exact single HTTP node on the candidate tree; stop at its next actual failing seam if any. Do not merge dependency ancestry.

## Full diff

```diff
diff --git a/tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py b/tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
index c18fe40b6..033482ec2 100644
--- a/tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
+++ b/tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
@@ -136,10 +136,10 @@ def test_cli_sheet_v2_runtime_preserves_document_and_reads_back(
                         "publication_id": base_head["publication_id"]},
     }
     assert base_document["parent_revision"]["revision_id"] == base_head["revision_id"]
-    # Use the real original publication's closure and the full recorded request
-    # for the provider's physical bindings, effects and immutable successor ids.
+    # The provider reopens the verified closure without the client's base_parent
+    # publication annotation; the full request/head still bind the original pair.
     expected_plan = execute(
-        authenticated_base, [expected_command], commit_request=request,
+        bundle_from_document(base_document), [expected_command], commit_request=request,
         evaluated_head=base_head,
     )
     assert expected_plan.bundle["source_mapping"] == authenticated_base["source_mapping"]
```
