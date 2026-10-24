Updated only the five evidence artifacts. **Candidate: 261 closed / 6 open / 267**.

- Reopened restart on current **2FAIL/1.92s** evidence. Older38af proof remains historical/challenged; changed `journal.py`/`begin_nudge` and unavailable raw receipts are explicit.
- Added stale-head **1PASS/0.85s**, bounded mocked unit, and complete-closure **1PASS/6.34s**, source-mode with all22 predicates retained. Both have independent0645 PASS; seven prior publication passes were not recounted.
- **120 mappings:119 current closures +1 historical challenged**. Preserved264 unrelated nodes, prior24 closures,45 prior proofs/coverage records and full contract inventory. Now48 proof records;45 distinct proof references support closed nodes.
- Active owners: **Agent6**; families: **SDK4 + child/import1 + rendering/pack1**.

Validation passed:

- `python3 "$TMPDIR/validate_current_challenge.py"` — IDs/phases, exact delta, preservation, CSV/JSON membership, source/AST/assertions, links and sums.
- `(cd evidence && sha256sum -c agent-D32-current-node-reconciliation-H30-corrected.sha256)` — OK.
- `git diff --check` — PASS.

No behavior/static/product/full/browser/gate tests ran. Raw JUnit files remain unavailable locally; full25691 FAIL, Farm96 uncertainty, D23 and snapshot-gap limits remain explicit.

Remaining six exact IDs, all phase `call`:

```text
tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons
tests/sdk/test_timeline_helper_capture.py::test_cut_nudge_restart_merges_other_cut["second"]
tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head
tests/sdk/test_timeline_persistence.py::test_restart_a_fresh_process_sees_every_edit_and_the_undo_history
tests/sdk/test_timeline_persistence.py::test_two_writers_in_separate_processes_merge_different_clips_and_refuse_the_same_param
tests/test_generic_host.py::test_structure_pack_members_survive_harvest_cleanup_and_reopen
```

Census SHA-256:
`22ee4d6df217eef1cef60f7e9c646b6f5fe13a45d31163afb2ffe46126facae0`

Five-file package SHA-256:
`9e52f5a93bc5ff9a0ada21ed917737e2e91ab38eb32643f5583c0a8dad1e9cdf`

Package encoding: sorted relative filename + NUL + bytes + NUL.

No blockers. Commit message and `DONE` written. Next: independent package review; Runtime’s faithful persistence-fixture migration remains unqualified.