# App M2 Gate5 — managed marker native fixture

Status: candidate complete; browser qualification remains central-test-service work.

## Exact tree

- App worktree: `/home/user/work/wt/app-m2-sevenjourney-managed-marker-native`
- Changed files: `tests/e2e/local/support/astrid.ts`, `tests/e2e/local/support/harness.ts`, `tests/e2e/local/three-products.spec.ts`
- Source contract checked: Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`

## Old/new fixture mapping

| Existing fixture | Native fixture |
| --- | --- |
| Ingested `f2-placeholder` object | A real `f2.marker` task admitted and settled with `generation.publish_v1`; its immutable output is bound to the same child clip and `f2-placeholder` registry alias |
| Marker task with generic output | Marker task with the same installed capability and generation intent/effect, so its output has a managed generation/variant identity |
| Legacy checkout/edit/publish media swap | Original bundle capture plus `capture_occurrence_swap_media` with exact old/new five-field selections and generated verified-media reads |

The child clip’s `at`, `hold`, type, root/shot/occurrence ownership, opaque data, transition clip, and all strict task/publication assertions remain unchanged. No fake pin, SQL, legacy publisher, Agent wire/API, or authority bypass was added.

## Native guards

- Public generated Runtime SDK reads `get_project_media_selection` and `get_project_verified_media` using the fixture’s actual Astrid credential.
- Association/object/version selection is read first, then rebound to the authored aliases (`f2-placeholder`, `f2-marker`); verified media must echo the exact selection.
- Capture reads the original pinned bundle basis and rejects a bounded page, missing output, or equal old/new object identity.
- The old registry entry is the native media binding (`media_id`, `type`, `generationId`, `variantId`) required by `occurrence.swap-media`.

## Ready central command

Run the central Gate5 suite after the harness/browser build is available:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app full-e2e-three-products)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

This worker did not run browser, build, socket, or full suites.
