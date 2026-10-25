# D100 final receiving report

- Corrected source identity PASS. Only the two permitted metadata hashes were fixed; product/test blobs remain exact.
- Candidate27 PASS: `27 passed in 2.86s`.
- Projection source received byte-exact from `f53b0169…`; SHA-256 `6e41a5bb…a1436`.
- Own9 FAIL: all 9 selectors errored during setup at `candidate.parent.config.theme_overrides.visual.canvas.fps: must be a finite number`. No adaptation or retry performed.
- Projection9 acceptance: NOTRUN.

Evidence:

- `evidence/source1914-corrected-manifest.json`
- `evidence/identity-receipt.json`
- `evidence/source-custody.json`
- `evidence/facts.json`
- `evidence/commands-results.md`
- `evidence/verdict.md`
- Private XML: `private/candidate27.xml`, `private/own9.xml`

Final checks passed: JSON/XML parsing, scoped AST check, `git diff --check`, and exact product/test/projection hashes. Only the approved projection test file is modified. No full suite or browser/native tests run.

Commit message saved; `DONE` marker created.