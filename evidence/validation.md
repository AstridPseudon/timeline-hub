# D141y custody-correction validation

## Historical result preserved

- Original tuple SHA: `6fe1b04ca64f38cc8a524bc397950df5a6bce835be614341a70e2c163d253c4d`.
- Original raw stderr SHA: `8723a85802bb604561bf76ba507e71dc13fc4d4c4ae9bda553b32fee0fb90c95`.
- Original exit: `2`; original App ancestry refusal: base `fc24f84994dc36cfae9349112782ab4d91dbc73b`, tip `4de54db14bdc9ddc2ce2e5887258b03acbffd30d`.
- Original `command.json` invocation count: `1`.
- Agent, Runtime, App, and Composition patch/tree/bundle/apply checks: `NOT_REACHED`.
- Original author and independent review files remain at their original absolute paths; SHA-256 values are recorded in `source-manifest.json`.

## Custody correction

The independent review’s F1 is **substantiated from old evidence**. The author transcript contains the sampler start command at line 853, but no assigned original sampler PID or lifecycle receipt. Line 3880 is only a `ps` query for PID 3265 and has no returned process state. The author’s `finalize.log` records wrapper finalization and cleanup, not sampler kill/wait/reap. Therefore historical terminal, termination, and reap are **UNKNOWN/UNSUBSTANTIATED**. Only that unsupported historical claim is retracted.

The current sampler records are present-time observations. They show PID 8, start `2026-10-26T07:25:10.193Z`, terminal `2026-10-26T07:25:16.203Z`, `kill_return=0`, `wait_return=143`, and reap `2026-10-26T07:25:20.217Z`; both samples stayed above the `4000000000` stop. They are explicitly not substituted for the original sampler.

## Read-only checks

Current read-only `git rev-parse`/status comparison found all four source heads and trees equal to the original tuple and clean. No source proof was retargeted. JSON validation covers the five JSON artifacts in this derivative; no product tests, typecheck, lint, browser, service, full suite, or targeted suite was run.

C0 sections 1, 4, and 7 were read from `contract/commit-v2.md` (SHA `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`). The request remains `api_version/project_id/timeline_id/base_revision_id/base_publication_id/commands/label/steps(id,label,intent,tags,command_ordinals,patch,reads)/merge fields|atomic/declared reads/idempotency/dry_run/source/rationale/group_id`; replies remain accepted/merged canonical closure with authenticated receipt/records/bindings/effects/dependencies/history/guarded undo, conflict reason/head, invalid code/path/hint/suggested command, and unchanged preview semantics. No contract or source file was changed.
