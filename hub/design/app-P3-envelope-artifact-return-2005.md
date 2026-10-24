## PASS — P3 artifact return

Added retained artifacts under [evidence/p3-envelope-artifact-return-2005](/home/user/work/wt/app-P3-envelope-artifact-return-2005/evidence/p3-envelope-artifact-return-2005):

- Corrected [proposal.md](/home/user/work/wt/app-P3-envelope-artifact-return-2005/evidence/p3-envelope-artifact-return-2005/proposal.md)
- Byte-identical [proposal.patch](/home/user/work/wt/app-P3-envelope-artifact-return-2005/evidence/p3-envelope-artifact-return-2005/proposal.patch)
- Machine-readable hash/predicate map and `SHA256SUMS`
- Independent 21-mutation envelope control and hash-reproduction control

Correction: only the published virtual hash was wrong.

- Base: `736fd381…491e05`
- Patch: `80127a0b…46733`
- Correct virtual: `93c2bf4c…a64b`
- Helper: `312ded75…390c2`
- B regions: `67e2292e…434b6` → `f0c857e3…e54f5`

Validation:

- Envelope control: **PASS**, canonical fixture + 21 mutations.
- Node20 Gate-5 fault-order test: **PASS**, 3/3.
- Exact hash reproduction: **PASS**.
- `git apply --check --whitespace=error`: **PASS**.
- Syntax, JSON parse, and `git diff --check`: **PASS**.
- No product/protected-test source was changed; no browser, live, full, or original P3 run performed.

The protected scope decision and any eventual proposal application remain pending orchestrator approval. `DONE` and the P3 commit message are present.