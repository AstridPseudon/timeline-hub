# Existing accepted projection history audit — M1

Completed 2026-10-19T23:24:02Z, read only, worker `agt-m1-projection-history-audit`.

**No historical overwrite candidate or new proven damage was found in the surviving test corpus inspected. This cannot establish universal absence.** There were 30 accessible SQLite files, containing 29 initialized test realms and one incomplete realm-creation remnant. Fourteen had `timeline_commit_history`; those tables held 18 edges: 12 bootstrap and 6 recorded, with 0 legacy_unknown edges. Three realms contained those six recorded commits, each joined to its `timeline.commit` idempotency result. Across all 30 files there were 97 total idempotency rows and **0 stored shot revisions**. The six recorded canonical documents contained **0 shot images, 0 occurrences and 0 recorded created facts**. Thus none contains an accepted shot first-materialization destination edge to compare with another timeline's prior ownership. Candidate count: **0**. Newly proven mutable-projection damage: **0**. Newly proven pinned-film corruption: **0**.

These surviving recorded commits are the neutral Runtime acceptance fixtures, not a surviving actual-provider occurrence-move history or an owner's film. The reviewed manager probe remains the separate established evidence of mutable projection loss; its temporary realms and the newer shared-identity probe/fixture realms are excluded from this census. No new fixture was created or probe replayed.

Source heads inspected (unchanged at the final head check):

| Source | Exact HEAD |
| --- | --- |
| Assigned Agent worktree and `/home/user/work/agent` | `2b8f2caaadf8b7dd97396803c7f8d289b10a7117` |
| `/home/user/work/runtime` | `80973d34ae10e498d7213c30287012c9876f4b1a` |
| `/home/user/work/app` | `bdc9dcd9b5bacb5ef0466e167b7af06d15c2d362` |
| `/home/user/work/composition` | `7aa384a9f3c815f78ce88ff9b47de5adee7bf34a` |

These identify the code used to interpret storage, not the generating commits of historical fixture databases. The retained databases have no established source-head attribution; none is invented. Read PLAN.md, Agent INBOX's 23:20 same-project-shot-overwrite decision, `managers/agent/notes/shared-identity-probe-reviewed.py`, its measured `shared-identity-probe.log`, and `design/runtime-coordination.md`. No decision was changed.

Discovery was limited to the ORCH artifact tree (excluding delivery source kits), specifically named Timeline task/review temp roots, `/tmp/timeline-*`, the App harness's `/tmp/astrid-direct-*` prefix, and integration `test-results`, `playwright-report`, and `tests/fixtures` directories. Under `/tmp/pytest-of-root`, only Timeline/film test directories or truncated names matching functions from the repos' `tests/*timeline*.py` were selected, including `popen-gw*` workers. The fixture conventions were confirmed in Runtime `tests/timeline_commit_film_fixture.py`, `tests/test_timeline_commit_integration.py`, `tests/test_timeline_commit_acceptance.py`, and App `tests/e2e/local/support/harness.ts`. No arbitrary `tmp*` directories, home/configured personal realms, credentials, or credential files were opened. No surviving realm.sqlite3 was found in the selected ORCH, App harness, named review/temp, or workspace artifact roots; the 30 below were all under pytest temp roots.

The exact 81 selected roots and 30 database paths are retained in `discovery.json` beside the worker report. Discovery visited 1,002 directories, with a 12-level depth cap, no depth truncations, and no symlink-directory traversal. Database inspection used Python stdlib `sqlite3.connect(Path(path).as_uri() + '?mode=ro', uri=True, timeout=2, isolation_level=None)`, `PRAGMA query_only=ON`, then explicit `BEGIN`; all queries for each inspection shared that read transaction, followed by rollback/close. Initial queries were table presence, exact row counts, history intent counts, and count of `command_kind='timeline.commit'`. No product service/store constructor or mutating PRAGMA was used.

The 111-line `audit.py` follow-up bounded values to 2 MB, SQLite execution to about 2 million VM instructions per connection, and recorded-edge reads to 1,000 rows (requesting 1,001 and asserting the bound). Its joined query was:

```sql
SELECT h.publication_id,h.revision_id,h.records_json,c.result_json
FROM timeline_commit_history h JOIN command_idempotency c
ON c.txn_id=h.publication_id
WHERE h.intent='recorded' AND c.command_kind='timeline.commit'
LIMIT 1001;
```

For all six joined rows it checked exact canonical-document digest, parent revision identity and recorded commands against the stored acceptance result. It compared retained parent payloads with their canonical-document images and recomputed the exact content digest: **6 document-digest checks and 6 retained parent-image checks passed**. The shot/internal image arrays were empty. No hash-prefix heuristic was used as ownership authority. With no shot materialization edge present, there was no candidate requiring prior-timeline binding/source proof, an intentional-shared-ownership classification, or a candidate-specific pinned-shot closure examination. This was not a complete event-chain, media/CAS or renderer audit.

