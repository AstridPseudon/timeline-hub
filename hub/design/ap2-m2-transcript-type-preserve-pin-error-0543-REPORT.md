# ap2-m2-transcript-type-preserve-pin-error-0543

## Result

Changed only `src/tools/video-editor/commands/transcriptAssociateCapture.ts`.
`exactPin` now binds with the existing `object(value)` predicate and explicitly
fails with the unchanged message and `invalid_source` for non-object values.
The genuine typing narrowings and all other command/record/type-shape code are
unchanged. No API, schema, pin, caller, activation, or shared-composition
qualification was added.

## Hashes and diff

- Base commit: `ab60b24c80b94042569be33806c21a1eb439e8e3`.
- Current HEAD before harness commit: `ab60b24c80b94042569be33806c21a1eb439e8e3`.
- Final edited-file SHA-256: `a4db541841f2c068c2984c27225c6fd14a5b557a648b6d9412b5ed5e352020a2`.
- Working diff SHA-256: `d47b0eb9815156b404c9d8c83f191b817c658202d223b2f1b9323fd611696a19`.
- Diff: exactly 1 insertion / 1 deletion in `transcriptAssociateCapture.ts`.
- Live callers outside the target and its test: `0`.

## Tests and probes

- `npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts` — **PASS**, 1 file, 7 tests.
- `npx eslint src/tools/video-editor/commands/transcriptAssociateCapture.ts --ext ts --max-warnings 0` — **PASS**.
- Direct existing capture seam probe through `captureTranscriptAssociation` — **PASS**: non-object, array, and null pins each refused with message `exact transcript new DocumentPin is required` and kind `invalid_source`.
- Ordinary success/golden output remains covered by the 7 passing transcript tests.
- Prior evidence retained without replay, as requested: 157 focused tests passed, strict-island typecheck passed, and the prior typing diagnostic delta was 52→0. Broad suites were not run.

## Merge-forward and limitations

Immediately before finalization, attempted:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/merge-forward ap2-m2-transcript-type-preserve-pin-error-0543 hub/tl/integration`

Both canonical refs `hub/tl/integration` and
`hub/timeline/app/tl/integration` were `1a54d30521945c7ea1ab7148e840011c8893c78d`.
The attempt was blocked before applying a merge because the sandbox refused the
linked worktree Git ref write for `.git/worktrees/.../ORIG_HEAD.lock`.
No merge, commit, rebase, checkout, or shared graph edit was performed.

No browser, full suite, install, or live-socket qualification was run.
