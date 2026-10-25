## Result

Adopted the qualified Runtime D102c release using the normal tooling.

Changed only:

- `runtime.lock.json`
- `public/install-manifest.json`

Pins:

- Runtime: `1daca2a33f6d7b10053e07c539a54843e3984e19`
- Runtime tree: `a522511414947e48e317a5e5c2103483b121a750`
- Agent: `8c88ea8f06b65f9b79fb7810af04720845c5cc6f`
- Agent tree: `cd2a51721f07b447215f4084980d385de3842fd9`
- App base: `f0fcdce17841a6b4bb09521c52610010745325d4`
- Schema digest: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`

Release identity was confirmed as Runtime contract `0.2.14`. The 14 existing vendor mappings and producer version were preserved.

## Verification

Passed:

- `node scripts/sync-runtime-client.mjs /home/user/work/runtime`
- Manifest updater `--plan` and `--write`
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/runtime`
- Installer, manifest, and schema-guard Node tests: 6 passed
- Vendor-lock and install-skew Vitest tests: 17 passed
- Generated client/timeline tests: 77 passed
- Scoped ESLint
- JSON syntax, pin/mapping checks, and `git diff --check`

Node available was `v22.22.0`; Node 20-specific execution is unverified. No full suite was run.

No product source, schema, protected files, or unrelated branches were changed. Completion marker and conventional commit message were written.