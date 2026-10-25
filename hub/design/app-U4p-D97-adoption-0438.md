## Report — U4p/D97

Adopted released Runtime provenance using normal tooling.

Captured tuple:

- Runtime: `0c62dfa63db9ff608ac9338388431e31a814e080`, tree `e22cdd54b668acea9fe593e6724b34d1a56f7530`
- Agent: `5faeec5bbced687f040751ded739e1b9c8c41757`, tree `455b16e8b6384abde89b4e1187e7e7317fe8cab7`
- App base: `1e34f8eac5e3d5a54dbba12d538a7f3bf8509b66`, tree `73b0a07be3ffdc86d82d6dc45f1584113dff1dcb`
- Schema: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`

Changed only:

- `runtime.lock.json` — `fd41c1a27cf466f69009cf6708b68eadda38e3428bb3f8b6d1f3f08657050de5`
- `public/install-manifest.json` — `e99e7b12ae551e07afb259f3c2452349f240fb35b5c3298488f4cd5a0a5dd026`

Checks:

- Normal sync and manifest updater: PASS
- Updater/manifest tests: 4/4
- Schema guard: 2/2
- Manifest skew: 2/2
- Vendor-lock Vitest: 15/15
- Exact producer mappings: 14/14
- Runtime artifact manifest: PASS; artifact tests 3/3
- JSON, syntax, scoped ESLint, `git diff --check`: PASS
- Canonical generated client/schema bytes unchanged
- Six protected specs and two protected source blobs unchanged

Known limitation: Runtime generator tests reproduce the documented pre-existing stale conformance outputs: 2 failed, 4 passed. Runtime checkout was not modified.

No full/browser suite was run. Full P2 is the next step and remains manager-owned.

Created `DONE` and commit message:

`chore(app): adopt Runtime D97 release provenance`