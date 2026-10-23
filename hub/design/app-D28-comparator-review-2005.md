# D28 App18607 comparator independent audit

## Verdict

**FAIL.** The retained execution and raw-log custody claims in
`app-D28-App18607-safe-comparator-2001.md` are supported, but that handoff does
not satisfy the requested finite 1956 matrix as written. It leaves several
fields as generic `UNKNOWN`/`NOTCAPTURED` even though the exact run summary and
the retained 1829/1830 receipts provide bounded, public evidence. This is a
report-completeness failure, not a new behavioral or causal verdict.

## Verified retained run facts

- Run: `app-P1-local-OPS-1830-ap2-P1-chain-h6-1023185313-18607`; actual direct
  service snapshot, clean target; requested `2026-10-23T18:53:13Z`, ended
  `2026-10-23T19:05:41.146658791Z`; exit `1`, elapsed `744s`.
- Result remains exactly **1 PASS / 1 FAIL**. Case 1 passed in `27.4s`. Case 2
  failed at the expected-post boundary (`2` expected, `1` observed), then the
  original assertion and `afterEach` timed out. Agent move, HTTP 409 refusal,
  and App rollback/message assertions were unreached. Cause remains
  `UNKNOWN`.
- Retained raw log custody remains **26,440 bytes / 62 lines**; safe-export
  verification passed before and after export. Raw bytes were not rewritten.
- Retained source identities are App `2107e1870e51c650d59315f4cc1ab6af338f198c`
  with tree `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`, Agent
  `78738040d72ce74c42ddf7731221aecb06f9246d` with tree
  `e77ea239789dd8ae9103c68fef79b49329cf2c6e`, Runtime
  `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` with tree
  `f79a2355cfb39d9ada7721978bd20d5702105778`, and Composition
  `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` (tree unavailable).
- The retained exact summary has the public test command
  `npm run test:e2e:three-products -- tests/e2e/local/three-products.p1-chain.spec.ts`
  and the Playwright invocation/config. It records `[direct] hosted dist is
  current; skipping the build`.

## Concrete handoff omissions/corrections

1. **Node and installed module paths are captured, not merely “retained”.**
   The retained Remotion receipt is
   `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-remotion-app-p1-787-2a9-1830.env`.
   It records the public Remotion project directory
   `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830`, the Node
   executable path
   `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node`,
   Node `v20.19.4`, npm `10.8.2`, the schema Python path
   `/home/user/work/venv-agent/lib/python3.13/site-packages`, and the
   Agent/Runtime source commits above. The handoff should return those bounded
   public paths/versions; npm executable path remains `NOTCAPTURED`.

   The retained provision report is
   `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/provision/venv-agent-child-app-p1-787-2a9-1829.txt`.
   Its installed import origins are captured for `astrid`, `astrid_runtime`,
   `runtime_protocol`, and `astrid_runtime_client` at these public paths:

   ```text
   /home/user/work/venv-agent-child-app-p1-787-2a9-1829.partial.20261023T182941Z-12784/lib/python3.13/site-packages/astrid/__init__.py
   /home/user/work/venv-agent-child-app-p1-787-2a9-1829.partial.20261023T182941Z-12784/lib/python3.13/site-packages/astrid_runtime/__init__.py
   /home/user/work/venv-agent-child-app-p1-787-2a9-1829.partial.20261023T182941Z-12784/lib/python3.13/site-packages/runtime_protocol/__init__.py
   /home/user/work/venv-agent-child-app-p1-787-2a9-1829.partial.20261023T182941Z-12784/lib/python3.13/site-packages/astrid_runtime_client/__init__.py
   ```

   These are CLI/preflight installation origins only. They do **not** establish
   actual daemon/provider attribution; daemon Python, actual
   `astrid.sdk.timeline.commit` origin, and actual `runtime_protocol` origin
   remain `NOTCAPTURED`.

2. **Command-level environment presence can be safely stated.** In the exact
   retained command, `NODE_PATH` is explicitly removed (`env -u NODE_PATH`), so
   its body-command presence is **false**; `NODE_OPTIONS` and `PYTHONPATH` are
   explicitly assigned, so their body-command presence is **true**. The
   requested `ASTRID_QUICK_DESCRIPTOR`, `ASTRID_APP_DIRECT_DIST`,
   `ASTRID_APP_DIRECT_DOOR_PORT`, `ASTRID_APP_DIRECT_ORIGIN_PORT`,
   `VITE_RUNTIME_ORIGIN`, and `VITE_WORKSPACE_RUNTIME_EXPECTED_*` presence is
   **NOTCAPTURED**; absence from a receipt is not an unset claim. This is a
   bounded command-level observation, not a claim about every child process.

3. **Row hashes exist, but no final application-state projection is retained.**
   The safe packet records public hashes for the two retained diagnostic rows:

   - line 10: line hash
     `623197e4bdc045754664412d01c9953c2ac12563dd378c1bdab14634dd02e079`;
     source-range hash
     `6400ec8183c629b1d83b9e578b62357cfd3b951f51f46574ec6ad59e73c1405d`.
   - line 11: line hash
     `d9988f19348c0b7eeeb153b77bced2ee33457abdac6ffacf654e329c33c2192c`;
     source-range hash
     `ce8095346127435092a1a91279ee788513734695f34179fdd14cfa905ab0c59e`.

   A final-row projection of the mounted application state is not present in
   the safe packet and must remain `NOTCAPTURED`; the row hashes must not be
   presented as that projection. The public P1 source SHA is retained in the
   safe packet, and source/custody evidence is unchanged.

4. **Selected source versus synthetic snapshot.** The App/Agent/Runtime values
   above are selected source commit/tree identities recorded for the clean run
   target. They must not be labeled as an actual synthetic test snapshot tuple.
   The synthetic snapshot `%P` is unavailable; no synthetic `%H/%P/%T` tuple is
   reconstructed. The retained mode is explicitly actual direct service, not
   synthetic/control.

5. **No unsupported runtime state was promoted.** Public route/method/status
   observations in the actual safe packet include retained `200` readonly
   records for health/realm/handshake-related routes, but they do not prove
   health, realm, connection, authorization, mounted project/timeline
   equality, or transient connectedness. Basis remains `fields`, one item,
   `13` reads; detailed read states remain as captured. Owner aggregate is
   `ownerCount=1`, `hasIdleOwner=true`; connection state and owner identity
   remain `UNKNOWN`. No inference from earlier native runs was used.

## Scope, checks, and next step

This was a read-only artifact review. No live probe, browser/service/body
access, preflight, build, environment triage, test rerun, product change,
collector change, or Git operation was performed. Tests/typecheck/lint are
**N/A** for this review. The assigned worktree remained clean (`git status
--short`, `git diff --check`, and `git diff --stat` produced no output).

The author should first amend the handoff’s finite matrix with the bounded
facts above, preserving `UNKNOWN`/`NOTCAPTURED` where they remain applicable;
ProofSol1950 should continue to own the separate environment-equivalence and
causal verdict.
