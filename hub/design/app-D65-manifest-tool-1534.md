## Done

- Added guarded owner command: `scripts/installer/update-manifest.mjs`
- Added positive/negative tests and registered them in `test:node`.
- Public manifest remains unchanged pending D62 adoption.

Tests:

- `node --test ...manifest.test.mjs ...update-manifest.test.mjs` — 4/4 passed
- `--help`, current-head `--plan`, syntax checks, JSON validation, and `git diff --check` — passed

Current plan tuple: Runtime `e68cf231…`, Agent `d27b6601…`, schema `sha256:4118…`.

Follow-up apply command:

```sh
node scripts/installer/update-manifest.mjs \
  --runtime-checkout /home/user/work/runtime \
  --agent-checkout /home/user/work/agent \
  --write
```

This must run after D62 adoption and fresh owner-merged heads.