## Report

Completed U4p/D65 provenance adoption.

Changed only:

- [public/install-manifest.json](/home/user/work/wt/app-U4p-current-provenance-1635/public/install-manifest.json)
- [runtime.lock.json](/home/user/work/wt/app-U4p-current-provenance-1635/runtime.lock.json)

Pins:

- Runtime: `bc227de07262accb702eae8a44c4a666b568c08e`, tree `1d410a674d827979caf10d2da2ce3767b68c75da`
- Agent: `9a781a38f747ccf97274c22779b941f52184aa97`, tree `71574688d7195d804fdce961b67dbdbfb11cf920`
- Schema: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`

Runtime tree exactly matches reviewed `760269` tree. Runtime producer version remains `sha256:084f3f…ea8de5`.

All 14 producer mappings matched App bytes and lock hashes; mapped bytes and canonical schema/client bytes are unchanged from `8b32`.

Checks:

- Normal sync tool: PASS
- Vendor-lock check: PASS
- Installer updater tests: 4/4 PASS
- Manifest skew Vitest: 2/2 PASS
- Runtime schema guard: 2/2 PASS
- Runtime generator `--check`: PASS
- Runtime artifact manifest `--check`: PASS
- Updater post-write `--plan`: PASS, no changes proposed
- Syntax, JSON validation, `git diff --check`: PASS

Known unrelated issue: Runtime TypeScript conformance `--check` reports two pre-existing stale files (`conformance/typescript/generated.ts` and `contract-metadata.ts`). No Runtime files were modified.

Commit message written and `DONE` marker created.