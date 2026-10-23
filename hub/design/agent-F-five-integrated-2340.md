## Result: PASS

Qualified exact Agent head `19646f04d815900853a8892dd24f1ddefffe9c21`, tree `f5a756298d51327413decdc2cf22afc19283c010`, with Runtime `8ea0766f…`, tree `6047ac…`. Worktree clean; no source/test changes made.

Behavior lanes:

- Video normal: `190 passed, 1 deselected`
- CLI: `92 passed`
- Inverse fixture: `47 passed`
- Scene integration: `27 passed`
- Scene contract: `4 passed`
- Root redo: `17 passed`
- Managed video service `agt-F-five-integrated-2340-agt-G4-video-sol-2250-managed-video-1023234329-5692`: `1 passed`

Total: `378 passed, 1 deselected`.

Static/vendor checks:

- Ruff baseline: `2148/2148`
- Mypy baseline: `1911/1911`
- Scoped mypy retained 2 inherited diagnostics; no new diagnostics in changed hunks.
- Vendor lock, artifact manifest, and `git diff --check`: passed.
- Frozen `34eac`, `d106`, and `819acf` custody hashes matched.

Provenance audit passed: 14 changed paths exactly match the five reviewed source commits; HEAD-minus-`c36` equals their union; merge parents are serial normal merges; `d7db17a60` and `4387ff0cb` are not ancestors.

The prior full suite remains terminal-failed (`262 + 5` failures, `17159` passed); it was not rerun or relabeled. Qualification applies only to exact head `19646f04…`; any later head move requires requalification.

Markers and commit message were written as required.