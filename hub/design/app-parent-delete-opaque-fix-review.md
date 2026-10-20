# App D1 follow-up: opaque parent-delete eligibility

Verdict: **PASS**

Candidate: `tl/app-m2-parent-delete-opaque-eligibility-fix` at `f1410193f6717ef53ccbeacdb5902028d5863a70`

Base: `a84f1c0c890113bf93f9a5213f9f340a877fa288`

## Review result

The candidate fixes the reported D1 counterexample with the intended minimal product change. `commitSession.ts` no longer interprets authored `app.canonical`; it authorizes a parent delete from the authenticated project/timeline, the exact known display head/binding, one display row with the requested raw ID, and the existing native capture against the known authored closure. Parent ownership is not inferred from a display ID or from opaque canonical metadata.

The candidate adds no helper or alternate path. Compared with the requested base, the product delta is one import removal and deletion of the obsolete `app.canonical` identity check (`1 added / 6 deleted` in `commitSession.ts`); the only other changed file is its focused regression test.

## Evidence

All Vitest runs used the candidate in a private `git archive` snapshot, the private `/tmp/app-coherent-deps12/node_modules` dependency link, `--configLoader=runner --no-cache --maxWorkers=1`. No shared dependency file, symlink, or cache was modified.

- Exact ordinary counterexample, unchanged input/assertions: SHA-256 `abf193bdf89c1ca812c9f53a87395d634f5ada6b4f6023491bd1a56b6f344a34`; **3 passed**, exit 0.

  ```sh
  node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-split029-review/notes/runner.cjs node_modules/vitest/vitest.mjs run --config review.counterexample.config.ts --configLoader=runner --no-cache --maxWorkers=1
  ```

- Focused delete/neighbour cohort (17 files): **493 passed**, exit 0.

- Native raw-row subset using the existing Agent SDK: exact frozen command/record/after bundle plus opaque `app.canonical` row; guarded inverse restored both originals: **2 passed**, exit 0.

  ```sh
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python native_subset.py
  ```

- Invalid projection/display identity, missing/duplicate raw display identity, project/timeline/head scope mismatch, occurrence/shot identity, and suffix/colon target guards: **31 refusal tests passed**, exit 0.

- Group delete `useClipEditing.test.ts:261`: targeted assertion **1 passed** (20 unrelated tests filtered); the file is byte-identical to base (SHA-256 `1beea75106b059db7462b080059253688c47a77db16d55ecfbaf438c62ba9fce`).

- `git diff --check a84f1c0c890113bf93f9a5213f9f340a877fa288 f1410193f6717ef53ccbeacdb5902028d5863a70`: passed.

## Limitations

This was a read-only D1 review. No product files were changed in the assigned worktree; it remains clean. I did not run a full suite, build, browser/e2e, live socket, TypeScript check, install, activation, or real Runtime/Agent qualification. The native inverse evidence covers the initial guarded inverse restoration only, not accepted-history redo. The temporary candidate snapshot and review-only script/config were removed after testing.

Recommended next step: accept this D1 candidate for integration, while retaining the separate real Runtime/Agent and restart/retry qualification as follow-up evidence.
