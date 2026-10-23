## Report

- Diagnosed the initial `config.app` order: Runtime authoritative storage and
  receipt/reload use sorted-key canonical JSON, so the old `before, target,
  after` fixture could not read back in that order. This is not normal API
  data loss.
- Applied the permitted setup-only correction in
  `tests/test_timeline_owned_reference_integration.py`: target remains
  `com.example.compiler-canary`; siblings map `before -> a-before` and
  `after -> z-after`, with all corresponding exact map/order and
  `insertion_order` assertions updated. Null/opaque values and all semantic
  remove/retry/receipt/no-duplicate/restart/inverse/redo assertions remain.
- Complete preflight passed: Runtime42a producer bytes/all 15 lock entries,
  all 76 artifacts, schema 65/37 and exact digests, 0.2.17/import/profile,
  shared dependency read-only checks, temp/disk, syntax/diff checks, 1-test
  collection, and complete fixture setup closure.
- Exact preflight collection command: `env
  ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad
  PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad"
  PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q
  -p no:cacheprovider --collect-only -m integration
  tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo`
  → `1 test collected`.
- Earlier unchanged-tree setup failures were ordered `27437` and RT03
  `11493`; corrected fixture-registration run `30759` reached the old order
  assertion and established the canonical-readback witness used here.
- One authorized central ordered run only:
  `rt-m2-private017-initial-order-diagnosis-1015-private017-agent6c-integration-1021101825-7616`
  (snapshot tree `02d77ba52097cba031b16aa2f183236b52472cf0`)
  → `1 failed in 1.51s`, first failure at line 284 because the normal Agent
  recorder enriches the accepted command with capture fields and the test
  compares it to the raw command. No auto-retry and no RT03 run.
- Remove, restart/exact retry, inverse, and redo behavior remains unverified;
  no qualification/adoption claim is made. No product source or immutable42a
  artifact/pin was changed.

See [the detailed diagnosis](design/runtime-private017-initial-order-diagnosis-1015.md)
for the source trace, literal key mapping, preflight identities, and exact
central result.
+

## P1 current R1 real-document corpus (2026-10-23)

- **PASS** — Agent base/current tree `b7a32c5238f0948a913869b06437f174a277172c`; donor `52e9c0ea659123c86d6cbadc94f78ef972d74308`; original packet `d8e1578bd9f717eb975addb50c2654de70815475`; prior independent PASS42.
- Verified all 15 permitted packet blobs against donor: 15/15 exact, 0 mismatches. Imported only the three older/missing packet paths: provider test, request test, and `doc_patch_requests.json`. No product/schema/generated/pin/lock/launcher/outside-test/skip/xfail changes.
- Required pytest: 42 passed, 1 warning, exit 0. Ruff, mypy, and `git diff --check`: passed, exit 0. Logs: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-current-R1-corpus/{pytest,ruff,mypy,diff-check}.log`.
- Evidence uses the production Agent caller `create_runtime_commit_service().commit(...)` via the existing detached service. Exact command/guards/physical roots/created IDs, absence-vs-null, collection `selection_changed`, same-field `value_conflict`, opaque/order/alias/trim/inverse assertions remain covered.
- Detached disjoint-head evidence is legacy `rebased`, not v2 `merged`. Mounted App/HTTP chain and Runtime HTTP publication remain unexecuted; product merge eligibility remains Agent-owned. No full/browser/heavy/socket suite ran.

See `design/handoff-ap2-P1-current-R1-corpus.md` for the detailed handoff.

## P1 corrected encoder corpus review (2026-10-23)

- **PASS — only for the new `p1EncoderCorpus.test.ts` encoder corpus test; not H3 GO.** Reviewed HEAD `d3e141fa5bb544db6eb083d0e08a564f92df67ad`, tree `991c6720b89302e5a375845542ae03a9af4bb666`. The cumulative product diff from App integration `794d365ae03725453c3359d21c791b1ffe7ccee9` is exactly one added file: `src/tools/video-editor/commands/p1EncoderCorpus.test.ts`.
- The corrected split case asserts the complete `list.insert` payload, absent guard, parent physical root, stable created ID, prior order and insertion anchor, all three original `clip-a` before-values and intended updates, exact resulting clip rows, mirrored `config.clips`, preserved registry/name/unknown/output and opaque/params data, and source/after-document immutability. Whole-array `toEqual` rejects omitted or unexpected changes. The existing trim assertions and all 7 current / 8 historical provenance checks are unchanged.
- Exact pinned corpus verification passed for all 8 cases. Actual `documentPatchIntent` imports are only its implementation, `documentPatchIntent.test.ts`, and this corpus test; there is no production encoder caller or mount. This is therefore interim isolated test coverage, not a production-path or H3 claim. The split→trim-new-clip→intervening-Agent-edit→lost-ack→restart chain remains `authored-not-go`.
- Required checks: combined Vitest command **PASS** (2 files, 14 tests); `node node_modules/typescript/bin/tsc --noEmit` **PASS**; targeted ESLint with `--max-warnings 0` **PASS**; `git diff --check` **PASS**. No full/browser/heavy/install run was performed.
- Separately unverified: the full v2 ABI/request and reply boundary—ABI 1 scope/base/commands, label, step metadata/patch/optional reads, `fields|atomic`, reads, dry-run and `Idempotency-Key`; accepted/merged canonical closure/digest/heads/`rebased_onto`, authentic receipt, commands, authoritative steps/dependencies/merge mode; conflict reason/head; invalid code/path/hint/suggestion; and dry-run/history behavior.

See [the corrected encoder handoff](handoff-ap2-P1-encoder-corrected-review.md) for exact command output and limits.

