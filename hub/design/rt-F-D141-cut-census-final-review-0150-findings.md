# D141 final census metadata review

## Decision

**PASS for both 0137 findings and for remaining real defects, scoped to finite preparation only.** This is not a behavior, REG, preexisting, product-fault, or zero-REG verdict.

## Finding 1 — mutable queue `why` hashes

**PASS — closed by explicit history.** The original 0132 claimed hash, the 0137 observation, the 0143 derivative observation, and the 0150 current-as-of observation are recorded separately:

- 0132 claim: `186892ceda5ead968acf6748cc708ab4bea1cb7aa6be2770f2dcf32727da2905`.
- 0137 observation: `9bbf7539757ca42cce991a9ca3b16b33f5adc92cc3eb139dbb1839a8ac37d971`.
- 0143 observation at `2026-10-26T01:45:20Z`: `c40e7d0abdc1f974fcf152b67deed2536ae558f68bd3899f8a870e36bf8b2327`.
- 0150 current observation at `2026-10-26T01:51:20Z`: `bd4e7df129271887473d0d8a5d6f48de5df39ed6d17e2abb2008f7d2e9c5061e`.

The file is mutable queue-admission diagnostic text. The hashes are not asserted equal, historical bytes are not claimed to remain available, and no refresh, comparator result, immutable test proof, or behavioral proof is implied. The queue is still `queued`; its low-disk admission is ordinary admission handling. The earlier “queued safety denial” wording is a textual mislabel, not evidence of an actual safety or permission denial. Future `why` changes are expected and are not a new failure.

## Finding 2 — tree placeholders

**PASS — closed from immutable Git objects.** The derivative uses actual commit/tree pairs for Composition, Runtime cut/pristine, and Agent cut/pristine. Independent `git rev-parse` and object-type checks match every recorded pair, all five worktrees are clean, and no unresolved placeholder remains. The original defective 0132 manifest is preserved as historical evidence and was not rewritten.

Resolved pairs:

| Source | Commit | Tree |
| --- | --- | --- |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` |
| Runtime cut | `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` | `ac5b862744bece65b2e30565db1777bacd60da28` |
| Runtime pristine | `fa9cd5464a8b37b02f971de375e56be846cd69e2` | `124e10dbcd54fb90219e783ec11aa34f8c91590c` |
| Agent cut | `28e56cacb42d3da85b02e5b3543895b44f3d0f70` | `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a` |
| Agent pristine | `8b6ed2116fd1803d24b2be5bc08bd9490407fe4a` | `0a3691a49b63fd7b0c22fb3478e9cf1947f266ed` |

## Preservation and limits

The original 0132 `cut-failures.json`, `selector-map.json`, source manifest, retained cut XML, and retained artifact-hash references remain byte-exact historical references. Counts `7392` / `53`, `15` exact mappings, `38` `NEW_OURS` bounded rename checks, privacy, and exact source custody are reused from the independently passing 0137 review; no broad repeat was performed. The 53 original records remain `UNCLASSIFIED_NO_SAME_ENV_COMPARATOR` / `NONE` until the actual same-environment comparator runs.

No tests, imports, collection, lint, typecheck, provider, body/capture, source, product, C0, registry, pin, fixture, custody-framework, or Git-ref changes were made.
