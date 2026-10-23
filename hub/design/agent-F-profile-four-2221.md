## Diagnosis

**Source/content: PASS. Qualification/custody: FAIL/UNVERIFIABLE.**

The four additions are deterministic registry outputs, not arbitrary contamination:

- `.astrid-registry-state.json`: `d609b44b37d724358a33405e9d8539008fd1ac30bc2f0d9746575c3fbadaac96`
- `src/animations.generated.ts`: `02326f12177879eb5905f9d9b6d476b2de185928ddeeeeb2321a68ebffb47ad6`
- `src/effects.generated.ts`: `127e5653e0c66993726f8334b9f4ac122d24cdfbaa9e70cdaa142189afcf2bbe`
- `src/transitions.generated.ts`: `c46d6bbd88712e775812867ec1cbe6de67473664775266c5a0b9317344ceb989`

Computed registry state hash: `32b312f5ea7b2a67717a79ae71b539510590e9010e2ec7f77c8bce1edbabbfc6`.

Private offline generation reproduced all three files byte-for-byte and matched the state file exactly. Generator/runtime output paths also matched.

## Cause and custody

- The generator intentionally writes the three host `src/*.generated.ts` files under lock: `astrid/core/rendering/_effect_registry.py:25-31,337-370,631-659`.
- Runtime settlement intentionally binds and may write those three files plus `.astrid-registry-state.json`: `astrid/core/rendering/remotion_runtime.py:758-851`, `astrid/packs/rendering/rendering/renderers/remotion/run.py:328-332,404-481`.
- The installer only performs dependency installation and environment staging; it does not invoke registry generation: `astrid/installer/backend.py:60-73,367-410`.
- D22 service `2130` failed at installed source binding (`remotion_runtime.py:717-721`) before any generator success/write receipt. The `16:17:09Z` timestamps therefore establish proximity only, not creator custody.

Exact creator remains **unverifiable**. No files were deleted or modified.

The durable pre-contamination evidence proves `21,501` regular files, `33` links, read-only profile, and passing lock/archive/installed-origin checks. A complete per-file manifest was not retained, so byte-for-byte identity of every original regular file is **UNKNOWN**.

## Contract conclusion and remedy

The fixed preflight check is too strict for the supported runtime contract: `preflight.py:113-118` requires exactly `21,501` regular files and all read-only, while production tests intentionally generate these outputs in temporary projects (`tests/packs/rendering/test_remotion_backend.py:906-1001,1108-1125`).

Recommended harness-only qualification contract:

- Preserve the original `21,501` immutable regular-file baseline and `33` internal links.
- Permit exactly these four runtime registry paths, making the expected total `21,505`.
- Require the four hashes/state hash above and generator/source-binding validation.
- Preserve all archive bytes, installed package bytes, lock hash, origin checks, and non-registry immutability checks.

## Evidence

- Prior central preflight: six boot cases passed; profile inventory failed only on `21,505` vs `21,501`.
- D22 service: `108 passed, 1 failed`; failure was installed registry source binding before generation.
- No full run was submitted; zero full nodes executed.
- Worktree remains clean; no product, test, profile, generated, pin, or provisioning files changed.