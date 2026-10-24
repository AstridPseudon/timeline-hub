## Report

Blocked before test execution. The mandated `--submit` command exited 1 after ~5.2s:

`D66 source selection: D66 agent source must be a per-request checkout, not its mutable normal home`

Verified exact pins and clean trees:

- App: `63d7c74b6d0ce59bf93002a47912abeb47de5f2e` / tree `992c2b4560f1eab3baa4880b493bff0f16ccf7ef`
- Agent: `039ff2c2187d02b723074a8a6dfcbc6a70544c19` / tree `4e40d897bb1bbbcb8e7ec63f9916c5600deae8cd`
- Runtime: `732c48c6f5a9441a65c61b24595d454a1cd3e180` / tree `7ed0559c6f0a05954427cc668e303b6cd2f51586`
- Composition: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`

Checkout receipts: 4/4 present. Preflight tests: 0. Normal body tests: 0. No suite registry or source changes were made.

Recorded blocker at `.../workers/app-P2-popup-digest-ADD-original-2251/BLOCKED`. No commit message or `DONE` file created.