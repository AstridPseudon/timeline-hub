# Handoff: App P1 refusal schedule/oracle

Proposal only; no product/spec/helper/ops changes were made.

The current second P1 case must hold the actual normal App trim POST after `observe` has captured its authentic body/key, then accept a real Agent move from the split pin, then release the same route request unchanged to Runtime. Reuse `observe`, `page.route`, `forward`, the real outbox, and real UI. Do not fabricate a request, force the Agent head, remove reads, use an alternate executor/provider, or manually commit.

The actual local-save request is full v2 with `merge: 'fields'` and declared reads. Assert its real `at` and `from` reads and the accepted split base pair. The old `atomic_scope_changed`/`parent`/`[]` assertion is stale because it describes omitted reads. The exact current Agent/C0 refusal is:

```ts
reason: 'value_conflict'
ref: 'parent'
path: ['config', 'clips', `id:${rightId}`, 'app', 'astrid']
```

Why: the actual trim clears `app.astrid`; native Agent move writes `app.astrid.fixed_start/for`. Agent canonicalizes both to the parent config clip path and scans the authored patch guard before the later declared `at`/`from` field guards. Keep `at`/`from` reads in the wire assertion, but do not claim `at` is the returned first conflict without changing source behavior. Retain the existing generic tagged `base/theirs/ours` shape checks rather than guessing state values.

Keep every current second-case assertion after the 409: recovery/refusal message, rejected outbox, history `before + 2`, Agent head, canonical parent/payload/dependency manifest, no child revisions, clip order, `config.clips`, opaque/null/absence/order, `app.astrid`, and no legacy write. Keep guarded undo covered by its existing C0/provider/e2e controls; do not issue an undo in this no-write refusal case.

Allowed implementation hunk: the second test in `tests/e2e/local/three-products.p1-chain.spec.ts` only—route fence, actual request/read assertions, real Agent move ordering, unchanged release, and replacement of the stale atomic oracle. No Runtime/Agent/App production or contract change is indicated.

Evidence: Agent pure provider lanes passed `31 passed, 1 warning in 5.16s`; the in-memory real-provider replay returned the exact conflict above. Browser/original P1 e2e and full/build/service lanes remain unverified and were intentionally not run.

