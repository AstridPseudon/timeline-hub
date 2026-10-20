# App refreshed native parent-delete source review

## Verdict

**APPROVE the bounded source slice; HOLD activation and retirement claims.**

Reviewed candidate `8ecefbd8e6a2726971b9e5a62cf457746a7e10a4` (`tl/app-m2-refreshed-parent-delete-source-port`) against corrected root `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c`. The review worktree was current root `7bb885b638838588a0dff81b64b7c34960ac07f3`; the candidate CORS restoration is exactly the two files already present at that current root.

## Findings

No blocking line-level finding in the approved scope.

The exact D1 opaque-eligibility input remains a positive: `app.canonical` is
treated as opaque, while eligibility stays restricted to the known raw parent
closure and exact project/timeline/display binding. Unrelated canonical data,
prototype-shaped values, null/absence distinctions, and collection order are
guarded/preserved rather than inferred or rewritten.

- `src/tools/video-editor/commands/clipDeleteCapture.ts:128-179` accepts only the closed `clip.delete` v1 parent-row command, records whole-row and collection/order guards, preserves opaque fields, compiles the existing mirror, and creates no IDs or media/registry cleanup writes.
- `src/tools/video-editor/commands/commitSession.ts:323-360` keeps capture, finish, and submit inside the existing durable command session/outbox, fences scope/display identity and local generation, validates the original claims against the current closure without refreshing them, and accepts only the matching single-removal preview.
- `src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts:34-50`, `useTimelineCommandsService.ts:850-863`, and `useTimelineOps.ts:286-297` intercept only one unpinned raw parent clip. Group/multi/occurrence and prepared-media paths retain their existing writers; mixed native patches refuse atomically.
- `src/tools/video-editor/hooks/useTimelineCommandSession.ts:170-179` adds the existing legacy-clean barrier and scope cleanup wrapper without changing local projection/recovery/label-intent machinery.
- The exact original grouped-delete assertion at `src/tools/video-editor/hooks/useClipEditing.test.ts:261` remains byte-identical to corrected root (SHA-256 `1beea75106b059db7462b080059253688c47a77db16d55ecfbaf438c62ba9fce`) and remains covered by the candidate run.
- `src/shared/lib/media/mediaCrossOrigin.ts` and its test are byte-identical between candidate and current `7bb885b...`; no other current-root changes were copied.

The candidate diff is exactly 19 allowlisted paths (`+1,339/-9`), with no new whole-parent replacement, renderer/provider, mobile boot, rollback, generic edit engine, or old cohort copy. The source audit reports all other corrected-root paths byte-preserved, including development-only Runtime 0.2.9 artifacts and current label/recovery/projection context.

## Test proof

Candidate-provided final-tree evidence, inspected from the worker notes:

- Core targeted cohort: 6 files, **116 passed**.
- Neighbor/CORS cohort: 12 files, **401 passed**.
- Repository selection: 18 files, **517 passed**.
- Exact opaque-parent counterexample: **3 passed** unchanged.
- Native Agent subset: **2 passed** (exact command/record/after golden, opaque `app.canonical`, guarded inverse).
- Scoped ESLint: passed; known-failure audit: 3 pre-existing authorized markers, 0 forbidden; `git diff --check`: passed; source allowlist and dependency/cache audits: passed.

My review-tree checks:

```text
git diff --check 85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c 8ecefbd8e6a2726971b9e5a62cf457746a7e10a4
  exit 0

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-parent-delete-source-port/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/shared/lib/media/mediaCrossOrigin.test.ts
  1 file, 21 tests passed, exit 0
```

The first CORS invocation without the supplied runner failed during config loading because `__dirname` is unavailable under the runner; the rerun above used the established private runner and passed. No shared dependency, cache, or worktree product file was changed.

## Limits and next steps

This is source-slice approval only. The candidate’s session tests are offline harnesses, not the actual safe Runtime/Agent pair. Real Runtime acceptance, browser/reload, paired guarded undo/retry, and zero legacy traffic remain unrun. No full suite, build, browser, localhost/socket, project TypeScript check, or install was run. Keep group/multi/occurrence replacement, global legacy-writer deletion, and production activation open until those gates are separately qualified.
