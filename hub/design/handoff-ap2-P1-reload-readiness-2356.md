Implemented the permitted first-case readiness leaf in [three-products.p1-chain.spec.ts](/home/user/work/wt/ap2-P1-reload-readiness-2356/tests/e2e/local/three-products.p1-chain.spec.ts):

- Reused and qualified `openSeededTimeline(page, harness)` after reload.
- Preserved retry observer, timeout ceilings, recovery, request/body/key, owner, restart, drain, history, and all second-case bytes.
- No production/helper/schema/route/outbox changes.

Qualification:

- Offline real-helper control: PASS, exit 0.
- Node: `v20.19.4`.
- Typechecks under lock: all 3 PASS. `run3types` wrapper was unavailable; equivalent commands ran directly.
- Scoped ESLint: PASS.
- Playwright `--list`: exactly 2 tests, PASS.
- `git diff --check`: PASS.
- No browser/full/backend/service run.

Hashes:

- New first leaf SHA256: `eecdb2b41f66ecfe16a3d564f701c3138e39dd214b473c98635c6f7da51cbd72`
- Full spec SHA256: `50960dd2efadc8350b8647a1f7e88a6cad2b44907bf36a7108832ee0ea9ebf17`
- Second leaf unchanged: `4d614d4c8f01e5a53abfa34ff3dd4b59f7dd63908c5`
- Gate 5 blob unchanged: `37caf28577d42fbe98afd2320dffa3c72e6e74b1`

Commit message written; harness commit remains pending. Actual mounted P1 recovery remains unverified/NO-GO pending a future runner.