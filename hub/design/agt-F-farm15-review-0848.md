# F-farm15 Evidence Review — PASS

Reviewed the D48 evidence-only delta against the frozen Farm9cd/45c packet.

- Classification confirmed: **80 environment / 1 regression / 15 unknown**; **0/15 unknowns resolved**.
- All 96 IDs, ordering, Farm tuple identities, and qualified prior-proof scopes validated.
- CSV validated: **31 columns × 96 rows = 2,976 cells**, with complete JSON parity.
- Unknown groups and offsets validated exactly:
  - Shutdown markers: 5
  - Observed-owner markers: 2
  - Render-wire outputs: 6
  - Installer child exits: 2
- No invented stderr, causes, or current-source credit.
- Full v2 request/reply requirements and the “production caller uses it” boundary remain preserved; no caller proof was claimed.
- Current 263/4 official census was untouched.

Publishable tracked files are at worktree root, not under the brief’s `evidence/` paths:

- `farm96-causes.json`
- `farm96-causes.csv`
- `farm96-causes-source-and-limits.md`

Artifact SHA256:

- JSON: `9b9bc96bc6309c8b98d5afa8c3582a88d38d2895f97438f407e1c5044668b896`
- CSV: `d0dd5e799b1d18a6f051642e55077f650af068da6c5a4675b4e5e7c717913da4`
- Source/limits: `8f2f30f37d39ce09f5531700c9132149f7e063767ba71a4c1be5dbd45be45540`

Validation performed with read-only stdlib checks and `git diff`; no product tests, probes, full suites, or recounts were run per instruction. No blockers. DONE marker and conventional commit message were created.