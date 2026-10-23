# G5 c271 final evidence review

**Result: FAIL. G5 remains DRAFT / gated:P1.**

This is a genuine Agent emission defect. The unchanged c271 body reached its
first guarded undo in a fresh process using Agent f27/tree cf7395 and Runtime
2a9e/tree f79. The sole selected test (1/0 deselected) received a real 422
`validation_error`, reason `invalid_records`, as `CommitRejected` with:

```text
inverse stage native writes do not cover its authenticated effect image
```

The refusal was no-write with unchanged head/history; teardown completed.
Redo/overlap assertions were unreached. No pytest terminal stdout/exit is
claimed because the tool did not surface it.

The accepted restructure record has 10 native writes and 10 `commit.effect`
bindings but no `commit.materialization` bindings. Its inverse stage declares
native range `[0,10]` and effect range `[0,9]` while the stage changes physical
shot/internal revision edges. Agent
`astrid/sdk/timeline/_commit_patch.py:638–640` suppresses materialization
bindings whenever an existing occurrence root or `shot_id` is written; this
restructure writes the unchanged `occ-film` root while changing its physical
revision edges. Runtime 2a9e's strict authenticated image comparison at
`runtime_protocol/timeline_commit_auth.py:1368–1375` therefore correctly
refuses the unauthenticated native image. This is not evidence for a Runtime
normalization or harness defect. Sol owner `agt-R2-c271-effect-sol-2013` owns
the Agent hunk; this review does not edit it.

Source/import/body-lock checks passed. No product/test/body rerun was done.
The exact lossless packet is exported as:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-G5-c271-cause-review-2013-packets-a8dcf1d1.tar.gz`

SHA-256 `a8dcf1d1fe6c2ce6905749ea11fe96057b421f7497c0e233c13ca1e0182bc3d4`,
14,794,303 bytes, 85 members. The matching manifest is beside it with SHA-256
`e44a72454b1f641c385dcc0ba0177bd40bc58ae009b2301b69ba6a6fcac361d5`.

Recommended next step: fix and prove Agent materialization emission, then
rerun c271; do not waive Runtime's guard or claim unexecuted assertions pass.

Bounded checks: `git diff --check` PASS; archive `cmp` PASS; exported archive
SHA-256/size/member count PASS (`a8dcf1d1...`, 14,794,303 bytes, 85); exported
manifest SHA-256 PASS (`e44a7245...`, 4,409 bytes); credential-pattern scan
over extracted JSON/JSONL returned 0 matches. The body was not rerun.
