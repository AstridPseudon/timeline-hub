## Report

Verdict: PASS. No product/test changes; worktree remains clean.

Requested five scenarios:

1. Asset replace/swap forwarders — PASS: `test_cli_assets.py:26-78`.
2. Media add/trim/slip/fade forwarders — PASS: `test_cli_media.py:21-75`.
3. Voice replace/insert/script forwarders — PASS: `test_cli_voice_bindings.py:71-123`.
4. Offline `--file` clip edit and candidate guidance — PASS: `test_cli_edit_flags.py:134-155`.
5. Offline `--file` voice edit and candidate guidance — PASS: `test_cli_edit_flags.py:178-185`.

Evidence was read-only; tests were not rerun per brief.

Save funnel:

- `_cmd_edit` falls back at [cli.py:3185-3223](/home/user/work/wt/agt-F-CLI-save-path-review-0600/astrid/packs/timeline/cli.py:3185).
- `_edit_checkout` opens a detached draft at [cli.py:2757-2764](/home/user/work/wt/agt-F-CLI-save-path-review-0600/astrid/packs/timeline/cli.py:2757).
- `Checkout.save()` writes only the local checkout via temp-file replacement at [checkout.py:156-250](/home/user/work/wt/agt-F-CLI-save-path-review-0600/astrid/sdk/timeline/checkout.py:156).
- The CLI exports a derived-field-free candidate and prints check/commit commands at [cli.py:3247-3258](/home/user/work/wt/agt-F-CLI-save-path-review-0600/astrid/packs/timeline/cli.py:3247) and [publish.py:632-648](/home/user/work/wt/agt-F-CLI-save-path-review-0600/astrid/sdk/timeline/publish.py:632).

Publication:

- Numeric literal move/trim dispatch directly through `TimelineSession` at [cli_native.py:193-224](/home/user/work/wt/agt-F-CLI-save-path-review-0600/astrid/packs/timeline/cli_native.py:193), with receipt evidence `pub1` in `test_cli_commit_move.py:88-108` and `test_cli_commit_trim.py:40-53`.
- Detached candidate commit uses the G3 emitter and `Timeline.commit()` at [cli_native.py:109-135](/home/user/work/wt/agt-F-CLI-save-path-review-0600/astrid/packs/timeline/cli_native.py:109).
- The printed document-script path also emits `doc.patch` and calls `TimelineSession.commit_many()` at `timeline_document.py:281-333`; both reach Runtime through [sync.py:529-551](/home/user/work/wt/agt-F-CLI-save-path-review-0600/astrid/sdk/timeline/sync.py:529).
- `RemoteTimelines.save()` is retired and returns 410 without writing at [remote.py:464-477](/home/user/work/wt/agt-F-CLI-save-path-review-0600/astrid/sdk/remote.py:464).

The retained native-sheet outbox is the only fallback-adjacent save edge that can publish during `Checkout.save()`; it still uses the normal Runtime session, not the retired route.

Smallest missing producer: none. Local staging is intentional; final film publication is Runtime-only. No C0 wire/schema claim made.

Read-only checks: source hash checks completed; HEAD `bb50a43c91`; no pytest, Node, HTTP, browser, or full-suite runs.