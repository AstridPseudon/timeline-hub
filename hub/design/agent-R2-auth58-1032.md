# R2 original58 authentication qualification — blocked on exact source recovery

## Disposition

**STOPPED before execution.** The requested one meaningful run was not made.
The original untracked 58-case authentication probe is not recoverable from the
retained artifacts with its exact source and complete case inventory. The brief
requires stopping rather than inventing a replacement matrix or claiming a
58-case result.

No product, test, generated, pin, environment, service, shared-dependency, or
contract files were changed. No checkout, Git write, daemon, or full/HTTP/
native14/browser/other-matrix run was performed.

## Settled evidence read

Read:

- `PLAN.md` (v2.1; single source of truth).
- `design/agent-R2-split-inverse-0826.md`.
- `design/agent-R2-split-review-0836.md` (the requested independent0836
  evidence artifact).
- `design/agent-R2-split-integrated-0851.md` (the requested integrated0851
  evidence artifact).
- `design/peer-runtime-to-agent-20261023T1027-inverse-stage-integrated-READY.md`.
- `managers/agent/briefs/R2-auth58-1032.md`.
- Durable worker logs for `agt-R2-split-inverse-0826`,
  `agt-R2-split-review-0836`, `agt-R2-split-integrated-0851`, and
  `agt-R2-stage-repro-0912`.

The retained prior matrix summary is exact for these facts:

- total candidates: **58**;
- prior result: **53 pass, 5 fail**;
- failed candidate indices: **4, 16, 28, 40, 49**;
- failure labels:
  - `4 two-step/['clips']/False/whole`;
  - `16 two-step/['clips']/True/whole`;
  - `28 two-step/['config', 'clips']/False/whole`;
  - `40 two-step/['config', 'clips']/True/whole`;
  - `49 native/whole`;
- failure: `invalid_records` / `provider binding differs from its
  authenticated input image`.

The report also preserves the broad class summary (single-step split aliases,
selected split/note/move paths, merged split, and whole multi-step failures),
but it does **not** preserve the complete 58-case construction, each case's
request/guard assertions, or the source hash of the untracked probe.

The retained `design/agent-R2-stage-repro-0912.py` is explicitly a single
split+unrelated-note repro and embeds `no_original_58_rerun: True`; it is not
the requested matrix and was not used as a substitute. The earlier durable
`auth_probe.py` source recovered in the 0826 log is only the 8-candidate
single-step probe (2 aliases × 2 output orders × insert present/absent), also
not the 58-case matrix.

## Exact source identity checked

Agent worktree `/home/user/work/wt/agt-R2-auth58-1032`:

- branch: `tl/agt-R2-auth58-1032`;
- HEAD: `ef851b22c506245441b9a630c093b3460e39cbdc`;
- status: clean at inspection;
- `astrid/sdk/timeline/commit.py` SHA-256:
  `7776e31c83a7f0fc58965141b5863548c7cd4bb60f58f5c827848254c810eb3b`;
- `astrid/sdk/timeline/inverse.py` SHA-256:
  `267b1b1589c0254345a13bf802df8b40301f70020389c223c91f4b14808f336d`;
- `tests/editing_conformance/test_inverse_clip_mirrors.py` SHA-256:
  `7cec273a0fe7bd73be794e11bc54bbd1f222455112bb9b3d87e9e08b4f474b81`;
- helper hashes retained for the focused fixture:
  - `test_doc_patch_mirrors.py`:
    `f15be6a4f16276a630460e33e47a96ec881cc2b88fa80df86dccd773d08fd4a0`;
  - `test_doc_patch_v2.py`:
    `32e2fd46443106221e424fda9aa432efab6bccd55773a59664d86a400ba15629`;
  - `test_timeline_commit_provider.py`:
    `06228341db69c9604af57a786d4b8fc462ba881e59c195281c7151f2ce2e0ef4`;
  - `test_provider_step_undo_v2.py`:
    `c5daf0318cba184fd5787103fff77a704ad37c08d731533c5346993b704c74eb`.

Runtime pin `/home/user/work/wt/rt-pin-49ce5328`:

- detached HEAD: `49ce53289bc37d9387a7d9e6b9c9b16072162181`;
- tree: `364380ae064c512c0a0d2b8903a599b7026642f4`;
- clean at inspection;
- `runtime_protocol/timeline_commit_auth.py` SHA-256:
  `65fd735edfa0e9f4a77aaf4f473095f1539ea1ce453439177e9fe7f39b4466f1`;
- `runtime_protocol/timeline_commit_store.py` SHA-256:
  `243d312fe404f5ed80f0ef1aa9d7405b93ff77949eef5157827a7779c6323b9f`.

The normal `/home/user/work/runtime` checkout was also at the same clean
`49ce532...` / `364380...` pair during inspection. No shared checkout was
modified.

## Why no faithful harness adaptation was attempted

The brief permits adapting the original harness only when it has the same
history defect, using actual `store.history_entry` /
`_inverse_stage_history` authenticated provenance exactly as reviewed. That
adaptation cannot be applied without the original 58 requests, assertions, and
case ordering. The durable 0912 source is a different one-case witness and
explicitly says not to rerun original58. Constructing a new 58-case loop from
`test_inverse_clip_mirrors.py` would change the requested case identity and
guards, even if it reproduced the five known failure labels.

## Commands and results

Read-only identity checks completed:

```text
git rev-parse HEAD
  ef851b22c506245441b9a630c093b3460e39cbdc
git status --short --branch
  ## tl/agt-R2-auth58-1032   (clean)
git -C /home/user/work/wt/rt-pin-49ce5328 rev-parse HEAD
  49ce53289bc37d9387a7d9e6b9c9b16072162181
git -C /home/user/work/wt/rt-pin-49ce5328 rev-parse HEAD^{tree}
  364380ae064c512c0a0d2b8903a599b7026642f4
```

No pytest, central targeted service, network/live-store process, or authmatrix
command was run. Therefore there are no current per-case PASS/FAIL results,
no loaded-module origins before/after each case, and no qualification claim.

## Required next step

Recover and publish the original 58-case probe source plus exact case inventory
and hash from retained external storage/logs. Then run it once against Agent
`ef851b22...` with Runtime `49ce532...` through the normal pin route, recording
the actual Agent/Runtime module origins before and after every case and retaining
the original positive/negative guards and full request envelope. Do not reuse
the 0912 one-case script, borrow D17-normalizer work, or broaden into another
matrix.
