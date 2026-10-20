# App M2 seven-journey managed-native review

Verdict: REJECT.

The managed-marker/native migration is contract-correct, but the completed candidate is not ready to combine because it is based on b1 without the required Gate 5 shared-seed reset from `571e93a15b946983b38f7054ae2d01b573cc6b9b`. The candidate's serial worker fixture leaves `f2-app-clip` at position 5 after the earlier M1 journey; Gate 5 still calls `prepareAfterAckLossMoves` as though the clip were at 0. The missing hunk is the existing 5-line reset, and must be applied to the candidate/new setup rather than to the older b1 root:

```ts
const resetResponse = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);
await dragTimelineClip(page, seed3.appClipId, seed3.transitionClipId, 5, 0, THREE_PRODUCTS_REFERENCE_AT);
const reset = await resetResponse;
expect(reset.status(), await reset.text()).toBe(200);
await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).every((item) => !item.pending && !item.intents.length), CEILING).toBe(true);
```

Insert it in `tests/e2e/local/three-products.spec.ts` immediately before the Gate 5 `prepareAfterAckLossMoves` call (the candidate's Gate 5 starts at current line 1015). The candidate already has a separate reset in the later dependency-conflict case at lines 1141-1145; that does not repair Gate 5.

## Exact source and tree

- Base: App `b1ef4b9b910ba72375c34cf319692f90d22edc25`, tree `8d8a10b057ed31fed69517e18a23b8ec3811447a`.
- Candidate reviewed: `tl/app-m2-sevenjourney-managed-marker-native`, commit `dc6c4aa3bb1c025ef109802bc307ecce973415ce`, tree `93cefc7f5361b90a8f7905046d1c52f084bc6463`; parent native-write commit `d0ba426e0922501e59985f504579fbcaf879b1f3`.
- Separate reset source: `571e93a15b946983b38f7054ae2d01b573cc6b9b`, tree `6e232ce33acb10ac1a8462d3d5cba1eee553ae46`; it is based on b1 and is not the candidate tree.
- Frozen Agent checked: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, tree `75354d38c898729bac09619679f5421faba319ed`.
- Frozen Runtime checked: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.

## Change map and review

- `tests/e2e/local/support/astrid.ts:199-258` admits and settles a real `f2.marker` task through the public CLI, reads managed outputs, then uses the generated Runtime client for association/object/version selection, alias selection, and verified-media reads. The frozen generated contract has the exact five fields `asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`; the code asserts `verified.selection == selection`.
- `tests/e2e/local/support/astrid.ts:260-368` captures the original pinned bundle, uses current `State` rows for hold extension and explicit asset clear, and calls frozen Agent `capture_occurrence_swap_media` with the original owner selection, old five-field media selection, new five-field media selection, and both `VerifiedMedia` values. No private provider, raw custody fake, direct SQL, or compatibility publication was added. The duplicate `body_commands = [command]` assignment at lines 351-352 is harmless but should be removed as cleanup.
- `tests/e2e/local/support/harness.ts:689-750` binds the real managed placeholder output to the authored `f2-placeholder` alias and retains the task id for the old-media read. The registry binding remains the native managed identity (`media_id`, `type`, `generationId`, `variantId`), while the full five-field selection is re-read through Runtime for the actual swap.
- `tests/e2e/local/three-products.spec.ts:45-62` changes fixture setup to create the managed placeholder before publishing the authored bundle. Case 1's original task, event-feed, completion, no-reload, Runtime-head, App follow-up, root/occurrence, opaque-data, and readback assertions remain one-to-one; only legacy checkout/edit/publish writes are replaced with the native commit.
- `tests/e2e/local/three-products.spec.ts:473-480` replaces the concurrent Agent writes with a native batch: hold is computed from the current pinned row and asset is explicitly cleared. The existing positive transition/opaque/root/readback and Keep/Use-latest assertions remain. The existing legacy whole-document conflict is retained as an overwrite-risk conflict, not presented as a native disjoint-command conflict.
- The candidate has no product-source changes; all changes are test fixture/helper changes. Existing `/composition-revisions` references are fixture seeding and the App legacy-route observation, not a new Agent publication path.

## Commands and results

- `git diff --check b1ef4b9b910ba72375c34cf319692f90d22edc25 dc6c4aa3bb1c025ef109802bc307ecce973415ce` — passed.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/astrid.ts tests/e2e/local/support/harness.ts tests/e2e/local/three-products.spec.ts` — passed. `node_modules` remains the read-only symlink to `/home/user/work/app/node_modules`.
- Frozen Agent ref was extracted to a private temporary directory without checking out or modifying the frozen worktree. `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private-frozen-agent> /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider <private-frozen-agent>/tests/editing_conformance/test_recipe_occurrence_media.py --basetemp=/tmp/app-m2-sevenjourney-native-review-pytest` — 56 passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private-frozen-agent> /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider <private-frozen-agent>/tests/sdk/test_workspace_client_timeline_commit.py -k 'media or commit' --basetemp=/tmp/app-m2-sevenjourney-native-review-client-pytest` — 9 passed.
- Offline signature checks against frozen Agent d874 and generated Runtime client passed: `capture_occurrence_swap_media(..., *, verified_media=...)`, `get_project_media_selection`, `get_project_verified_media`, `list_managed_outputs`, and the five-field `MediaSelection` contract are present and match the candidate calls.
- No full suite, browser, localhost/socket, build, TypeScript check, install, or central test-service request was run.
- App worktree status after review: clean; no source edits, merge, or qualification claim.

## Central seven-gate status

1. Lossless semantics — not centrally run; frozen native occurrence controls passed.
2. Atomic acceptance — not centrally run.
3. Renderer-independent save — not centrally run.
4. Transport — not centrally run; generated-client boundary controls passed.
5. Adversarial App journey — blocked for this candidate until the Gate 5 reset hunk above is combined; browser qualification remains central-service work.
6. One writer, one viewer — not run.
7. Delivery — not run.

After the exact reset is combined on top of the candidate, central should run the named native Gate 5/three-products lane with the frozen Agent d874 and Runtime 2c4 pair. This review does not release any gate.
