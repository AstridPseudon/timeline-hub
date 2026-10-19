Implemented the reviewed Runtime refresh.

- Pinned Runtime integration SHA `182a7dd8446456162a452a25c8493256c5da29fe`
- Release `0.2.1`
- Schema digest `sha256:4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d`
- Artifact aggregate `sha256:9b18a553108535606aed239ab946c89c9609b1d8c1515d229395691964b87e4d`
- Preserved compiled timeline-config pin `sha256:f52b8202…`
- Receipt `project_seq` now matches main as `[number, number]`
- Lock retains 13 files and all 9 response fixtures

Checks passed:

- Vendor-lock update/check
- Byte/hash audit against Runtime SHA
- `npm run test:contracts` — 1 passed
- Runtime integration Vitest lane — 77 passed
- Central `vendorLock.test.ts` — 13 passed
- ESLint and `git diff --check`

Changed only the three official generated/lock files. Commit message written to the requested path.