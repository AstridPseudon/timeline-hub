# D73 independent receiving review

## Verdict

**FAIL for evidence integrity; receiving remains NOT_READY.** The route itself
is not admitted. The author packet correctly refuses readiness, but the packet
and its consumed source review contain two immutable/hash inconsistencies, and
the central suite digest is stale.

## Source-cited findings

1. `afda6c66a11608d8cb012df1a54bf2489d8c20b3` resolves to tree
   `67bd2d4ee1d50bd95ebb8b0de55d4d1ed1e3e87f` with parent
   `ff6498859bb2a72b1b7d52d807dd04d3852fc055`. Agent `2eca9a1d...` resolves to
   tree `888c16e3dbbff2d6827e7ffcfea64208b0e2a5e4` and Runtime `ab1e4f61...`
   resolves to tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`. The Runtime
   checkout is clean and receipt-backed; the exact Agent checkout receipt is
   absent. See the absolute `source-manifest.json` in this evidence directory.

2. Four candidate file blob/content pairs match the Git object. The candidate
   `ops-d73-exact-nodes/suites.conf` content hashes to
   `ddf8d6d20e9dbadbb4f23716726695b662c053f6d449c8d6e7df3d2d80d2f3c5`.
   The author/source manifest claims
   `ddf8d6d20e9dbadbb4f23716726695b662c053f6d449c8d6e7df3d2d80d2f3c5`.
   This is a one-character evidence error.

3. `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-D73-source-review-2209-review.json`
   records Agent tree `...b0e5a4`; the actual Git object and the author packet
   record `...b0e2a5e4`. The prior PASS7 controls were not rerun or relabeled.

4. Current `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test`
   and `test-run` match the prior recorded hashes. Current
   `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`
   hashes to `84d3045878ea806439b73b0a5ca983c06371fcac2d42bc8c7e8add0ebfbd3988`,
   not the prior `fecaa...` value. Neither exact D73 row is present. This is
   stale source metadata, not evidence that a row is installed.

5. The static route is exact: `integration:agent`, `--no-cache`, four named
   selected4 selectors and one named fork selector. The source row invokes the
   pinned launcher as `... MANIFEST run -- -m pytest -q -o addopts= -m
   integration -p no:cacheprovider --timeout=45 --junitxml=...`. The C0 guard
   records the requested full request/reply field set and makes no DTO change.

6. Missing App/Composition receipt identities, rendered newline manifest,
   interpreter/schema/profile/Node provenance, central rows, fresh per-ID
   artifacts and submit/end disk witnesses remain genuine. Every listed owner
   is justified by the current launcher or central route: the launcher checks
   all four checkout identities and preflight checks Python, Node, schema,
   nonsymlink `node_modules`, lock/archive/registry hashes, imports and the
   composition version. No claimed dependency was found to be unnecessary.

7. D139 is separate: current integration heads are Agent
   `cd63be424d62226e3ee5c26fc5ce03227f5394a5` and Runtime
   `f103bb46866999c961a8865636f2e66d544e0c9b`; the D73 route remains historical
   Agent 2eca + Runtime ab1e. The Runtime D139 dependency recipe remains the
   exclusive owner for the missing environment input. No old-tuple core or
   source overlay was used.

## Checks run

```text
python3 (stdlib JSON/hash/subprocess metadata comparison): PASS
git show/rev-parse Git object and blob checks: PASS, except the two recorded inconsistencies above
git diff --check: PASS
current central row lookup: PASS for absence of both exact D73 rows
df -B1 --output=avail /home/user: 5242650624 bytes observed; no submit/end witness exists
```

No product tests, typecheck, lint, imports, launcher, pytest, provider/body,
Store, child request, install, registration, acquisition, suite installation,
full suite, Git mutation, hub/design write, or D130 operation was performed.

The complete finite missing-input list remains at the absolute author path:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-OPS-D73-receiving-inputs-2227/evidence/missing-inputs.json`.
