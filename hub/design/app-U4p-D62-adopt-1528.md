## Report

Prepared branch-only App adoption from Runtime producer:

- Commit: `e02f3e3d9d972be74450536ec0ee49e8bc51c2ec`
- Tree: `a095ecbe8b01b0ff0a7825c4c19bbf41120ec3ed`
- Producer version: `sha256:084f3f2510edff28c18d33aac4a459f8aa6df3cb4fd71cba4fb292274ea8de5`
- Schema digest: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`

Changed only:

- `runtime.lock.json`
- `src/integrations/runtime/generated-contract-metadata.ts`
- `src/integrations/runtime/timeline-commit-types.ts`

All 14 lock mappings match producer manifest and bytes. Generated client and vendored schema remained byte-identical. `HistoryEntry.recorder_abi` is optional `1 | 2`; legacy history fields/default omission remain intact. Commit requests contain no `recorder_abi` authority field.

Tests/checks passed:

- Normal sync tool
- Producer-bound `vendor-lock` check
- Astrid CLI vendor-lock check
- Runtime schema guard: 2 passed
- Vendor-lock Vitest: 15 passed
- Recorded responses + client Vitest: 54 passed
- TypeScript app/node checks
- ESLint on changed files
- `git diff --check`

An initial Vitest `--configLoader runner` attempt failed due the existing config’s `__dirname` usage; the normal bundled loader passed.

Status: branch prepared only. Home merge remains held pending Runtime security PASS and producer handback. No full/browser suite run. Commit message and `DONE` marker created.