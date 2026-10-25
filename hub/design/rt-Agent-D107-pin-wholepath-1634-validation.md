# D107 validation

Verdict: behavior pending. No product or test edit was made in this worker.

## Retained behavior evidence

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D107-current-baseline-1530/evidence/current-equivalents.xml` — two authorized cases, both fail at `test_m1_current_equivalent.py:317` with `exact transcript pin is missing or revoked or ambiguous`; no timeout/setup error.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D107-purpose-review-1550/evidence/validation.json` — protected-purpose PASS, 131 assertions and 5 `pytest.raises` contexts conserved, original M1 unchanged.
- No retained SQLite realm/database or private hydration capture from the D107 run exists in the worker artifacts; persisted record status is **EXACTMISSING**.

## Static checks run

- `sed -n ... PLAN.md`, `MANAGER-COMMON.md`, and `/tmp/.../orch/design/commit-v2.md` — PASS/read.
- `git status --short --branch` — clean worktree aside from the already committed D107 baseline; HEAD `b4b3805da5e8611490401122f986e203f67f21b4`.
- `git diff --check 20177e66564f9f91735ed1a11bac821682d60edf` — PASS.
- Python AST parse/span scan for the four Agent source/fixture files — PASS; spans recorded in `source-map.json`.
- SHA-256 source scan for Agent and Runtime paths — PASS; hashes recorded in `source-map.json`.
- Read-only source callgraph/diff inspection of Agent hydration, manifest construction, Runtime persistence, closure reload, and compiler use — PASS.

## Explicitly not run

- No actual D107 test rerun, unchanged-two rerun, body rerun, full suite, family/P4/tour/native/profile/acquisition test, collector/provider rerun, or browser/live suite.
- No source, test, fixture, pin, schema, generated file, Runtime worktree, Git ref, credential, hub, or design file was modified.

## C0 shape check

The current D107 request builders statically retain the full requested base/command/step envelope (`api_version`, project/timeline, base revision/publication, command schema/op/version/select/args, label, steps, merge, reads, dry_run, source, rationale, group_id). The idempotency key is passed at the Runtime call boundary. No reply shape was widened; the retained XML stops before a successful CLI reply, so accepted/merged/refusal/preview reply behavior remains unverified by this worker.

## Decision

The smallest proved seam is the exact accepted-head record boundary: compare the pre-restart `commit_manifest_json` document pin with its immutable content/binding/link rows and the restarted Agent `pinned_documents` capture. The evidence does not justify assigning Runtime or Agent ownership without that record. Do not infer blame from the compiler guard and do not reconstruct the missing record.
