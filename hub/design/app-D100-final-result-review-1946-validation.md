# D100 validation record

All checks below were read-only. No product, fixture, Runtime, manifest, or source file was edited.

## Source and scope checks

- `git diff --name-status 42040a9c05ae7105cf88459cad5f0b8b9bf56fd1 3082cad490ce1cee764ff137f99cb791a67ddd08` — PASS; exactly one path, `tests/sdk/test_timeline_capture_projection.py`.
- `git diff --check 42040a9c05ae7105cf88459cad5f0b8b9bf56fd1 3082cad490ce1cee764ff137f99cb791a67ddd08` — PASS.
- Byte comparison of the receiving projection file with `f53b016900c99e46998268e36c7c431ac0eec61e` — PASS; SHA-256 `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436`.
- Final product SHA-256 — PASS; `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`, length 64.
- Final D100 test SHA-256 — PASS; `fcd5f187e185faa2222fb23c69827bd6d8bcbb710fdad131f649973f95e6de37`, length 64.
- Git modes and blob IDs for product, D100 test, and projection — PASS; all are regular `100644` files and match the custody record.
- Original 1914 manifest versus corrected derivative — PASS; recursive comparison reports exactly two changed JSON fields: `agent.protected_product.sha256` and `agent.protected_product.required_exact_blob`.
- Current review worktree status — PASS; clean.

## Actual XML checks

Private XML was parsed in place; raw XML was not copied or published.

- Candidate27 XML — PASS; 27 tests, 27 passed, 0 errors, 0 failures, 0 skipped, 2.860 seconds.
- Own9 XML — NO-GO; 9 tests, 9 errors, 0 failures, 0 skipped, 27.585 seconds. Each selector shares the same setup boundary; no projection body passed.

## Source/caller checks

- Agent registered-provider source — PASS; the test registers `load_timeline_commit_provider("astrid")` and calls `service.commit_timeline`.
- Runtime startup and dispatch source — PASS; startup loads the selected provider, registers it before serving, and `RuntimeService.commit_timeline` dispatches through the registered provider execution coordinator.
- Frozen qualified App source — PASS for custody only; durable persistence calls `RuntimeDataProvider.saveTimelineAtHead`/`saveCommitAtHead`, which calls `client.commitTimeline`. The ordinary D66 hook is not relevant to this assertion.
- C0 §§1–5/7 — PASS as read-only contract basis for request/reply, guard, authority, history, and open-field semantics; no contract or product change was attempted.

## Commands deliberately not run by this reviewer

No pytest, collection, socket, provider, body, full, browser, native, TEN, P4, D130, acquisition, retry, or guard-writer action was run. The producer’s exact command was accepted as actual evidence only after independent source, XML, admission, hash, tree, and custody checks. The candidate command used `--timeout=45`; no timeout below the mandated minimum was used.

## Admission chronology

The manager’s read-only cleanup receipt records 5,280,329,728 free bytes at 19:40:44Z. The producer source log records a real floor gate passing immediately before candidate27 launch; candidate27 XML begins at 19:41:31Z. The later own9 command independently logged 5,113,278,464 free bytes, but that later number is explicitly not used to infer candidate27 admission.
