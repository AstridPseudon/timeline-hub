# P4 D141c actual result custody review

Verdict: `FAIL` with one finite custody finding, `P4-D141c-R001`.

The genuine central request `agent-p4-current-becfe-http-3legs-1026011042-10086` is distinct from historical service `...-1347`. Its request, summary, snapshot, external-version record, terminal status, actual command, run manifest, JUnit, body log, and exits bind to the same normal request `p4-d141c-normal`.

The actual body result is `3 passed / 0 failed / 0 errors / 0 skipped`, exit `0`, JUnit time `23.668s`. The three JUnit module/name pairs map to the three full concrete selectors in `review.json`; each selected source file exists at the frozen Agent checkout, has the recorded source hash, and contains exactly one undecorated matching function definition. The command has `run -- -m pytest`, later `-m integration`, `-q`, cleared `addopts`, `-p no:cacheprovider`, timeout `45`, exactly three selectors, and no collection-only, skip, or xfail flag. The JUnit has no skipped nodes.

CAS custody also passes independently: the registry is mode `0600`; the backup equals the recorded preimage; the installed target row is exactly candidate SHA `21f407285a7f1476e9507add8d8d54e723776d6ce5074ac7cbbe8be5773c2f0b`; and all outside rows are byte-identical before/after. Manifest SHA `67ef4348b4b77eb02b74abe20ad6fefdb075f980dc8ca563c0a3c79d1f0e5b9f` materialized to a distinct body path with identical bytes.

## Finding P4-D141c-R001

The preserved manifest and runmanifest still contain:

`junit_paths=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-D141-cut-controller-0047/evidence/p4-d141c-normal.xml`

That path is absent. The actual command instead wrote to:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-D141-operational-return-0055/evidence/body-evidence/p4-d141c.xml`

The latter exists and hashes to `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d`. The stale field therefore affects receipt discoverability and prevents a clean `PASS_RESULT_CUSTODY`, but it does not erase the authentic result binding established by the central service artifacts and actual command. The stale value is preserved; no receipt was rewritten and no claim was made that the manifest-expected JUnit equals the actual JUnit path.

Historical `1347` remains a preserved zero-selector failure, `0101` remains `FAIL`, and `0106` remains `PASS_OPERATIONAL_SOURCE` with `INSTALLATION_NOT_READY`. App owns any cumulative P4 verdict. This result review is not a GO, ship, REG, full-suite, or product qualification decision.
