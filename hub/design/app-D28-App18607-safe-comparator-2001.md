# D28 App18607 safe comparator handoff

The exact retained App18607 run is `app-P1-local-OPS-1830-ap2-P1-chain-h6-1023185313-18607`, an actual direct-service snapshot at App `2107e1870e51c650d59315f4cc1ab6af338f198c`, Agent `78738040d72ce74c42ddf7731221aecb06f9246d`, Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`. The snapshot was clean. It was requested at `2026-10-23T18:53:13Z`, ended at `2026-10-23T19:05:41.146658791Z`, ran `744s`, and failed with exit `1`.

The first P1 case passed in `27.4s`. The second case failed before the second commit: expected two posts, observed one; the original assertion timed out at `90000ms`, then `afterEach` timed out at `300000ms`. Agent move, HTTP 409 refusal, and App rollback/message assertions were unreached. Cause is `UNKNOWN`.

Finite retained safe matrix:

- startup completion, public backend/door/editor addresses, compiled Runtime HTTP base, WebSocket host/path, health/realm/handshake, allowed-origin equality, credential/session presence, mounted project/timeline equality, actual authoring profile/quick descriptor, actual daemon Python, nested `astrid.sdk.timeline.commit` and `runtime_protocol` module paths, Playwright path/version, exact build command/dist path, and final-row projection/hash: `NOTCAPTURED` or `UNKNOWN` as applicable; no inference from source or setup.
- basis: `fields`; one basis item; `13` reads; read states `UNKNOWN` except the collection read, which is `NOTCAPTURED`. Four retained readonly records and one retained wire-head record have status `200`; this is not a health proof.
- preflight: D21 boundary passed and actual body executed. Node `v20.19.4`, npm `10.8.2`; Node executable path is retained in the Remotion env receipt. Child package origins are retained for top-level `astrid`, `astrid_runtime`, `runtime_protocol`, and `astrid_runtime_client`; actual daemon attribution remains `NOTCAPTURED`.
- presence-only environment keys (`ASTRID_QUICK_DESCRIPTOR`, `ASTRID_APP_DIRECT_DIST`, `ASTRID_APP_DIRECT_DOOR_PORT`, `ASTRID_APP_DIRECT_ORIGIN_PORT`, `NODE_PATH`, `NODE_OPTIONS`, `PYTHONPATH`, `VITE_RUNTIME_ORIGIN`, `VITE_WORKSPACE_RUNTIME_EXPECTED_*`): `NOTCAPTURED`; no unset claim.
- retained mode: `direct hosted dist`; log says hosted dist was current and build was skipped. Dist path is `NOTCAPTURED`.
- retained owner aggregate: `ownerCount=1`, `hasIdleOwner=true`; connected state is `UNKNOWN` (`connectionState=unknown`), with no owner identity.
- snapshot `%P` is unavailable. App `%H/%T` are `2107e1870e51c650d59315f4cc1ab6af338f198c` / `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`; Agent `%H/%T` are `78738040d72ce74c42ddf7731221aecb06f9246d` / `e77ea239789dd8ae9103c68fef79b49329cf2c6e`; Runtime `%H/%T` are `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` / `f79a2355cfb39d9ada7721978bd20d5702105778`; Composition `%H` is `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, `%T` unavailable.

Custody: the retained log is `26440` bytes / `62` lines; safe-export verification passed before and after export; raw bytes were not rewritten. The detailed capped record remains explicitly truncated/lost. No credentials, auth keys, principals, realm values, tokens, headers, cookies, raw bodies, full env, unsanitized console/trace, or credential/auth/raw-log hashes are included; the only hash-like values above are the explicitly requested source/snapshot identities. No new probe or test was run. Environment equivalence is **NOTPROVEN** and actual cause is **UNKNOWN**.

See the worker report for the full field/source/case/time/custody table and the names-only v2 wire boundary.
