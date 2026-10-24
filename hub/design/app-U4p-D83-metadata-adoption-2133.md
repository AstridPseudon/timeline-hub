## Report

Adopted U4p/D83 metadata provenance using normal tooling.

Captured tuple:

- App base: `ce1cd9c439ee5fdf0f6d8801f7825235fb03a761`, tree `4f73d76b…`
- Runtime: `bc04caa23f4b503fc55e49769ead20677904702a`, tree `fa696b34…`
- Agent: `5fc1f300fb4fe5913a7bdc990b1f531402c2f258`, tree `a1703333…`
- Schema: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`

Changed only:

- `runtime.lock.json` — SHA256 `31579710…`
- `public/install-manifest.json` — SHA256 `e3f64acf…`

Commands/checks:

- Normal sync, producer-aware vendor-lock: PASS
- Manifest/updater controls: 4/4
- Schema guard: 2/2
- Manifest skew: 2/2
- Vendor-lock Vitest: 15/15
- Runtime generator and artifact manifest: PASS
- Exact producer mappings: 14/14
- JSON, syntax, scoped ESLint, protected six-file hashes, `git diff --check`: PASS

Runtime TypeScript conformance reports the known pre-existing stale outputs (`conformance/typescript/generated.ts`, `contract-metadata.ts`); Runtime was not modified.

Commit message written to the required path and `DONE` created.