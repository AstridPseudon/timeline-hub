# P2 popup SWAP source comparison

## Pinned run

- Suite: `app-pin-bceb0350-d73-popup-swap-profile-2250-v2-bceb0350-1024230205-25174`
- App commit/tree: `bceb0350326f22beefdde5c5ba275412bb09b419` / `46ad4dde505a376e22026c3377615a5fca05a55e`
- Agent commit/tree: `039ff2c2187d02b723074a8a6dfcbc6a70544c19` / `4e40d897bb1bbbcb8e7ec63f9916c5600deae8cd`
- Runtime commit/tree: `732c48c6f5a9441a65c61b24595d454a1cd3e180` / `7ed0559c6f0a05954427cc668e303b6cd2f51586`
- Composition commit/tree: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148`
- Original result: readiness passed; popup SWAP received HTTP 422 with `reason=invalid_records`, `status=refused`, and `message=provider executed a different command`.

## Exact comparison

1. App production builder: `src/tools/travel-between-images/components/shotTimelineDataProvider.ts:866-868` emits the second command with `op=occurrence.swap-media`, `select=occurrence:<occurrenceId>/clip:<id>`, and `args={old_media,media}`, but no `created` claim.
2. The same builder's ADD branch at `:834-846` declares a new occurrence asset when it is absent from the prior registry, and declares the new clip. This establishes the intended caller-side allocation pattern.
3. Agent production provider at `astrid/sdk/timeline/native_occurrence_media_commands.py:264-275` calls `_registry(..., create=True)` when the new media alias differs from the current alias. `:287-293` captures SWAP without a caller-supplied `created` field.
4. Agent recorder at `astrid/sdk/timeline/_recording.py:246-270` sets authoritative `command['created']` from recorded allocations. The SWAP's new registry alias therefore produces one generated occurrence asset ref when that alias is not already present.
5. Agent `commands.py:300-304` preserves the generated record and `:303` restores original claims except `intent`; it does not erase the generated `created` list.
6. Runtime `runtime_protocol/timeline_commit_auth.py:318-327` compares the submitted command tuple `(schema_version, op, version, select, args)` and then compares submitted `created` (default `[]`) with the provider record's `created`, allowing only the documented inverse/track-create omissions. SWAP is not one of those omissions.

Therefore the decisive mismatch is `commands[1].created`: submitted absent/`[]`; provider authoritative record contains one newly allocated occurrence asset reference. The core tuple and media pins are not the implicated comparison. The retained browser trace does not preserve raw request/record bodies, so the exact alias is intentionally not published.

The retained test source establishes the missing-allocation precondition: setup declares only the imported old asset at `three-products.p2-popup.spec.ts:270-296`, then supplies distinct new PNG bytes at `:302-303`; the SWAP path therefore targets a new alias absent from the baseline occurrence registry.

## Contract and correction boundary

C0 `contract/commit-v2.md:~570` says caller-generated native `created` claims list canonical entity refs and must be declared in the same command envelope. The bounded minimum correction belongs to the App SWAP builder: add the conditional occurrence asset claim used by ADD (only when `newAsset` is absent from `beforeRegistry`), e.g. `created: [\`occurrence:${occurrenceId}/asset:${newAsset}\`]`; keep it empty/omitted when the alias already exists. Do not weaken Runtime equality or introduce a SWAP exception.

No product, test, schema, pin, or Runtime files were changed in this worker.
