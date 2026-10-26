## Result: PASS — bounded installation review

- Verified canonical hashes/modes:
  - `README.template.md`: `90f8…e7b84`, regular `0644`
  - `gate-results.md`: `ddebb…500bc1`, regular `0644`
- Exact preimage backups match requested hashes.
- Recomputed all 568 outside files; before/after maps are equal and every path/hash/byte count/mode matches.
- Confirmed one successful guarded CAS, replacement order README → gate results, durable backups/fsync/readback, and no second CAS.
- Exact checker: `PASS_PRIVATE_D141GG_CANDIDATES`.
- `json.tool`, conservation checks, and function-only `render_readme` with fallback: PASS.
- Worktree remains clean; no product files changed.

Limits retained: historical `FAIL_CUSTODY_NATIVE_TEST_PASS`, missing first-tool trace window, and discrete monitor gaps remain explicitly disclosed. The new sampler cannot repair historical custody.

Evidence is in the required `evidence/` set. Commit message and `DONE` marker were created. No product/full-suite/build/service/ZIP tests were run.