The census is per-file consistent, not a machine-wide snapshot. Two zero-history pytest-287 realms were successfully read during the initial census, then removed by ordinary concurrent pytest cleanup before the final file-existence check. Their initial counts are retained below; they contained no recorded commits. Six recorded edges were examined in consistent transactions in the three surviving pytest-119 realms. Sixteen SQLite files lacked a history table, including the incomplete creation remnant. They cannot establish accepted-history absence before that table existed. Removed fixtures, unselected realms and real user histories remain unverified.

Historical records do not provide a direct mutable shot/item before-image. A prior immutable reference could identify an overwrite candidate but would not by itself prove deleted mutable items; a differing current mutable projection can also reflect intentional shared ownership or later legitimate writes. No deletion is inferred here. The existing reviewed probe separately measured before/after loss and intact immutable pins; this audit neither expands nor negates that finding.

Every inspected SQLite file is listed below. `realm` counts initialized realm rows; `history` is the exact history row count or an absent table; `recorded` counts recorded edges. All listed files had 0 shot_revision rows.

| SQLite source path | realm | history | recorded |
| --- | ---: | ---: | ---: |
| /tmp/pytest-of-root/pytest-119/test_atomic_acceptance_exact_r0/realm/realm.sqlite3 | 1 | 3 | 2 |
| /tmp/pytest-of-root/pytest-119/test_changed_payload_and_publi0/realm/realm.sqlite3 | 1 | 3 | 2 |
| /tmp/pytest-of-root/pytest-119/test_failure_after_receipt_rol0/realm/realm.sqlite3 | 1 | 1 | 0 |
| /tmp/pytest-of-root/pytest-119/test_identical_retry_after_res0/realm/realm.sqlite3 | 1 | 3 | 2 |
| /tmp/pytest-of-root/pytest-119/test_invalid_prepared_values_a0/realm/realm.sqlite3 | 1 | 1 | 0 |
| /tmp/pytest-of-root/pytest-119/test_invalid_prepared_values_a1/realm/realm.sqlite3 | 1 | 1 | 0 |
| /tmp/pytest-of-root/pytest-119/test_invalid_prepared_values_a2/realm/realm.sqlite3 | 1 | 1 | 0 |
| /tmp/pytest-of-root/pytest-119/test_invalid_prepared_values_a3/realm/realm.sqlite3 | 1 | 1 | 0 |
| /tmp/pytest-of-root/pytest-119/test_invalid_prepared_values_a4/realm/realm.sqlite3 | 1 | 1 | 0 |
| /tmp/pytest-of-root/pytest-119/test_invalid_prepared_values_a5/realm/realm.sqlite3 | 1 | 1 | 0 |
| /tmp/pytest-of-root/pytest-119/test_invalid_prepared_values_a6/realm/realm.sqlite3 | 1 | 1 | 0 |
| /tmp/pytest-of-root/pytest-119/test_invalid_prepared_values_a7/realm/realm.sqlite3 | 1 | 1 | 0 |
| /tmp/pytest-of-root/pytest-119/test_preview_is_validated_and_0/.realm.create-sulmzkxk/realm.sqlite3 | 0 | absent | 0 |
| /tmp/pytest-of-root/pytest-287/test_canonical_timeline_refere0/realm/realm.sqlite3 | 1 | 0 | 0 |
| /tmp/pytest-of-root/pytest-287/test_timeline_shot_and_referen0/realm/realm.sqlite3 | 1 | 0 | 0 |
| /tmp/pytest-of-root/pytest-41/test_canonical_timeline_refere0/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_generic_filmstrip_outputs0/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_replace_timeline_clip_is_0/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_replace_timeline_clip_rej0/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_replace_timeline_clip_rej1/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_replace_timeline_clip_rej2/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_replace_timeline_clip_rej3/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_replace_timeline_clip_rej4/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_replace_timeline_clip_req0/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_timeline_create_replays_r0/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_timeline_document_command0/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_timeline_document_replay_0/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-41/test_timeline_shot_and_referen0/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-46/popen-gw0/test_canonical_timeline_refere0/realm/realm.sqlite3 | 1 | absent | 0 |
| /tmp/pytest-of-root/pytest-46/popen-gw1/test_generic_filmstrip_outputs0/realm/realm.sqlite3 | 1 | absent | 0 |

Validation command (exit 0):

```sh
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m1-projection-history-audit/notes/audit.py
```

Result: 30 SQLite files / 29 initialized realms / 14 history tables / 18 history rows / 6 recorded rows; all 6 document and 6 retained-parent checks passed, no errors. Discovery and initial census also exited 0. `git status --short` was empty before and after inspection. No repository test suite, full suite, install, network, mutation, SQL seeding, commit or merge was run. Only the assigned shared report/notes artifacts were written; the worktree remains clean.

Recommended next step: retain the M1 hold until Runtime's atomic occupied-destination refusal and the permanent real-provider regression/positive controls pass. Report the historical answer as “no candidate in the bounded surviving test corpus; historical impact elsewhere remains unknown.” No historical repair/migration is justified by this audit alone.
