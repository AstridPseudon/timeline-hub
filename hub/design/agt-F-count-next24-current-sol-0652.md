Updated only the five permitted evidence artifacts: **260 closed / 7 open / 267 total; 118 mappings**.

Preserved all 243 other nodes, 38 prior proofs and coverage records, 94 prior mapping rows, and metadata0636’s complete contract inventory. Ownership is **Agent 6 + Runtime 1**; families are **SDK/timeline 5 + Runtime child/import 1 + rendering/pack 1**. Original versus reviewed fixture differences are explicit.

Validation passed:

- `python3 "$TMPDIR/validate_next24.py"` — preservation, source/AST/assertion fidelity, reviewed membership, counts, links, and all 118 CSV/JSON members.
- `(cd evidence && sha256sum -c agent-D32-current-node-reconciliation-H30-corrected.sha256)` — OK.
- `git diff --check` — PASS.

No behavior/static/full/browser/gate tests ran. Missing raw receipts, root import-snapshot limits, D23, full25691 FAIL, and frozen Farm96 uncertainty remain explicit.

Census SHA-256:
`b7af85439f36b31c1603b162d331d9daea77dd2a2e44148f0ed369462fd59e8c`

Complete five-file package SHA-256:
`2f74ecba4d5218e41fad670fa339059dac13fe448cb22dcfe902e716f6339481`

Package digest uses sorted relative filenames, each encoded as `filename + NUL + raw bytes + NUL`.

Remaining seven exact IDs, all phase `call`:

```text
tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons
tests/sdk/test_timeline_helper_capture.py::test_cut_nudge_restart_merges_other_cut["second"]
tests/sdk/test_timeline_normal_publish.py::test_ordinary_publish_preserves_complete_closure_and_followups
tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head
tests/sdk/test_timeline_persistence.py::test_two_writers_in_separate_processes_merge_different_clips_and_refuse_the_same_param
tests/test_generic_host.py::test_structure_pack_members_survive_harvest_cleanup_and_reopen
tests/timeline/test_authoring_media.py::test_document_publish_forwards_new_stale_head_to_runtime
```

No blockers. Commit message and `DONE` written. Next step: independent review of this candidate; no broad/full-suite PASS is claimed.