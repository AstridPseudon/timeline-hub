# D141p corrected documentary binding recipe

Status: `NOT_READY`. This is a finite receiving recipe only. It creates no final
binding, imports no module, requests no checkout, submits no service row, and
does not run preflight, a body, or a test.

The exact output root for this packet is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141p-proof-prep-return-0420/evidence
```

## Authenticated tuple

Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` / tree
`ac5b862744bece65b2e30565db1777bacd60da28` and Composition
`635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree
`5ab5191a296980a0a6bcd1178ab6902d6478a148` are known qualified fixed
members. Their exact detached checkout custody and receipt still have to be
received, as does the installed paired Runtime kit; they are not missing
producer-qualification gates.

Only a genuinely qualified new Agent head and a genuinely qualified new App
head may fill the other two tuple positions. The held App `8f278b91…` and
historical App `520d7e4f…`/Agent `28e56cac…` are not final inputs. Existing
D141p/D141l authority already covers final-head proof when the qualified source,
installed kit, and admission are ready; no new MAIN approval wait is allowed.

Before accepting a tuple, the later caller must retain, for every source, the
full commit and tree, detached clean checkout path, parent/origin identity,
source manifest, and receipt that authenticates those exact Git facts. It must
also retain the installed Runtime kit's source/review/CAS hashes and supported
admission/continuous-trace interface. A string receipt, boolean `clean`, or
boolean `qualified` is not enough.

## Placement and selector source

Placement is first. The held-8f/current-520d Git file
`tests/e2e/local/three-products.p2-elements-assets.spec.ts` is blob
`186ba03b6a8bb5d45d2659cf0a1b647b68e5a149`, SHA-256
`ec63d7f5728be8d6a8cd41d2bc83cf7353ac4c2543c9ae15729972c1faf3039e`.
The prior `7cca7827…` claim is stale and must not be bound or run. The approved
D141d/0243 expectation remains exactly two `commit.materialization` bindings
and the complete 22-path structural family, including the full history,
reload, and guarded-undo tail.

The eight selector IDs, order, source blobs, and full-file SHA-256 values are
in `source-manifest.json`. The later caller must use those exact source files
and preserve all their tails. The order is:

```text
p2-automatic-child-placement
p2-popup-add
p2-parent-move
p2-transition-none-single
p2-transition-none-bulk
p2-register-asset
p1
p3
```

## Existing production builder

The later source owner must use the actual final App module
`scripts/testing/d66-plain-stack.mjs`, not an arbitrary supplied module. Before
importing it, the caller must verify its Git blob and SHA-256 from the genuine
final App checkout. The historical held/current module is blob
`59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA-256
`2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`, 49,914
bytes, exporting `buildSubmitPlan` and `serviceRecipe`; this proves only API
continuity, not final-source qualification.

The production caller uses the existing APIs with genuine pins and checkouts:

```js
buildSubmitPlan({
  name,
  target: `app-pin-${app.head.slice(0, 8)}`,
  paths,
  pins: fixedPins,
  checkouts: fixedCheckouts,
  checkoutRoot,
  receiptRoot,
});

serviceRecipe({
  name,
  pins: fixedPins,
  checkouts: fixedCheckouts,
  preflight: false,
  diagnosticHelper: null,
});
```

The production caller records the exact UTF-8 command bytes without a terminal
newline and their SHA-256, then the exact registered row bytes with one LF and
their SHA-256. `registration=false` remains prospective in this packet. Before
either paired part runs, actual registered bytes must equal the genuine builder
output byte-for-byte. No guessed binding or output is present here.

## C0 v2 wire preservation

The caller must preserve the approved request spelling and envelope exactly:
`api_version`, `project_id`, `timeline_id`, `base_revision_id`,
`base_publication_id`, `commands` with `schema_version`, `op`, `version`,
`select`, `args`, and `created`, `label`, `steps` with `id`, `label`, `intent`,
`tags`, `command_ordinals`, `patch`, and `reads`, `merge` (`fields` or
`atomic`), `reads`, `Idempotency-Key`, `dry_run`, `source`, `rationale`, and
`group_id`. Do not change the envelope or code names.

Accepted and merged replies preserve the exact `{data, receipt}` envelope, with
`canonical_document`, `document_digest`, `commands` (the normalized commands
recorder), `id_map`, `provider_version`, `compiler_version`, complete `steps`,
`base_revision_id`, `base_publication_id`, `previous_revision_id`,
`previous_publication_id`, `accepted_revision_id`, `rebased_onto`,
`merge_mode`, `records`, `bindings`, `effects`, `dependencies`, `history`,
`undo_steps`, `publisher`, and echoed `source`, `label`, `rationale`, and
`group_id` annotations. Landing is represented by the accepted revision pair
and, for a merged result, `rebased_onto`; no invented `landing` key is added.

Conflict replies preserve `reason` and the actual `head`/current pair. Invalid
replies preserve `code`, `path`, `hint`, and `suggested_command`. Preview
success preserves `would_status` and a null `receipt`. The production caller
must consume these actual C0 fields; it must not replace them with a summary or
new receipt schema.

