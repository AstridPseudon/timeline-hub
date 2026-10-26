# U2 G4 G5 F D141ee writers15 source-only return

Result: `SOURCE_SCOPE_CORRECTED_REG_PENDING`; no product/test repair and no behavior PASS.

I read PLAN §3, C0 `commit-v2.md`, MAIN D141ee/D120, the immutable prior author evidence, and all seven review findings. The new packet contains the complete 15-ID scope (4–18), once each, with per-ID protected purposes, exact assertion differences, current source citations, and bounded owner/repair actions. All 15 remain REG-pending. Rows 8, 12, and 13 remain owner-scope pending; rows 10/11 remain distinct narration parameter cases; row 7 splits retained key/one-call/authority from mandatory force refusal.

The source trace establishes:

- `cli_working.py:_cmd_restructure:470-504` calls `_PublishMixin.publish`, but the wrapper’s `_commit_restructure` (`publish.py:345-455`), ordinary `_commit_document` (`publish.py:188-343`), and `_publish_narration` (`publish.py:483-585`) submit through `TimelineSession`/`RemoteTimelines.commit` to `WorkspaceClient.commit_timeline` and Runtime `commitTimeline`. The source therefore shows an old wrapper interface delegating through the approved Runtime-only writer, not a second writer body. F5 still needs an explicit G4/G5 owner decision if the wrapper is removed.
- Agent `WorkspaceClient.publish_parent_composition:429-444` and RemoteTimelines operation dispatch (`remote.py:350-420`) remain exposed, but Runtime’s route is guarded and `service.publish_parent_composition:2943-2944` immediately calls `_require_timeline_command:1665-1672`, which raises `retired_route` and points to commitTimeline. This proves refusal, not Agent-surface retirement and not a second writer. F7 remains owner-pending.
- Runtime `server.py:_timeline_commit:301-341` calls `service.commit_timeline:2469-2483`, whose coordinator/provider path is the canonical mutation route. C0 request/reply rules remain the migration contract: base pair, commands, label/steps, merge/reads, Idempotency-Key, accepted/merged canonical result/receipt/records/bindings/effects/dependencies/history/undo_steps, conflict reason/head, invalid code/path/hint/suggested command, and preview with `would_status`/null receipt/no writes.

Tests and validation:

- No pytest, collection, typecheck, lint, vitest, browser, request/CAS/service, dependency, generated-client, body, profile, or child run was performed, as required.
- Tests were already restored at `445b9c1`, merged HOME `14ccf296f376`, and targeted-failing; this worker did not restore or rerun them.
- JSON validation passed for `per-id.json` and `source-manifest.json`; semantic validation passed for exact 15/unique IDs and all F1–F7 coverage. Typecheck/lint are N/A for source-only work.
- The required fresh `disk-trace.txt` sampler ran every five seconds through worker exit and used the 4,000,000,000-byte stop threshold; the earlier five-second historical trace was not copied or repaired.

Files: `per-id.json`, `source-manifest.json`, `validation.md`, `handoff.md`, `report.md`, and `disk-trace.txt` in the worker evidence directory. No worktree files were changed.
