# D141hh independent installation review

## Verdict: PASS_BOUNDED_CAS

The exact reviewed README and gate-results candidates are installed. Both canonical files are regular `0644` files, equal their candidates, match the requested SHA-256 values, preserve the exact predecessor backups, and append one suffix only. Gate-results retains all 32 numbered IDs and the prior ledgers, witnesses, gaps, and limits.

The immediate before/after inventories contain 568 entries. I recomputed every current outside entry against both maps by full path, SHA-256, byte count, and mode; all 568 entries match and the maps are equal. The retained installer source in `log.txt` shows the ordering: durable before-map, exact backups and fsyncs, staged candidate/rollback files, guarded README-then-gate atomic replacements with directory fsync after each, cleanup, readback, and durable after-map. The wrapper and finalization records support one successful CAS only; there was no second CAS or canonical rewrite.

The required immutable checker was run exactly without `--write` and returned `PASS_PRIVATE_D141HH_CANDIDATES`. The actual canonical files were also rendered through `render_readme` function-only with four controlled repository rows and missing-gate fallback. The caller and production bin both hash to `ef9cd915…fd9ca`; placeholders, fences, two disclosures, and fallback behavior passed.

Findings and limits retained in full:

- The installer wrapper’s post-CAS wording assertion failed after the successful mutation because the README says “raw KEEP was added prospectively.” Final verification was read-only; this is not a second CAS or a repaired history.
- The installer’s required first-tool sampler evidence is missing because its `tmpdir` was a pre-existing regular file. The later bounded sampler has only two durable samples with observable PID/exit/wait/reap; it cannot establish first-tool or continuous whole-worker coverage.
- The author and protected source reviewer’s late two-sample monitor limits remain limits. Current equality does not become historical custody proof.
- The original single `FAIL_CUSTODY`, Main D141hh’s bounded service acceptance, late raw KEEP, future-output-only relocation, and original no-body `1135` NOTRUN remain distinct. `TEST_KEEP` is future-only. No custody PASS, semantic re-review, source/prose repair, product test, build, service, full suite, REG0, or ZIP claim is made.
