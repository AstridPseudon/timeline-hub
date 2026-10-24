## Report — U4p/D84a

Adopted Runtime `732c48c6f5a9441a65c61b24595d454a1cd3e180` via normal tooling.

Captured tuple:

- Runtime tree: `7ed0559c6f0a05954427cc668e303b6cd2f51586`
- Agent: `840a58a70aa95fde504deac03b9e6c99a5f286ad`, tree `552152726b9a144a4dc87b567aad606060860ef6`
- App base: `5fcb9ad5cf8af93709d682ab994bcdb1af207f07`
- Schema: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`

Changed only:

- [runtime.lock.json](/home/user/work/wt/app-U4p-D84a-adoption-2212/runtime.lock.json) — SHA256 `bcb969275ae8a5b0f9388860483d568bb189c01b55bd33d152811fc94105dd2a`
- [public/install-manifest.json](/home/user/work/wt/app-U4p-D84a-adoption-2212/public/install-manifest.json) — SHA256 `6c09f4f2846eb0113e6cc8ded6dbccb5d17e80ade819a3ee565ec4bc9bab73d0`

Checks passed:

- Normal sync, vendor-lock, manifest updater
- Updater `4/4`, schema guard `2/2`, skew `2/2`
- Vendor-lock Vitest `15/15`
- Runtime generator and artifact manifest
- Exact producer mappings `14/14`
- JSON, syntax, scoped ESLint, `git diff --check`
- Six protected specs unchanged; placement hash `413d314d…fa4133`
- Asset Git blobs preserved: `b781573f…d35a`, `da9bcb36…f90`

Known limitation: Runtime TypeScript conformance reports pre-existing stale `conformance/typescript/generated.ts` and `contract-metadata.ts`; Runtime remained clean and untouched. No full/browser/service suite was run.

Commit message and `DONE` marker created.