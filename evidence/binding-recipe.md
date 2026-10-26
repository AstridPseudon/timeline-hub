# D141p freeze-2 paired binding recipe

Status: `NOT_READY`, source-only. This packet prepares the receiving recipe; it does not create a final binding, register rows, request checkouts, or run a preflight/body.

## Final source gate

Keep App candidate `8f278b91accec5852e39bb84822e99124fccb81d` unmerged. Agent freeze-2 merge-forward and qualification come first. After the genuine qualified App head is available, only the App source worker runs `scripts/installer/update-manifest.mjs` through its normal tools and reports the resulting manifest/vendor provenance. The candidate tree and a hand-edited future SHA are never a final input.

The final tuple must provide full 40-character App, Agent, Runtime, and Composition commit/tree identities, exact detached receiving checkouts, clean status, parent/origin identity, source receipts, and the installed Runtime paired-kit receipt. Composition is fixed at `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148` as the tiny documentary host. Current App `520d7e4f` and Agent `28e56cac` are historical inputs only.

## Production builder API

The authenticated source is `scripts/testing/d66-plain-stack.mjs`. The candidate `8f278b91…` and current `520d7e4f…` both resolve `serviceRecipe` to blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA-256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`, 49,914 bytes. This proves API/source continuity only; the final caller must import the builder from the genuine final App source receipt.

The pure functions are:

```js
buildSubmitPlan({
  name,
  target,
  paths,
  pins: fixedPins,
  checkouts: fixedCheckouts,
  checkoutRoot,
  receiptRoot,
})

serviceRecipe({
  name,
  pins,
  checkouts,
  preflight: false,
  diagnosticHelper: null,
})
```

`buildSubmitPlan` validates the named suite and returns `{name, target, pins, checkouts, checkoutRequests}`. The later D66 `--submit` caller owns receipt-backed checkout requests and must use this normal path. For a source-only binding regeneration, use the later genuine receipts as fixed `pins` and `checkouts`, call `buildSubmitPlan`, then call `serviceRecipe` twice. Do not hand-construct command strings.

Use `target = app-pin-${app.head.slice(0, 8)}`. Preserve the established pair naming convention:

```text
d141g-${selector}-${app.head.slice(0, 8)}-submit
d141g-${selector}-${app.head.slice(0, 8)}-submit-preflight
```

The first pair is placement; `d141g` is retained because this is the D141g-a paired admission carried onto freeze 2. Registration remains false until the normal D66 `--submit` path atomically installs both rows.

For each selector, record the exact `serviceRecipe` result as UTF-8 bytes without a terminal newline. Hash that command byte string with SHA-256. The registered row is exactly `app <suite-name> <serviceRecipe-output>` followed by one LF (`0x0a`); hash those row bytes separately. Before either paired part runs, the actual registered row bytes must equal the final production-builder output byte-for-byte. Preserve raw/private outputs and `KEEP` markers.

## Eight original selector identities

The source files and SHA-256 spec blobs are unchanged and are fully recorded in `source-manifest.json`:

1. `p2-automatic-child-placement` — first; `three-products.p2-elements-assets.spec.ts`, `7cca78274f96c9466d82bea3108f6f8a447462c9cd722c078ab958bc3578d637`.
2. `p2-popup-add` — unchanged D141j popup; `three-products.p2-popup.spec.ts`, `09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9`.
3. `p2-parent-move` — `three-products.p2-tour.spec.ts`, `83948c53c7990824fce81be7f0db2b4f947837c66a827abf2ffb08492f09bee4`.
4. `p2-transition-none-single` — same tour blob/hash.
5. `p2-transition-none-bulk` — same tour blob/hash.
6. `p2-register-asset` — `three-products.p2-elements-assets.spec.ts`, same `7cca…8d637` blob.
7. `p1` — `three-products.p1-chain.spec.ts`, `50960dd2efadc8350b8647a1f7e88a6cad2b44907bf36a7108832ee0ea9ebf17`.
8. `p3` — `three-products.spec.ts`, `93c2bf4c72ac3c91442a1a52174e36311113751ab9d8b7e0f52e4a958559a64b`.

The exact execution order is placement first, then the other five P2 selectors, then P1 and P3: placement → popup ADD → parent move → single clear → bulk clear → registerAsset → P1 → P3. Each selector gets its own paired preflight/normal names and command/row hashes.

## C0 v2 wire preservation

The production caller must preserve the complete request: `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, `commands[schema_version,op,version,select,args,created]`, `label`, `steps[id,label,intent,tags,command_ordinals,patch,reads]`, `merge` (`fields|atomic`), `reads`, `Idempotency-Key`, `dry_run`, `source`, `rationale`, and `group_id`.

Replies retain `accepted`, `merged`, `data`, canonical `receipt`, `digest`, `normalizedcommands`, `idmap`, `base`, `previous`, `accepted`, `landing`, `rebased_onto`, `merge_mode`, `records`, `bindings`, `effects`, `dependencies`, `history`, and `undo_steps`; conflicts retain `reason` and `head`; invalid replies retain `code`, `path`, `hint`, and `suggestedcommand`; previews retain `would_status` and a null receipt where required. No contract or semantic source review is part of this packet.

## Pure receiver

The optional `pure-builder-receive.mjs` in this evidence directory is inert until a later worker supplies genuine receipts. It rejects draft `8f278b91…`, historical `520d7e4f…`, and old Agent `28e56cac…`, validates full IDs/checkouts/receipts, and uses the actual `serviceRecipe` export for both paired command outputs. It emits prospective bytes/hashes only and never registers or executes a row.
