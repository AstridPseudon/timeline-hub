# P1 chain Sol-source independent review — 2026-10-23

Result: **FAIL — source readiness; not H3 GO/body PASS**.

Reviewed App `tl/ap2-P1-chain-sol-0327` at `4fa831be1` against PLAN §3 P1,
C0c §§1–5/7, D12 legacy-validation, the original P1 corpus/fixtures, the
`0303` first-return brief, and `0309`. Only
`tests/e2e/local/three-products.p1-chain.spec.ts` differs from App `4394b74a1`;
no product/generated/lock/fixture/launcher/harness/suite edits, skips, xfails,
or weakened assertions are present.

Review0309's two missing assertion groups are correctly fixed. Refusal now
requires the normalized C0c physical atomic conflict
`{kind: 'atomic_scope_changed', ref: 'parent', path: []}` and structured root
path `[]`. Merged canonical closure checks the actual right clip's foreign
`app['org.example']` object, explicit `clear: null`, and absent `app.astrid`,
while preserving the prior opaque/order/created-ID/mirror/receipt/history/
request-retry/refusal/message/legacy-route assertions and both interleaving
boundaries.

Concrete blockers remain in newest joined App `f7764de59`:

1. The spec seed has numeric `hold: 8`, but App's `isHoldClip` treats every
   numeric hold as a hold clip and its split branch copies `from`/`to` and
   `app.astrid.for` into the right clip. The retained spec requires source
   windows to split and right `app.astrid` to be absent.
2. The unchanged `getByLabel('Source In')` locator is not supported by the
   current UI: `FieldLabel` is a `div`, and the adjacent `NumberInput` has no
   label association/`aria-labelledby` at that call site.
3. The production local save handoff omits reads/merge; the session therefore
   sends the doc.patch with C0c's conservative `merge: 'atomic'`. Since the
   intervening Agent label changes the parent scope, the retained merged-trim
   expectation cannot land through this caller.

The bounded parent-only direct genesis seam is accepted for source review;
no workaround or unrelated gate was added. The chain exercises accepted,
merged and refused only; invalid/preview variants remain unexecuted.

Checks:

- Playwright list command — PASS, exactly 2 tests.
- `npx tsc --noEmit` — PASS.
- scoped ESLint with `--max-warnings 0` — PASS.
- `git diff --check` — PASS.

No browser/socket/body/full/heavy run was performed.
