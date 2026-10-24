FAIL — independent read-only review.

Corrections:

- P1 attribution was wrong. The mounted App UI performs split (`.clip-action` → ruler → `s`) and trim (`Timing` → `Source In` → Enter). App transport is `useTimelineSave` → persisted outbox → `RuntimeDataProvider.commitTimeline` → generated `client.commitTimeline` → Runtime `/v1/.../commit`; it is not `client.timelines.commit`. Agent only supplies the intervening label/move via `astrid.commitCaptured`.
- P1 assertions are stronger than the report stated: accepted App split with `doc.patch` list insertion/created ID, exact clip/closure/opaque preservation; merged trim with `rebased_onto`, Agent label preservation, history/readback; lost-ACK exact body/key after reload and Runtime restart; one history entry and no legacy writes. The refusal case asserts Agent move canonical state, HTTP 409 `value_conflict`, structured conflicts, rollback dialog, rejected outbox, exact Agent canonical closure, and no legacy writes.
- P5 restore is genuinely covered positive behavior in `test_timeline_commit_crash.py`: `/v1/projects/{project}/timelines/{timeline}/composition-revisions/{revision}/restore`, parameterized pre/before/after crash, replay, and changed-payload rejection. It is Runtime crash/idempotency coverage, not replacement success authority for App authoring.
- P4 must distinguish SDK-only evidence from Runtime HTTP evidence. `tests/sdk/test_p4_*` use fake/detached or monkeypatched generated boundaries. The real service nodes are the three `tests/editing_conformance/test_p4_*_runtime.py` files: CLI/sheet plus show/history, ten notes in one commit with per-step undo/redo after restart, and conflict rerun with exact `[200, 409, 200]`.
- Certified P5 evidence remains exactly the prior 14-node integration proof plus 24 crash nodes: the 14-pass pair was Runtime `62c454ac/tree b84e048` with Agent `f894c3c9/tree d24f25a`; the 24-pass current-provider crash run used that Agent. This is historical evidence, not final-tuple proof.

Source identities inspected:

- Review App: `66354161950d1e747965c095ea97b881d2592708`, tree `9a37265f0286128df7e6240a9df9877d959474af`.
- Integration Agent: `1f15f274824fadca722feb8676e6746dbd237f64`, tree `1ac5f2d6de4083d3959bf59e8fc8167d5ae3400e`.
- Integration Runtime: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`, tree `f56c396c4495547680b46e832565278d2c375e69`.
- Current C0 contract: `contract/commit-v2.md`, blob `257024df…`, SHA-256 `4581ea85…`.
- Frozen R4 refs were inspected separately and are not final producer/install identities.

Current source hashes in the prior map were confirmed. Existing suite locks are historical and stale for P1, P3, and P2 popup:

- `app full-e2e-three-products`
- `app ap2-P3-gate5-h6-0348`
- `app ap2-P1-chain-h6`

The rows retain old Agent/Runtime tuple locks (`079580ca…`, `2a9e347…`), old App/tree locks, P1 old body/tail locks, P2 old popup lock, and P3 Gate-5 body lock. The submitted App runs `23809` and `9310` remain unchanged and were not classified or rerun.

C0 request/reply summary: request includes `api_version`, project/timeline IDs, base revision/publication IDs, commands with `schema_version/op/version/select/args/created`, label, steps with `id/label/intent/tags/command_ordinals/patch/reads`, `merge` (`fields|atomic`), request `reads`, `Idempotency-Key`, `dry_run`, `source`, `rationale`, and `group_id`. Replies include `{data, receipt}`, `accepted|merged` plus historical `rebased`, canonical document/digest, id map, base/previous/accepted heads, merge mode, provider/compiler/publisher, records/effects/dependencies/steps/history/undo steps, preview/required/would-status, conflict reason/head, and invalid code/path/hint/suggested command. Runtime remains the sole writer; Agent is the semantic producer/provider; App is the mounted outbox caller.

No supported App-service entry currently runs the Python P4/P5 nodes. Smallest next owner input: App service owner must provide an entry for the exact D48-adopted Agent/Runtime tuple using the existing `agent p4-v2-http-nodes`, `runtime commit-integration`, and `runtime first-capture-integration` command shapes. No new framework, backend, authority, or substitute route is justified.

Verification:

- `git diff --check` — PASS.
- Worktree status — clean.
- No gate, browser, service, HTTP, source-test cohort, full suite, or `request-test` run, as required.
