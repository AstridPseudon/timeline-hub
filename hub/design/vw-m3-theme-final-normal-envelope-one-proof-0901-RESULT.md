# One normal Theme proof — result

## Source

- Worktree: `/home/user/work/wt/vw-m3-theme-final-normal-envelope-one-proof-0901`
- Base: `tl/vw-m3-theme-envelope-corrected-space-cleared-0839`
- Base SHA: `d6176de7d38cda56591ffe313ed40c2326374935`
- Changed file SHA-256: `a1427d2a51cd52d8c73d3c9ec8911036358ba506adbe6b13343e7881d5ae65cb`
- Host source SHA-256: `c3adb033a7dab470d2bedb3fba66ac3a843b89888fed08a252c3bdd971eb0b29`

## Central proof

Exactly one request was submitted:

- Suite: `integration-viewing-theme-normal-props-0234`
- Result ID: `vw-m3-theme-final-normal-envelope-one-proof-0901-integration-viewing-theme-normal-props-0234-1021090154-3697`
- Result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-theme-final-normal-envelope-one-proof-0901-integration-viewing-theme-normal-props-0234-1021090154-3697`
- Snapshot tree: `79e2935a44e528a79c9d6a7ab69c385b6204d466`
- Exit: `1` (one failed test, 100.98 s)
- Summary SHA-256: `df00cc3e42e8d0d20d233f934cb036d8d363f240cd5cec997910d0a7ef2683aa`
- Log SHA-256: `0a64f6b3be9622c69e1f4634039f7921ced35305da3beb99a19e3af291512795`

The corrected normal call passed Runtime admission and managed input
materialization. The test reached and passed the managed `theme.json`
materialization assertions, including the attempt-local managed-object path
and explicit Theme contents. It then stopped at root preparation before
props/default/forged-source assertions:

`FileNotFoundError: runtime validation consumer context differs: this process's environment was not validated at launch (only the host and Remotion-capable capability workers are)`

This post-materialization validation-context failure is distinct from prior
result `20144`, which failed earlier with `KeyError: 'theme'` because of the
fixture's extra envelope layer. No retry, alternate suite, browser, MP4,
parity run, or further source edit was made.

## Other evidence

- `ruff check tests/integrations/test_generic_host_remotion_render.py`: passed.
- `git diff --check`: passed.
- AST control for corrected normal call, explicit authorization, retained
  admitted descriptor binding, and forged-source path: passed.
- Frozen Runtime: `/home/user/work/wt/rt-pin-8f105c26`,
  `8f105c26e3b62f9c2683f717a9773a12bc775a8e`.
- Frozen Runtime `service.py` SHA-256:
  `ee6c75b0f39e2bb456f296f069a42e28b4b9c2f5c9c75251c6054a6f9bb451c3`.
- Free space at final allocation check under lock: `11618856960` bytes;
  threshold: `11253940118` bytes.

## Cleanup and lock note

Under the shared browser lock, only this exact private copied graph was
removed:

`/tmp/pytest-of-root/pytest-120/test_generic_host_normal_impor0/workspace/remotion/node_modules`

The result log, realm, admission state, materialized Theme file, and
composition manifest remain. The initial request shell mishandled the returned
trailing slash and released the lock before waiting; it submitted no second
request. The same single request was then awaited under the lock to completion.
