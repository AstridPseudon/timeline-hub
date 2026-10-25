# D132a/G3/R2 source-assessment commands and results

- Read `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`, repository `AGENTS.md`, and the Astrid core skill — PASS. The settled plan and C0 rules were treated as authoritative.
- `git status --short --branch` in the assigned Agent worktree — PASS; clean branch `tl/app-D132a-child-boundary-applicability-1744`.
- Read-only source inspection of the graph fixture/test, Agent recorder/command/preview paths, Runtime service/port/store/auth paths, C0 contract, and the two named immutable Runtime pins — PASS.
- `git rev-parse HEAD HEAD^{tree}` — PASS; Agent commit `224de4697c36b8958d94c0b85626e0fedaf007cb`, tree `3db8babbbdaf9a011d2eab9e27884c6c195cd76c`.
- `git -C /home/user/work/wt/rt-pin-5e9ad1c6 rev-parse HEAD HEAD^{tree}` and the same for `rt-pin-ab1e4f61` — PASS; identities recorded in `evidence/source-custody.json`.
- `git -C /home/user/work/wt/rt-pin-ab1e4f61 diff --no-index --unified=8 /home/user/work/wt/rt-pin-5e9ad1c6/runtime_protocol/timeline_commit_auth.py /home/user/work/wt/rt-pin-ab1e4f61/runtime_protocol/timeline_commit_auth.py` — PASS; only the cited inverse/materialization/validation-order hunks differ; `native_site` is unchanged.
- `python3.11` AST parse plus `compile(source, filename, 'exec')` on 11 cited Python files — PASS; no bytecode or source writes.
- `python3` JSON parse of the Agent edit-command schema and qualified Runtime timeline-commit schema — PASS; 2 files.
- `git diff --check` — PASS.
- Clean-tree/no-change assertion and expected-base assertion — PASS; no repository edits.
- No pytest, own9 rerun, full/family/native/service/browser/socket suite, source change, recovery/SWAP inspection, collector, or test rewrite was run.

## Trace result

The first failed boundary is initial child birth during Runtime validation of the prepared record. The registered provider successfully executes the create handler and records the child captures. Runtime `validate_step` then resolves the captured occurrence aliases against the pre-command closure. The frozen `native_site`/`site` path reaches the occurrence-row lookup and refuses because the newly created occurrence is absent from that input boundary. The failure precedes materialization, inverse, reload, and redo.

`qualifiednormalab1e` does not alter that path. Its changes are explicitly inverse-only or authenticated materialization/turnover handling, and its `native_site` implementation is unchanged. Verdict: `NOT_APPLICABLE` to this exact first seam; existing owner is Runtime authenticated closure validation, with any correction limited to a narrowly authenticated same-command created-root alias boundary.
