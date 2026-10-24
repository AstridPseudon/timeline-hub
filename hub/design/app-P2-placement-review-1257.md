## Review report

Verdict: PASS for the placement-owned delta; full branch qualification remains pending shared helper composition.

- HEAD: `d5e9deba6104a852fc514fbcf16a668edc0a8670`
- Parent: `73aa558266e04cae80ea23c50a4bd4722abcda6b`
- Tree: `9203740c165f7520e948101fb3af14235cc86cbf`
- Delta: 2 files, `42 insertions / 3 deletions`
- Worktree: clean

Hashes:

- Full file before: `5f82ec9064abf15e1beada27e3c7905556cbcf66a63bc0a843f685729cb9ae71`
- Full file after: `b2a999b5a0cca7eb31e9cac4af6ca78194306624fbd7537482256f37f286f816`
- Placement case before/after: `d409f4ad…` → `2fa3cca2…`
- Protected element case: unchanged, `38653860…`
- Protected register case: unchanged, `7e8d5928…`
- New control: `2172aa3e…`

Evidence:

- Placement helper control: 1 passed.
- Exact reviewed `778ea…` shared-helper composition in bounded TMPDIR control: 1 passed, covering wrong receipt, key, base, history/head, and inverse target.
- Vitest targeted suite: 3 files, 118 passed.
- TypeScript check: passed.
- Scoped ESLint: passed.
- Playwright list-only with `reporter=list`: exactly 3 authored cases listed.
- Parent-split/parent-trim configs: zero applicable authored cases.
- `git diff --check`, reverse check, and reverse-apply check: passed.

Runtime contract comparison used current Runtime `becfe6db88b2cc034dba3fafa6c050117dc2b06`:

- C0 defines `receipt.receipt_id` as the authoritative publication ID and keeps `idempotency_key` distinct.
- `timeline.inverse` targets publication IDs.
- Current store emits receipt IDs from transaction IDs.

Known pending composition: the isolated branch still has the old shared `assertAcceptedReply`/history helpers. A bounded check reproduced their expected rejection of a distinct Runtime receipt. The reviewed replacement is in `778ea320c53734c9df9733174899dd6aad5cefdf`; no whole-branch PASS is claimed until composed.

No browser, backend, full-suite, or live-credit run was performed. Required commit message and `DONE` marker were written.