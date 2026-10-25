## D100 protected review

### Verdict

- **Source: PASS.** Candidate is limited to the authorized setup host-window change.
- **Behavior/product qualification: UNQUALIFIED.** No behavioral proof was run; retained 2966 result remains **5 failed / 5 errors**. No current-pass claim.

### Exact source map

Candidate commit/tree/blob:

- Commit: `010d0b27ddc406b168345b80757c078e0e8f3989`
- Tree: `834e43060c7c10865223e9fdaba11ef4b8200c78`
- Blob: `33e3d1f3312db059686edb86f9665ecdaa6cc114`
- SHA-256: `6cd578ad65910aff80addc55f6054e2b4b3b5919a5e206eccb9f1fa3bb4363c5`

True baseline:

- Commit: `786385631b8096e50e66b8ecff1e7034c5bc1da9`
- Tree: `d67cd81db76fe410ae7c12009ed6c7db41cba770`
- Blob: `621110f87f0af576097aeeaa92574f18f29e999b`
- SHA-256: `9a44e345bef8de79e66d8ff23626863434b8038ba57b2e7cd6ed3287f7d35097`

Preserved original fixture facts: occurrences at `0/1650/3300 ms`, all `1800 ms`; child clips `at=0`, `hold=1.8`; parent FPS `24`; shared placement inputs `on=13` and `on=6`; opaque/source-window and physical shared topology unchanged.

Exact minima:

- Authored-first: endpoints `53/10`, `323/60`, `29/5`, sibling `14/5`; minimum host `29/5 s = 5800 ms`.
- Original-third: endpoints `2`, `25/12`, `5/2`, sibling `49/5`; minimum host `49/5 s = 9800 ms`.

The prior `2000 ms` value was classified as the setup-only host bound and is explicitly replaced by D100. Authored timing and the unchanged `2000`/`13000`-related inputs remain intact.

AST preservation: five test functions, parameters `[3, 1]`, ten canonical IDs, and all 29 assertions unchanged.

### Checks

- In-memory `compile()` baseline/candidate: **PASS**
- Scoped Ruff candidate/baseline: **PASS**
- Scoped mypy candidate/baseline shadow: **PASS**
- `git diff --check HEAD^ HEAD`: **PASS**
- No pytest, collection, fixture/helper execution, service, browser, CLI, build, or MAIN proof run.

D72 publication entry is withheld until the reviewed Agent exact-arithmetic and same-batch alias fixes exist, followed by the single required ten-case MAIN proof. Candidate was not edited; worktree remains clean. `commit-msg` and `DONE` were created.