# App M2 recorder test-policy handoff — 2026-10-20

The fourth expected-failure marker introduced by `c5a3600f8` was physically in
`src/tools/video-editor/commands/clipMoveCapture.test.ts`, not
`clipMovePrimitives.test.ts`. Its old assertion expected the helper to overwrite
a divergent `parent.config.clips` mirror. That is a stale bug expectation: the
native e8 recorder synchronizes only an initially equal mirror, while the real
main API refuses the divergent opaque-only publication with
`409 canonical_payload_mismatch`.

The test now keeps the original adversarial `[{ id: 'legacy', at: 88 }]` input
and asserts the approved native outcome: the divergent config mirror is
preserved, `record.derived_writes` is empty, and the moved clip's opaque payload
and existing `astrid.cut` value remain unchanged. This is a normal M2
requirement update, not a lost supported behavior. The three audited drag
`it.fails` markers remain unchanged.

Evidence on the worker tree:

- Six core capture suites: 252 passed, 6 files passed.
- `node scripts/quality/check-known-failures.mjs`: 3 authorized, 0 forbidden.
- Targeted ESLint: passed.
- `git diff --check`: passed.
- No broad typecheck/full/browser/network suite was run; this is a test-only
  delta and the documented App typecheck baseline remains two errors.
